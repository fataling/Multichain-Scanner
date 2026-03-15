from aiogram import Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from typing import Optional

from others.states import ActionWallets
from aiogram.filters import StateFilter
from keyboards.keyboard import back_menu_keyboard
from storage.db import sql3_addopt_row, sql3_receipt_row

from storage.lists_scanners import (eth_rows,
                                    bnb_rows, 
                                    sol_rows, 
                                    ton_rows)

from validators.eth import valid_string_eth
from validators.bnb import valid_string_bnb
from validators.sol import valid_string_sol
from validators.ton import valid_string_ton

import asyncio 

reg_router = Router()

async def require_eth_address(client_id: int, row: str) -> Optional[bool]:
    rows = await sql3_receipt_row(
        client=client_id
    )
    if rows != None:
        if row in rows:
            return True
    
async def eth_valid_address(row: str) -> Optional[bool]:
    validator = await asyncio.to_thread(valid_string_eth,
                                        row)
    if validator is True:
        return True
        
@reg_router.message(StateFilter(ActionWallets.eth_wallet))
async def eth_reg_address(message: types.Message, state: FSMContext) -> None:
    eth_row = message.text
    client_id = message.from_user.id
    
    await message.bot.send_chat_action(chat_id=client_id,
                                       action=ChatAction.TYPING)
    msg = await message.answer(text='📝 Adding your ETH address to the list...',
                               reply_markup=back_menu_keyboard)
    
    success_reg = await require_eth_address(client_id,
                                            eth_row)
    if success_reg is True:
        await msg.edit_text(text=f'🔎 You are already tracking this address!',
                            reply_markup=back_menu_keyboard)
        await state.clear()
        return

    valid = await eth_valid_address(eth_row)
    if valid is True:
        await asyncio.sleep(1)
        await sql3_addopt_row(client_id,
                              eth_row)
        await msg.edit_text(text=f'✅ Your address was added to list!',
                            reply_markup=back_menu_keyboard)
        if client_id not in eth_rows:
            eth_rows[client_id] = set()
        eth_rows[client_id].add(eth_row.lower())
        
        await state.clear()
        return
    await msg.edit_text(text='⚠️ This address is invalid!',
                        reply_markup=back_menu_keyboard)


async def require_bnb_address(client_id: int, row: str) -> Optional[bool]:
    rows = await sql3_receipt_row(
        client=client_id
    )
    if rows != None:
        if row in rows:
            return True
    
async def bnb_valid_address(row: str) -> Optional[bool]:
    validator = await asyncio.to_thread(valid_string_bnb,
                                        row)
    if validator is True:
        return True
    
@reg_router.message(StateFilter(ActionWallets.bnb_wallet))
async def bnb_reg_address(message: types.Message, state: FSMContext) -> None:
    bnb_row = message.text
    client_id = message.from_user.id
    
    await message.bot.send_chat_action(chat_id=client_id,
                                       action=ChatAction.TYPING)
    msg = await message.answer(text='📝 Adding your BNB address to the list...',
                               reply_markup=back_menu_keyboard)
    
    success_reg = await require_bnb_address(client_id,
                                            bnb_row)
    if success_reg is True:
        await msg.edit_text(text=f'🔎 You are already tracking this address!',
                            reply_markup=back_menu_keyboard)
        await state.clear()
        return

    valid = await bnb_valid_address(bnb_row)
    if valid is True:
        await asyncio.sleep(1)
        await sql3_addopt_row(client_id,
                              bnb_row)
        await msg.edit_text(text=f'✅ Your address was added to list!',
                            reply_markup=back_menu_keyboard)
        if client_id not in bnb_rows:
            bnb_rows[client_id] = set()
        bnb_rows[client_id].add(bnb_row.lower())
        
        await state.clear()
        return
    await msg.edit_text(text='⚠️ This address is invalid!',
                        reply_markup=back_menu_keyboard)


async def require_sol_address(client_id: int, row: str) -> Optional[bool]:
    rows = await sql3_receipt_row(
        client=client_id
    )
    if rows != None:
        if row in rows:
            return True
    
async def sol_valid_address(row: str) -> Optional[bool]:
    validator = await asyncio.to_thread(valid_string_sol,
                                        row)
    if validator is True:
        return True
    
@reg_router.message(StateFilter(ActionWallets.sol_wallet))
async def sol_reg_address(message: types.Message, state: FSMContext) -> None:
    sol_row = message.text
    client_id = message.from_user.id
    
    await message.bot.send_chat_action(chat_id=client_id,
                                        action=ChatAction.TYPING)
    msg = await message.answer(text='📝 Adding your SOL address to the list...',
                               reply_markup=back_menu_keyboard)
    success_reg = await require_sol_address(client_id,
                                            sol_row)
    if success_reg is True:
        await msg.edit_text(text=f'🔎 You are already tracking this address!',
                            reply_markup=back_menu_keyboard)
        await state.clear()
        return
    
    valid = await sol_valid_address(sol_row)
    if valid is True:
        await asyncio.sleep(1)
        await sql3_addopt_row(client_id,
                              sol_row)
        if client_id not in sol_rows:
            sol_rows[client_id] = set()
        sol_rows[client_id].add(sol_row)
        
        await msg.edit_text(text=f'✅ Your address was added to list!',
                            reply_markup=back_menu_keyboard)
        
        await state.clear()
        return
    await msg.edit_text(text='⚠️ This address is invalid!',
                        reply_markup=back_menu_keyboard)


async def require_ton_address(client_id: int, row: str) -> Optional[bool]:
    rows = await sql3_receipt_row(
        client=client_id
    )
    if rows != None:
        if row in rows:
            return True
    
async def ton_valid_address(row: str) -> Optional[bool]:
    validator = await asyncio.to_thread(valid_string_ton,
                                        row)
    if validator is True:
        return True
    
@reg_router.message(StateFilter(ActionWallets.ton_wallet))
async def ton_reg_address(message: types.Message, state: FSMContext) -> None:
    ton_row = message.text
    client_id = message.from_user.id
    
    await message.bot.send_chat_action(chat_id=client_id,
                                       action=ChatAction.TYPING)
    msg = await message.answer(text='📝 Adding your TON address to the list...',
                               reply_markup=back_menu_keyboard)
    
    success_reg = await require_ton_address(client_id,
                                            ton_row)
    if success_reg is True:
        await msg.edit_text(text=f'🔎 You are already tracking this address!',
                    reply_markup=back_menu_keyboard)
        await state.clear()
        return

    valid = await ton_valid_address(ton_row)
    if valid is True:
        await asyncio.sleep(1)
        await sql3_addopt_row(client_id,
                              ton_row)
        await msg.edit_text(text=f'✅ Your address was added to list!',
                            reply_markup=back_menu_keyboard)
        
        if client_id not in ton_rows:
            ton_rows[client_id] = set()
        ton_rows[client_id].add(ton_row)
        
        await state.clear()
        return
    await msg.edit_text(text='⚠️ This address is invalid!',
                        reply_markup=back_menu_keyboard)
