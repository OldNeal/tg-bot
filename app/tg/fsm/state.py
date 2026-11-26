from aiogram.fsm.state import State, StatesGroup

class MainState(StatesGroup):
    users_search = State()
    settings = State()
    setting_text = State()

class OrganState(StatesGroup):
    create = State()
    settings = State()
    titul = State()
    search = State()
    setting_subparameter = State()
    setting_text = State()

class WikiState(StatesGroup):
    search = State()

class StatsState(StatesGroup):
    search = State()

class NewsPaperState(StatesGroup):
    search = State()
    settings = State()
    setting_text = State()
    create = State()

class QuestionState(StatesGroup):
    create = State()
    json_create = State()
    moderation_edit = State()
    moderation_reason = State()

class ItemState(StatesGroup):
    quantity = State()

class BeyonderState(StatesGroup):
    method_action_study = State()
