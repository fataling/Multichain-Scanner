from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

action_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                        [InlineKeyboardButton(text='➕ Track',
                                        callback_data='track'), 
                        InlineKeyboardButton(text='📒 Wallets',
                                        callback_data='my_wallets')]], 
                                                input_field_placeholder='What are we going to do today?')

blockchain_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='Ethereum',
                                      callback_data='eth_chain')],
                [InlineKeyboardButton(text='Binance Coin',
                                     callback_data='bnb_chain'),
                 InlineKeyboardButton(text='Toncoin',
                                     callback_data='ton_chain')],
                [InlineKeyboardButton(text='Solana',
                               callback_data='sol_chain')],
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')]
                        ], input_field_placeholder='Choose your chain...')

data_action_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='📌 Add',
                                      callback_data='track'),
                InlineKeyboardButton(text='❌ Delete',
                                     callback_data='delete_rows')],
                [InlineKeyboardButton(text='⭕ Delete all',
                                      callback_data='delete_all_rows')],
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')],
                        ], input_field_placeholder='What do you want to do?')

confirm_action_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='Yes',
                                      callback_data='yes_all'),
                InlineKeyboardButton(text='No',
                                     callback_data='no_all')],
                        ], input_field_placeholder='Confirm your action!')

back_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text='‹ Back',
                                      callback_data='back_menu')]
                        ], input_field_placeholder='Not a step forward!')
