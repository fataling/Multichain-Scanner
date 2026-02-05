from aiogram import Router

from .chat_routers import chat_router
from .callbacks import callback_router
from .primary_routers import primary_router
from .fsm import blockchain_router

main_router = Router()

main_router.include_routers(
    primary_router,
    chat_router,
    callback_router,
    blockchain_router
)
