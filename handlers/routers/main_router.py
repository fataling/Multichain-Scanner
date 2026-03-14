from aiogram import Router

from .start_router import start_router
from ..callbacks.data_seed import seed_router

from ..callbacks.data_choice_chain import choice_chain_router
from .reg_router import reg_router
from ..callbacks.data_remove import remove_router

main_router = Router()

main_router.include_routers(
    start_router,
    seed_router,
    choice_chain_router,
    reg_router,
    remove_router
)
