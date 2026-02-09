from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

action_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                        [InlineKeyboardButton(text='➕ Track',
                                        callback_data='track'), 
                        InlineKeyboardButton(text='📒 Wallets',
                                        callback_data='my_wallets')]], 
                                                input_field_placeholder='Type me Satoshi address...')

blockchain_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='Ethereum',
                                      callback_data='eth_chain'),
                 InlineKeyboardButton(text='Binance Coin',
                                     callback_data='bnb_chain')],
                [InlineKeyboardButton(text='Solana',
                               callback_data='sol_chain'),
                 InlineKeyboardButton(text='Toncoin',
                                     callback_data='ton_chain')],
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')]
                        ],
                                        input_field_placeholder='Tell me his...')


wallets_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='📌 Add',
                                      callback_data='track'),
                InlineKeyboardButton(text='❌ Delete',
                                     callback_data='untrack')],
                [InlineKeyboardButton(text='⭕ Delete all',
                                      callback_data='delete_all')],
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')]
                        ]
        )

confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='Yes',
                                      callback_data='pidor'),
                 InlineKeyboardButton(text='No',
                                     callback_data='popa')],
                [InlineKeyboardButton(text='‹ Back',
                               callback_data='back_menu')],
                        ],
                                        input_field_placeholder='Tell me his...')
