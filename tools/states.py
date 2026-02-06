from aiogram.fsm.state import State, StatesGroup

class ActionWallets(StatesGroup):
    add_wallet = State()
    remove_wallet = State()
    
    validator = State()
