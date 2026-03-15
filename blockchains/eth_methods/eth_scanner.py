from decimal import Decimal
from typing import Optional

from storage.lists_scanners import eth_rows, eth_hashes
from alarms.eth_alarm import eth_data_alarm
from others.cfg import log
from .cfg import eth_node

import aiohttp
import asyncio

headers = {
    'Content-Type': 'application/json'
}

async def eth_type_address(client_row: str) -> str:
    if client_row not in eth_hashes:
        eth_hashes[client_row] = {'Sent': set(),
                                  'Received': set()}
    return client_row
    
async def eth_get_req(ssn: aiohttp.ClientSession) -> Optional[dict]:
    request_block_number = {"jsonrpc":"2.0",
                            "method": 'eth_blockNumber',
                            "params": [],
                            "id":1}
    
    try:
        rspc = await ssn.post(url=eth_node,
                              json=request_block_number)
        if rspc.status == 200:
            data = await rspc.json()
            if data != None:
                return data
        else:
            raise aiohttp.ServerConnectionError()
    except aiohttp.ClientError as a:
        log(f'An error occurred while processing data from the server!' - {a})
        
async def getLastBlock(data: Optional[dict]) -> Optional[dict]:
    if 'result' in data:
        result = data['result']
        if result != None:
            return result
        return None
    
async def getDataInBlock(ssn: aiohttp.ClientSession, result: Optional[dict]) -> Optional[dict]:
    request_block = {"jsonrpc": "2.0",
                     "method": 'eth_getBlockByNumber',
                     "params": [result, True],
                     "id": 1}
    
    try:
        rspc = await ssn.post(url=eth_node,
                              json=request_block)
        if rspc.status == 200:
            data_block = await rspc.json()
            if data_block != None:
                return data_block
        else:
            raise aiohttp.ServerConnectionError()
    except aiohttp.ClientError as a:
        log(f'An error occurred while processing data from the server!' - {a})

async def getDataTransaction(data_block: Optional[dict], client_row: str) -> Optional[dict]:
    result = data_block['result']
    if result is None:
        return None
    
    transactions = result['transactions']
    if transactions is None:
        return None
    
    for transaction in transactions:
        row_to = transaction['to']
        if row_to == client_row:
            return transaction
        
        from_to = transaction['from']
        if from_to == client_row:
            return transaction
    
async def getSenderInTransaction(client_row: str, transaction: Optional[dict]) -> Optional[tuple]:
    try:
        eth_hash_tx = transaction['hash']
        if eth_hash_tx is None:
            return None
    
        acc = transaction['from']
        if acc == client_row:
            type_tx = 'Sent'
        else:
            return None
    except KeyError as a:
        log(f'No found this key - {a}')
    
    data_type_tx = acc, type_tx, eth_hash_tx
    
    if eth_hash_tx not in eth_hashes[client_row]['Sent']:
        eth_hashes[client_row]['Sent'].add(eth_hash_tx)
    else:
        return None
    return data_type_tx
    
async def getRecipientInTransaction(client_row: str, transaction: Optional[dict]) -> Optional[tuple]:
    try:
        eth_hash_tx = transaction['hash']
        if eth_hash_tx is None:
            return None
        
        acc = transaction['to']
        if acc == client_row:
            type_tx = 'Received'
        else:
            return None
    except KeyError as a:
        log(f'Not found this key - {a}')
        
    data_type_tx = acc, type_tx, eth_hash_tx
    
    if eth_hash_tx not in eth_hashes[client_row]['Received']:
        eth_hashes[client_row]['Received'].add(eth_hash_tx)
    else: 
        return None
    return data_type_tx
    
async def getValueTx(transaction: Optional[dict]) -> Optional[Decimal]:
    decimals = 18
    
    try:
        raw_amount_tx = transaction['value']
        if raw_amount_tx is None:
            return None
    except KeyError as a:
        log(f'Not found this key - {a}')
    
    pre_amount_tx = int(raw_amount_tx, 16)
    
    amount_tx = Decimal(pre_amount_tx) / Decimal(10**decimals)
    return amount_tx

async def process_eth_scan(ssn: aiohttp.ClientSession):
    try:
        getNumberBlock = await eth_get_req(ssn)
        if getNumberBlock is None:
            return None
    
        getBlock = await getLastBlock(getNumberBlock)
        if getBlock is None:
            return None
    
        getDataBlock = await getDataInBlock(ssn,
                                            getBlock)
        if getDataBlock is None:
            return None
                
        for user_id, rows in eth_rows.items():
            for eth_row in rows:
                getClient = await eth_type_address(eth_row)
                if getClient is None:
                    continue
           
                getDataTx = await getDataTransaction(getDataBlock,
                                                        getClient)
                if getDataTx is None:
                    continue
           
                getSenderOrRecipient = await getSenderInTransaction(getClient,
                                                                    getDataTx)
                if getSenderOrRecipient is None:
                    getSenderOrRecipient = await getRecipientInTransaction(getClient,
                                                                            getDataTx)
                    if getSenderOrRecipient is None:
                        continue
     
                getValue = await getValueTx(getDataTx)
                if getValue is None:
                    continue
           
                _, type_tx, eth_hash_tx = getSenderOrRecipient
                
                data_for_alarm = {'chat_id': user_id,
                                'hash': eth_hash_tx,
                                'row': eth_row,
                                'type_tx': type_tx,
                                'amount_tx': getValue}
                await eth_data_alarm(data_for_alarm)
    except Exception as a:
        log(f'Changes in data - {a}')
        
async def eth_main_scan():
    try:
        async with aiohttp.ClientSession(
            headers=headers
            ) as ssn:
            
            scan = True
            while scan:
                await process_eth_scan(ssn)
                await asyncio.sleep(4)
    except aiohttp.ServerConnectionError as a:
        log(f'An error occurred while connecting to the server! - {a}')
