from aiogram import Dispatcher

from others.cfg import bot
from storage.db import sql3_table
from handlers.routers.main_router import main_router

from blockchains.eth_methods.eth_scanner import eth_main_scan
from blockchains.bnb_methods.bnb_scanner import bnb_main_scan
from blockchains.sol_methods.sol_scanner import sol_main_scan
from blockchains.ton_methods.ton_scanner import ton_main_scan

import asyncio

dp = Dispatcher()

dp.include_router(
    main_router
)   

async def main():
    await sql3_table()
    
    asyncio.create_task(eth_main_scan())
    asyncio.create_task(bnb_main_scan())
    asyncio.create_task(sol_main_scan())
    asyncio.create_task(ton_main_scan())
        
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main()) 
