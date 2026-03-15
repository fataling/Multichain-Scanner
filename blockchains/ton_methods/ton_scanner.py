from tonsdk.utils import Address

from typing import Optional, Union
from decimal import Decimal

from storage.lists_scanners import ton_rows, ton_hashes
from alarms.ton_alarm import ton_data_alarm
from .cfg import ton_node, ton_api_url
from others.cfg import log

import aiohttp
import asyncio

import base64

headers = {
    'X-API-Key': ton_node
}

async def ton_type_address(client_row: str) -> str:
    if client_row not in ton_hashes:
        ton_hashes[client_row] = {'Sent': set(),
                                  'Received': set()}
    
    return client_row

async def ton_scan_row(ssn: aiohttp.ClientSession, client_row: str) -> Optional[dict]:
    params = {'account': client_row,
              'limit': 3,
              'sort': 'desc'}
    try:
        rspc = await ssn.get(url=ton_api_url,
                             params=params)
        
        if rspc.status == 200:
            data = await rspc.json()
            if data != None:
                return data
        else:
            raise aiohttp.ServerConnectionError()
    except aiohttp.ClientError as a:
        log(f'An error occurred while processing data from the server!' - {a})
                
async def getDataTransaction(data: Optional[dict]) -> Optional[tuple]:
    if 'transactions' in data:
        transactions = data['transactions']
        
        if transactions != []:
            last_tx = transactions[0]
            last_hash = last_tx['hash']
            
            if last_tx['in_msg']:
                data_last_tx = last_tx, last_hash
                return data_last_tx
            elif last_tx['out_msgs']:
                data_last_tx = last_tx, last_hash
                return data_last_tx
            
async def getReceivedTransaction(data_last_tx: Optional[tuple], client_row: str) -> Optional[tuple]:
    row = Address(client_row) 
    raw_address = row.to_string(
        is_user_friendly=False
        ).upper()
    
    last_tx, last_hash = data_last_tx
    
    if last_tx['in_msg']['destination'] == raw_address:
        type_tx = f'Received'
        
    raw_value = last_tx['in_msg']['value']
    if raw_value is None:
        return None
    
    if last_hash not in ton_hashes[client_row]['Received']:
        ton_hashes[client_row]['Received'].add(last_hash)
    else:
        return None

    data_type_tx = raw_value, type_tx
    return data_type_tx
        
async def getOutgoingTransaction(data_last_tx: Optional[tuple], client_row: str) -> Optional[tuple]:
    row = Address(client_row) 
    raw_address = row.to_string(
        is_user_friendly=False
        ).upper()
    
    last_tx, last_hash = data_last_tx
    
    for data_tx in last_tx['out_msgs']:
        if data_tx['source'] == raw_address:
            type_tx = f'Sent'
            
        raw_value = data_tx['value']
        if raw_value is None:
            return None
        
        if last_hash not in ton_hashes[client_row]['Sent']:
            ton_hashes[client_row]['Sent'].add(last_hash)
        else:
            return None
    
        data_type_tx = raw_value, type_tx
        return data_type_tx
        
async def getValueTransaction(data_type_tx: Optional[tuple]) -> Union[int, float]:
    decimals = 9
    raw_value, _ = data_type_tx
    
    value = Decimal(raw_value) / Decimal(10**decimals)
    return value

async def decode_ton_hash(data_last_tx):
    _, last_hash = data_last_tx
    
    decode_hash = base64.b64decode(last_hash).hex()
    return decode_hash

async def process_ton_scan(ssn: aiohttp.ClientSession):
    try:
        for user_id, data in ton_rows.items():
            for ton_row in data:
                data_address = await ton_type_address(ton_row)
                if data_address is None:
                    return None
                
                data_all = await ton_scan_row(ssn,
                                              data_address)
                if data_all is None:
                    return None
            
                data_last_tx = await getDataTransaction(data_all)
                if data_last_tx is None:
                    return None
                
                data_type_tx = await getReceivedTransaction(data_last_tx,
                                                            data_address)
                if not data_type_tx:
                    data_type_tx = await getOutgoingTransaction(data_last_tx,
                                                                data_address)
                    if not data_type_tx:
                        continue
                
                value = await getValueTransaction(data_type_tx)
                if not value:
                    continue
                    
                decode_hash = await decode_ton_hash(data_last_tx)
                if not decode_hash:
                    continue
                
                _, type_tx = data_type_tx
                
                data_for_alarm = {'chat_id': user_id,
                                  'hash': decode_hash,
                                  'row': ton_row,
                                  'type_tx': type_tx,
                                  'amount_tx': value}
                await ton_data_alarm(data_for_alarm) 
    except Exception as a:
        log(f'Changes in data - {a}')
        
async def ton_main_scan():
    try:
        async with aiohttp.ClientSession(
            headers=headers
            ) as ssn:
            
            scan = True
            while scan:
                await process_ton_scan(ssn)
                await asyncio.sleep(0.5)
    except aiohttp.ServerConnectionError as a:
        log(f'An error occurred while connecting to the server! - {a}')
