from aiogram.fsm.state import State, StatesGroup

class OrganState(StatesGroup):
    create = State()
    settings = State()
    titul = State()
    search = State()


