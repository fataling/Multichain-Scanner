from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

action_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                        [InlineKeyboardButton(text='➕ Track',
                                        callback_data='track'), 
                        InlineKeyboardButton(text='❌ Untrack',
                                        callback_data='untrack'),
                        InlineKeyboardButton(text='📒 Wallets',
                                        callback_data='my_wallets')]], 
                                                input_field_placeholder='Type me Satoshi address...')

blockchain_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='Ethereum',
                                      callback_data='ethereum_chain'),
                InlineKeyboardButton(text='BNB',
                                      callback_data='bnb_chain')],
                [InlineKeyboardButton(text='Solana',
                               callback_data='sol_chain'),
                InlineKeyboardButton(text='Ton',
                                     callback_data='ton_chain')],
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')]],
                                        input_field_placeholder='Tell me his...')
