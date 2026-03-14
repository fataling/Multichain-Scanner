from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from keyboards.keyboard import action_keyboard

start_router = Router()

@start_router.message(Command('start'))
async def handler_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    
    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)
    action_buttons = await message.answer(text=f'<b>Hello, this is a Tracker.</b>\n\n'
                                              f"🕵🏻 I can track wallets, let's get started!",
                                          reply_markup=action_keyboard,
                                          parse_mode=ParseMode.HTML)
    await state.update_data(
        action=action_buttons.message_id
        )
    
@start_router.message(StateFilter(None))
async def handler_any_message(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    
    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)
    buttons = await message.answer(text=f'🙊 <b>Oops!</b>\n\n'
                                        f"😶 I don't know how to communicate, please select the action button below!",
                                   reply_markup=action_keyboard,
                                   parse_mode=ParseMode.HTML)
    await state.update_data(
        action=buttons.message_id
        )
