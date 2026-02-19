from web3 import AsyncWeb3, AsyncHTTPProvider

from aiogram import types
from aiogram.enums import ChatAction

from scanners.alarms import eth_alarm_to_user
from tokens import evm_node

import asyncio

w3_connect = AsyncWeb3(AsyncHTTPProvider(evm_node))

async def eth_type_address(message: types.Message, client_row):
    chat_id = message.from_user.id
    type_row = await w3_connect.eth.get_code(client_row)
    
    if type_row == b'':
        asyncio.create_task(eth_scan_row(chat_id, client_row))
        return True
    else:
        await message.bot.send_chat_action(chat_id=message.chat.id,
                                           action=ChatAction.TYPING)
        await message.answer(
            text=f'Dont check smart-contracts!'
        )
        return False
    
async def eth_scan_row(chat_id, client_row):
    hashs = []
    
    while True:
        last_block = await w3_connect.eth.get_block(block_identifier='latest',
                                                    full_transactions=True)
        
        transactions = last_block['transactions']
        for transaction in transactions:
            hash_id = transaction['hash'].hex()
            
            if hash_id not in hashs:
                row_to = transaction['to']
                row_from = transaction['from']
            
                if row_to == client_row or row_from == client_row:
                    hashs.append(hash_id)
                    await eth_alarm_to_user(chat_id, hash_id, client_row)
                    
                    if len(hashs) == 15:
                        hashs.clear()
            
        await asyncio.sleep(2)
