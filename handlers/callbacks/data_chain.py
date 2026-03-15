from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.keyboard import back_menu_keyboard
from others.states import ActionWallets

chain_router = Router()
    
@chain_router.callback_query(lambda chain: chain.data in ['eth_chain',
                                                          'bnb_chain',
                                                          'sol_chain',
                                                          'ton_chain'])
async def handler_blockchain(callback: CallbackQuery, state: FSMContext) -> None:
    data_message = await state.get_data()
    action = data_message.get('action')

    client_id = callback.from_user.id
    chain_data = callback.data
    
    await callback.bot.edit_message_text(chat_id=client_id,
                                         message_id=action,
                                         text=f'💬 Send me your address!',
                                         reply_markup=back_menu_keyboard)
    if chain_data == 'eth_chain':
        await state.set_state(
            ActionWallets.eth_wallet
            )
    elif chain_data == 'bnb_chain':
        await state.set_state(
            ActionWallets.bnb_wallet
            )
    elif chain_data == 'sol_chain':
        await state.set_state(
            ActionWallets.sol_wallet
        )
    elif chain_data == 'ton_chain':
        await state.set_state(
            ActionWallets.ton_wallet
        )
