from tokens import token_bot
from aiogram import Bot

import logging

logging.basicConfig(level=logging.INFO, 
                    format="%(message)s")
log = logging

bot = Bot(token=token_bot)
