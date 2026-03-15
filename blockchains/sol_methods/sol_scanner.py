from decimal import Decimal
from typing import Optional

from storage.lists_scanners import sol_hashes, sol_rows
from alarms.sol_alarm import sol_data_alarm
from others.cfg import log
from .cfg import sol_node

import aiohttp
import asyncio

headers = {
    'Content-Type': 'application/json'
}

async def sol_type_address(client_row: str) -> str:
    if client_row not in sol_hashes:
        sol_hashes[client_row] = {'Sent': set(),
                                  'Received': set()}
    return client_row
    
async def sol_get_req(ssn: aiohttp.ClientSession, client_row: str) -> Optional[dict]:
    getSignature = { "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getSignaturesForAddress",
                    "params": [
                    f"{client_row}",
                    {
                    "commitment": "finalized",
                    "limit": 3
                    }
                ]
            }
    
    try:
        rspc = await ssn.post(url=sol_node,
                            json=getSignature
        )
        if rspc.status == 200:
            data = await rspc.json()
            if data != None:
                return data
        else:
            raise aiohttp.ServerConnectionError()
    except aiohttp.ClientError as a:
        log(f'An error occurred while processing data from the server!' - {a})
        
async def getDataTransaction(data: Optional[dict]) -> Optional[str]:
    if 'result' in data:
        result = data['result']
        
        if result != []:
            last_signature = result[0]['signature']
            return last_signature
        else:
            return None
            
async def getDataSignature(ssn: aiohttp.ClientSession, last_signature: Optional[str]) -> Optional[dict]:
    request_sign = { "jsonrpc": "2.0",
                  "id": 1,
                  "method": "getTransaction",
                  "params": [
                  f"{last_signature}",
                    {
                      "commitment": "confirmed",
                      "maxSupportedTransactionVersion": 0,
                      "encoding": "json"
                    }
                ]
            }
    
    try:
        rspc = await ssn.post(url=sol_node,
                              json=request_sign)
        if rspc.status == 200:
            data_sign = await rspc.json()
            if data_sign != None:
                return data_sign
        else:
            raise aiohttp.ServerConnectionError()
    except aiohttp.ClientError as a:
        log(f'An error occurred while processing data from the server!' - {a})
    
async def getSenderInSignature(data_sign: Optional[dict], last_signature: Optional[str], client_row: str) -> Optional[tuple]:
    result = data_sign['result']
    if result is None:
        return None
    
    transaction = result['transaction']
    if transaction is None:
        return None
    
    message = transaction['message']
    if message is None:
        return None
            
    acc = message['accountKeys'][0]
    if acc == client_row:
        type_tx = 'Sent'
    else:
        return None
    
    data_type_tx = acc, type_tx
    
    if last_signature not in sol_hashes[client_row]['Sent']:
        sol_hashes[client_row]['Sent'].add(last_signature)
    else:
        return None
    return data_type_tx

async def getRecipientInSignature(data_sign: Optional[dict], last_signature: Optional[str], client_row: str) -> Optional[tuple]:
    result = data_sign['result']
    if result is None:
        return None
    
    transaction = result['transaction']
    if transaction is None:
        return None
    
    message = transaction['message']
    if message is None:
        return None
    
    acc = message['accountKeys'][1]
    if acc == client_row:
        type_tx = 'Received'
    else:
        return None
    
    data_type_tx = acc, type_tx
    
    if last_signature not in sol_hashes[client_row]['Received']:
        sol_hashes[client_row]['Received'].add(last_signature)
    else:
        return None
    return data_type_tx

async def getBalancesAccounts(data_sign: Optional[dict], data_type_tx: Optional[tuple]) -> tuple:
    decimals = 9
    _, type_tx = data_type_tx
    
    result = data_sign['result']
    if result is None:
        return None
        
    meta = result['meta']
    if meta is None:
        return None
    
    if type_tx == 'Sent':
        raw_postBalances = meta['postBalances'][0]
        postBalances = Decimal(raw_postBalances) / Decimal(10**decimals)
            
        raw_preBalances = meta['preBalances'][0]
        preBalances = Decimal(raw_preBalances) / Decimal(10**decimals)
        
        data_balances = postBalances, preBalances
        return data_balances
    
    if type_tx == 'Received':
        raw_postBalances = meta['postBalances'][1]
        postBalances = Decimal(raw_postBalances) / Decimal(10**decimals)
            
        raw_preBalances = meta['preBalances'][1]
        preBalances = Decimal(raw_preBalances) / Decimal(10**decimals)
        
        data_balances = postBalances, preBalances
        return data_balances
    
async def getValueTx(data_balances: tuple, data_type_tx: Optional[tuple]):
    postBalances, preBalances = data_balances
    _, type_tx = data_type_tx
    
    if type_tx == 'Sent':
        raw_value = preBalances - postBalances
        
        value = raw_value.normalize()
        return value
    if type_tx == 'Received':
        raw_value = postBalances - preBalances
        
        value = raw_value.normalize()
        return value

async def process_sol_scan(ssn: aiohttp.ClientSession):
    try:
        for user_id, rows in sol_rows.items():
            for sol_row in rows:
                getClient = await sol_type_address(sol_row)
                if getClient is None:
                    return None
                
                getSign = await sol_get_req(ssn,
                                            getClient)
                if getSign is None:
                    return None
                
                getDataTx = await getDataTransaction(getSign)
                if getDataTx is None:
                    return None
                
                getDataSign = await getDataSignature(ssn,
                                                     getDataTx)
                if getDataSign is None:
                    return None
                
                getSenderOrRecipient = await getSenderInSignature(getDataSign,
                                                                  getDataTx,
                                                                  getClient)
                if not getSenderOrRecipient:
                    getSenderOrRecipient = await getRecipientInSignature(getDataSign,
                                                                         getClient,
                                                                         getDataTx)
                    if not getSenderOrRecipient:
                        continue
                
                getBalances = await getBalancesAccounts(getDataSign,
                                                        getSenderOrRecipient)
                if not getBalances:
                    continue
                
                getValue = await getValueTx(getBalances,
                                            getSenderOrRecipient)
                if not getValue:
                    continue
                
                _, type_tx = getSenderOrRecipient
                
                data_for_alarm = {'chat_id': user_id,
                                  'hash': getDataTx,
                                  'row': sol_row,
                                  'type_tx': type_tx,
                                  'amount_tx': getValue}
                await sol_data_alarm(data_for_alarm)
    except Exception as a:
        log(f'Changes in data - {a}')
        
async def sol_main_scan():
    try:
        async with aiohttp.ClientSession(
            headers=headers
            ) as ssn:
            
            scan = True
            while scan:
                await process_sol_scan(ssn)
                await asyncio.sleep(0.5)
    except aiohttp.ServerConnectionError as a:
        log(f'An error occurred while connecting to the server! - {a}')
