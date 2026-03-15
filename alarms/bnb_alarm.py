from others.cfg import bot, log
from keyboards.alarm_buttons import bnbscan_button

from aiogram.exceptions import (
    TelegramNetworkError,
    TelegramUnauthorizedError,
    TelegramForbiddenError
    )
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

async def bnb_data_alarm(data_for_alarm: dict) -> None:
    bnb_row = data_for_alarm['row']
    hash_tx = data_for_alarm['hash']   
       
    url = f'https://bscscan.com/tx/{hash_tx}'
    url_acc = f'https://bscscan.com/address/{bnb_row}'
    
    data_for_alarm['url'] = url
    data_for_alarm['url_acc'] = url_acc
    
    short_url = f"{bnb_row[:6]}...{bnb_row[-4:]}"
    data_for_alarm['short_url'] = short_url
    
    await alarm_to_chat(data_for_alarm)

async def alarm_to_chat(data_for_alarm: dict) -> None:
    button = bnbscan_button(data_for_alarm['url'])
    
    try:
        await bot.send_message(chat_id=data_for_alarm['chat_id'],
                               text=f'🔔 <b>Transaction is found!</b>\n\n'
                                     f"👛 <b>Wallet:</b> <a href='{data_for_alarm['url_acc']}'>{data_for_alarm['short_url']}</a>\n"
                                     f"📬 Type: <b>{data_for_alarm['type_tx']}</b>\n"
                                     f"💎 Value: <code>{data_for_alarm['amount_tx']}</code> BNB",
                               reply_markup=button,
                               link_preview_options=LinkPreviewOptions(
                                   is_disabled=True
                                   ),
                               parse_mode=ParseMode.HTML)
    except TelegramNetworkError as a:
        log(f'A network error occurred, please try again later! - {a}')
    except TelegramUnauthorizedError as b:
        log(f'Maybe, bot not detected! - {b}')
    except TelegramForbiddenError as c:
        log(f'Bot not have access to have chat! - {c}')
