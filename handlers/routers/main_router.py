from aiogram import Router

from .start_router import start_router
from ..callbacks.data_seed import seed_router

from ..callbacks.data_chain import chain_router
from ..callbacks.data_remove import remove_router
from .reg_router import reg_router

main_router = Router()

main_router.include_routers(
    start_router,
    seed_router,
    chain_router,
    reg_router,
    remove_router
)
