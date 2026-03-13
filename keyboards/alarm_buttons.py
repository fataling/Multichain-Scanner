from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def etherscan_button(url: str):
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='EtherScan',
                                        url=url)]])
     
def bnbscan_button(url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='BscScan',
                                    url=url)]])

def tonviewer_button(url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Tonviewer Exployer',
                                    url=url)]
                    ])
    
def solscan_button(url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='SolScan',
                                    url=url)]
                    ])
