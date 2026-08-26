from app.aio.cls.msg.base import Templates, BaseText
from app.validate.api import AnswerOrganInfo, AnswerMemberInfo, AnswerOrganInfoDescription, SettingGroupValidate, AnswerOrganInfoMembers
from datetime import datetime

class OrganText(BaseText):
    def __init__(self, data: AnswerOrganInfo | AnswerOrganInfoDescription | AnswerOrganInfoMembers):
        self.data = data

    @property
    def user_name(self):
        return self.html(self.data.user.fullname).openmessage(self.data.user.tg_id)

    @property
    def organ_name(self):
        return self.data.organ.name
 

    @classmethod
    def menu(self):
        return '🏛️ Меню'

    @classmethod
    def search(self, value: str, count: int, page: int, max_page: int):
        return f'🔎 По запросу "{value}" были найдены организации ({count} шт.) [{page + 1}/{max_page} стр.]' if count > 0 else '❌ Ничего не найдено'
    
    @classmethod
    def to_search(self):
        return '✒️ Введите поисковой запрос'

    @property
    def members(self):
        return '👥 Все участники'
    
    @classmethod
    def list(self, page: int, max_page: int):
        return f'📜 Все организации [{page + 1}/{max_page} стр.]'

    @property
    def info(self):
        organ = self.data.organ
        return f'{self.html(organ.emodzi or '🏛').emoji(organ.custom_emodzi_id)} {organ.name}' + self.html(self.html.joined([
            f'🏷 ID: {organ.id}',            
            f'👑 Глава: {(self.html(organ.owner.user.fullname or organ.owner.user.username).openmessage(organ.owner.user.tg_id)) if organ.owner else "❌"}',           
            f'👥 Участников: {organ.member_counts}',
        ])).blockquote()

    @property
    def desc(self):
        return (self.html('🪶 Описание').h1.br.br + self.html(self.data.description)) if self.data.description else '🪶 Описание отсуствует'

    @classmethod
    def member(self, user: AnswerMemberInfo):
        member = [f'🏛 В организации не состоит']

        if user.member:
            member = [f'🏛 Организация: {user.member.organ_name}',
            f'⚜️ Ранг: {user.member.rank_name} ({user.member.rank})']
            if user.member.titul:
                member.append(f'🎖 Титул: {user.member.titul}')
            #f'⌛ Состоит в организации дней: {(datetime.now() - datetime.fromisoformat(user.member.login_at)).days}'

        return self.user_name + self.html(self.html.joined([f'🏷 ID: {user.user.tg_id}'] + member)).blockquote()

    @classmethod
    def top(self):
        return '🏆 Топ организаций по количеству участников'





    @property
    def login(self):
        return self.user_name + f' стал участником организации self.data.organ.name'

    @classmethod
    def to_exit(self):
        return 'Вы хотите выйти из организации?'

    @property
    def exit(self):
        return self.user_name + f' вышел из организации "{self.organ_name}"'
    
    @property
    def cancel_exit(self):
        return self.user_name + f' передумал выходить из организации "{self.organ_name}"'

    @property
    def create(self):
        return self.user_name + f' создал организацию "{self.organ_name}"'

    @classmethod
    def parametr_value(self, value):
        if isinstance(value, bool): 
            return '✅' if value else '❌'
        return value

    @classmethod
    def to_enter_paramet(self):
        return '🪶 Отправьте новые настройки'

    @classmethod
    def settings(self, setting: SettingGroupValidate):
        return '⚙️ Настройки' + self.html.joined([
            f'{self.html(p.emodzi or '').emoji(p.custom_emodzi_id)} {p.name}: {self.parametr_value(p.value)}' for p in setting.parametrs if not p.is_hidden
        ]).blockquote()

    @classmethod
    def settings_values(self, values: dict):
        return '⚙️ Настройки' + self.html.json_format(values, indent=4).code().pre('json')   
    
    @property
    def capture(self):
        return self.user_name + f' захватил организацию "{self.organ_name}"'




    def uprank(self, rank: int):
        return self.user_name + f' был повышен до {rank} ранга'
    
    def downrank(self, rank: int):
        return self.user_name + f' был понижен до {rank} ранга'

    @classmethod
    def kick(self, purpose: AnswerMemberInfo):
        return f'Вы хотите выгнать {self.html(purpose.user.fullname).openmessage(purpose.user.tg_id)} из организации {purpose.member.organ_name}?'

    @property
    def accert_kick(self):
        return self.user_name + f' был выгнан из организации "{self.organ_name}"'

    @property
    def cancel_kick(self):
        return self.user_name + f' передумал кикать'
        
    @classmethod
    def redact_titul(self):
        return f'Введите новый титул'

    def titul(self, old_titul: str | None = None, new_titul: str | None = None):
        if new_titul:
            result = f'получил титул "{new_titul}"'
        elif old_titul:
            result = f'лишился титула "{old_titul}"'
        return f'{self.user_name} {result}'
            
    def give(self, purpose: AnswerMemberInfo):
        return f'{self.user_name} передал организацию "{self.organ_name}" пользователю {self.html(purpose.user.fullname).openmessage(purpose.user.tg_id)}'

    @classmethod
    def to_give(self, purpose: AnswerMemberInfo):        
        return f'Вы хотите передать организацию "{purpose.member.organ_name}" пользователю {self.html(purpose.user.fullname).openmessage(purpose.user.tg_id)}'

    @property
    def cancel_give(self):
        return self.user_name + f' передумал передавать организацию "{self.organ_name}"'