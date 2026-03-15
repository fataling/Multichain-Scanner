from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from storage.db import sql3_receipt_row
from keyboards.keyboard import (
    blockchain_keyboard,
    data_action_keyboard,
    action_keyboard,
    back_menu_keyboard
)

seed_router = Router()

@seed_router.callback_query(lambda trk: trk.data == 'track')
async def track_back(callback: CallbackQuery, state: FSMContext) -> None: 
    await callback.answer()
    step_data = await state.get_data()
    last_step = step_data.get('action')
    
    client_id = callback.from_user.id
    data = await sql3_receipt_row(
        client=client_id
    )
    if data != None:
        if len(data) >= 5:
            await callback.bot.edit_message_text(chat_id=client_id,
                                                 message_id=last_step,
                                                 text=f'📚 You have too many addresses!',
                                                 reply_markup=back_menu_keyboard)
            return
    await callback.bot.edit_message_text(chat_id=client_id,
                                        message_id=last_step,
                                        text=f'<b>Select blockchain</b>',
                                        reply_markup=blockchain_keyboard,
                                        parse_mode=ParseMode.HTML)
            
@seed_router.callback_query(lambda mywall: mywall.data == 'my_wallets')
async def my_wallets_back(callback: CallbackQuery, state: FSMContext) -> None:
    step_data = await state.get_data()
    last_step = step_data.get('action')
    
    client_id = callback.from_user.id
    
    data = await sql3_receipt_row(
        client=client_id
        )
    if data != None:
        rows = '\n\n'.join(
                f'{i}. {row}'
                for i, row in enumerate(data,
                                        start=1)
        )
        await callback.bot.edit_message_text(chat_id=client_id,
                                             message_id=last_step,
                                             text=f'<b>📋 Your addresses at moment:</b>\n\n\n'
                                             f'<code>{rows}</code>',
                                             reply_markup=data_action_keyboard,
                                             parse_mode=ParseMode.HTML)
        return
    await callback.bot.edit_message_text(chat_id=client_id,
                                         message_id=last_step,
                                         text=f'🤷‍♀️ You not have addresses it yet, added their!',
                                         reply_markup=back_menu_keyboard)
    await state.clear()
    return
    
@seed_router.callback_query(lambda back: back.data == 'back_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    main_menu = await callback.message.edit_text(text=f'↩️ Your return to main menu!\n\n\n'
                                                      f'<b>👇 Select action by clicking the button below</b>',
                                                 reply_markup=action_keyboard,
                                                 parse_mode=ParseMode.HTML)
    await state.update_data(
        action=main_menu.message_id
        )
