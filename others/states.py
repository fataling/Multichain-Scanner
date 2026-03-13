from aiogram.fsm.state import State, StatesGroup

class ActionWallets(StatesGroup):
    eth_wallet = State()
    bnb_wallet = State()
    sol_wallet = State()
    ton_wallet = State()
    
    remove_wallet = State()
    remove_all_wallet = State()
