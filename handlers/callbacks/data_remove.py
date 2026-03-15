from aiogram import Router, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from storage.lists_scanners import (eth_rows,
                                    bnb_rows,
                                    sol_rows,
                                    ton_rows)

from storage.db import (
    sql3_remove_row,
    sql3_receipt_row,
    sql3_remove_all_row
    )
from keyboards.keyboard import (
    data_action_keyboard, 
    confirm_action_keyboard, 
    back_menu_keyboard
    )

from others.states import ActionWallets

import asyncio

remove_router = Router()

@remove_router.callback_query(lambda dlt_all_rows: dlt_all_rows.data == 'delete_all_rows')
async def remove_all_rows(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    
    client_id = callback.message.chat.id
    
    data = await sql3_receipt_row(
        client=client_id
        )
    if data != None:
            await callback.message.delete()
            await callback.message.bot.send_chat_action(chat_id=client_id,
                                                        action=ChatAction.TYPING)
            delete_row = await callback.message.answer(text=f'❓ You really want delete all your addresses?',
                                                       reply_markup=confirm_action_keyboard)
            await state.update_data(
                delete_row=delete_row.message_id
                )
            await state.set_state(ActionWallets.remove_all_wallet)
            return
    await callback.message.answer(
        text=f"🤔 You don't added any addresses yet!"
    )
    
@remove_router.callback_query(ActionWallets.remove_all_wallet)
async def handler_remove_all_rows(callback: CallbackQuery, state: FSMContext) -> None:
    step_data = await state.get_data()
    last_step = step_data.get('delete_row')
    
    client_id = callback.message.chat.id
    
    if callback.data == 'yes_all':
        await callback.bot.edit_message_text(chat_id=client_id,
                                             message_id=last_step,
                                             text=f'⌛️')
        for dicts in [eth_rows,
                      bnb_rows,
                      sol_rows,
                      ton_rows]:
            if client_id in dicts:
                dicts[client_id].clear()
            
        await sql3_remove_all_row(
            client=callback.from_user.id
        )
        await asyncio.sleep(0.75)
        await callback.bot.edit_message_text(chat_id=client_id,
                                             message_id=last_step,
                                             text=f'✅ Your addresses were success deleted!',
                                             reply_markup=back_menu_keyboard)
        await state.set_state(None)
        return
        
    if callback.data == 'no_all':
        data = await sql3_receipt_row(
            client=callback.from_user.id
            )
        if data != None:
            rows = '\n\n'.join(data)
            await callback.bot.edit_message_text(chat_id=client_id,
                                                 message_id=last_step,
                                                 text=f'<b>📋 Your addresses at moment:</b>\n\n\n'
                                                      f'<code>{rows}</code>',
                                                 reply_markup=data_action_keyboard,
                                                 parse_mode=ParseMode.HTML)
            await state.clear()
            return 

@remove_router.callback_query(lambda dlt_rows: dlt_rows.data == 'delete_rows')        
async def remove_row(callback: CallbackQuery, state: FSMContext) -> None:
    step_data = await state.get_data()
    last_step = step_data.get('action')
    
    client_id = callback.from_user.id
    
    data = await sql3_receipt_row(
        client=callback.from_user.id
        )
    if data != None:
        rows = '\n\n'.join(data)
        await callback.bot.edit_message_text(chat_id=client_id,
                                             message_id=last_step,
                                             text=f'Cool! Now option address which you want delete and send me his!\n\n\n\n'
                                             f'<code>{rows}</code>',
                                             parse_mode=ParseMode.HTML,
                                             reply_markup=back_menu_keyboard
                                             )
        await state.set_state(ActionWallets.remove_wallet)
        return
    await callback.message.bot.send_chat_action(chat_id=client_id,
                                                action=ChatAction.TYPING)
    await callback.message.answer(
        text=f'You not have addresses it yet, added their!'
        )
    await state.clear()
    return
    
@remove_router.message(ActionWallets.remove_wallet)
async def handler_remove_row(message: types.Message, state: FSMContext) -> None:
    row = message.text
    client_id = message.from_user.id
    
    data = await sql3_receipt_row(
        client_id
        )
    if data != None:
        await message.bot.send_chat_action(chat_id=client_id,
                                                action=ChatAction.TYPING)
        visual_delete_row = await message.answer(
            f'⌛️'
        )       
        await asyncio.sleep(0.75)
        if row not in data:
            await visual_delete_row.edit_text(
                text=f"❌ You don't tracking this address!"
            )
            return
        for dicts in [eth_rows,
                      bnb_rows,
                      sol_rows,
                      ton_rows]:
            if client_id in dicts:        
                dicts[client_id].remove(row) 
                 
        await sql3_remove_row(client_id,
                              row)
        await visual_delete_row.edit_text(text=f'✅ The address success delete!',
                                          reply_markup=back_menu_keyboard)
        await state.clear()
        return
