from aiogram.fsm.state import State, StatesGroup

class Wallets(StatesGroup):
    edit_wallet = State()
    list_wallet = State()
    track_wallet = State()
    untrack_wallet = State()
