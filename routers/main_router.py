from aiogram import Router

from .chat_routers import chat_router
from .callbacks import callback_router

main_router = Router()

main_router.include_routers(
    chat_router,
    callback_router
)
