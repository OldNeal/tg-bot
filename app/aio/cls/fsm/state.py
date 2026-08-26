from aiogram.fsm.state import State, StatesGroup

class OrganState(StatesGroup):
    settings = State()
    titul = State()
    search = State()


