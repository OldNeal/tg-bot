from app.tg.text.base import Templates, BaseText
from app.validate.core import AnswerBaseInfo, AnswerUserBody
from app.tg.settings import is_setting_available, selected_setting_group, values_by_tag

class MainText(BaseText):
    def __init__(self, data: AnswerBaseInfo):
        self.data: AnswerBaseInfo = data

    @classmethod
    def menu(self):
        return '🧭 Главное меню'

    @classmethod
    def user_settings_editor(cls, groups, group_tag: str | None = None):
        choice_labels = {
            'notify_platform': {'telegram': 'Телеграм'},
            'notify_type': {
                'ephemeral_message': 'Эфемерное сообщение',
                'private_chat': 'В личный чат с ботом',
            },
        }
        lines = []
        values = values_by_tag(groups)
        selected = selected_setting_group(groups, group_tag)
        for group in [selected] if selected else []:
            for parameter in group.parametrs:
                if parameter.is_hidden or not is_setting_available(parameter, values):
                    continue
                value = parameter.value
                choices = getattr(parameter, 'choises', None) or choice_labels.get(parameter.tag)
                if isinstance(choices, dict):
                    value = choices.get(value, value)
                if isinstance(value, bool):
                    value = '✅ Да' if value else '❌ Нет'
                elif value is None:
                    value = '❌'

                emoji = parameter.emodzi or group.emodzi or '⚙️'
                custom_emoji_id = parameter.custom_emodzi_id or group.custom_emodzi_id
                icon = cls.html(emoji).emoji(custom_emoji_id)
                line = f'{icon} {cls.html(parameter.name).escape()}: {cls.html(str(value)).escape()}'
                lines.append(line)

        group_name = f' ({selected.name})' if selected else ''
        title = cls.html(f'⚙️ Настройки аккаунта{group_name}').escape().bold()
        return title + cls.html.joined(lines).blockquote()

    @property
    def info(self):
        member_text = [f'🏛 В организации не состоит']
        beyonder_text = [f'🔮 Обычный смертный']

        member = self.data.member
        beyonder = self.data.beyonder
        user = self.data.purpose or self.data.user
        telegram = user.telegram

        if member:
            member_text = [f'🏛 Организация: {member.organ_name}',
            f'⚜️ Ранг: {member.rank_name} ({member.rank})']
            if member.titul:
                member_text.append(f'🎖 Титул: {self.html(member.titul).escape()}')

        if beyonder:
            if beyonder.seq > 0:
                beyonder_text = [f'🔮 Путь: {beyonder.path_name}',
                f'🧪 Последовательноcть: {beyonder.seq} - {beyonder.seq_name}']
            elif beyonder.seq == 0:
                beyonder_text = [f'🎗 {beyonder.seq_name}']
            elif beyonder.seq < 0:
                beyonder_text = [f'🏵 {beyonder.seq_name}']

        user_id = telegram.tg_id if telegram else user.user_id
        username = telegram.username if telegram else None
        return f'{self.html(user.emodzi or '🪪').custom_emoji(user.custom_emodzi_id) if user.custom_emodzi_id else user.emodzi or '🪪'} ' + self.user_mention(user) + self.html(self.html.joined([
                f'🏷 ID: {user_id} ({user.user_id})',
                f'🔗 Юз: {self.html(username or '❌').escape().openmessage(telegram.tg_id) if telegram else '❌'}',
            ] + member_text + beyonder_text)).blockquote()

    @classmethod
    def check_ping(self, core_ping: str | None = None):
        return f'⌛ Задержка CORE - {core_ping} мс.'

    @classmethod
    def state_clear(self):
        return f'✅ Куки очищены'

    @classmethod
    def state_pop(self):
        return f'✅ Кук удален'

    @classmethod
    def state_dont_pop(self):
        return f'❌ Кук не найден'

    @classmethod
    def users_list(cls, count: int, page: int, max_page: int):
        if not count:
            return '❌ Пользователей нет'
        return f'👥 Пользователи: {count} {cls.page_text(page, max_page)}'

    @classmethod
    def users_search_fields(cls):
        return '🔎 Выберите критерий поиска'

    @classmethod
    def users_search_input(cls, field: str):
        labels = {
            'user_id': 'внутренний ID',
            'tg_id': 'Telegram ID',
            'username': 'username',
            'name': 'имя',
        }
        return f'✒️ Введите {labels[field]} пользователя'

    @classmethod
    def users_search_results(cls, count: int, page: int, max_page: int):
        if not count:
            return '❌ Пользователи по этому запросу не найдены'
        return f'🔎 Найдено пользователей: {count} {cls.page_text(page, max_page)}'

    @classmethod
    def user_info(cls, user: AnswerUserBody):
        telegram = user.telegram
        details = [
            f'🏷 Внутренний ID: {user.user_id}',
            f'🪦 Имя: {cls.user_mention(user)}',
            f'🆔 Telegram ID: {telegram.tg_id if telegram else "❌"}',
            f'🔗 Username: {cls.html(telegram.username or '❌').escape().openmessage(telegram.tg_id) if telegram else '❌'}',
        ]
        return '👤 Аккаунт' + cls.html(cls.html.joined(details)).blockquote()

    @classmethod
    def user_updated(cls):
        return '✅ Информация о пользователе обновлена'

    @classmethod
    def user_deleted(cls, user: AnswerUserBody):
        return f'✅ {cls.html('Ваш').escape().openmessage(user.telegram.tg_id)} аккаунт удалён. Если вы продолжите использовать бота, то он создаст вам новый аккаунт.'

    @classmethod
    def user_delete_cancelled(cls):
        return '🗑 Удаление аккаунта отменено'

    @classmethod
    def user_delete_confirm(cls, user: AnswerUserBody):
        return f'🗑 {cls.html('Вы').escape().openmessage(user.telegram.tg_id)} хотите удалить свой аккаунт? После удаления все ваши данные удаляются и сбрасывается прогресс. Позже их уже нельзя будет востановить'

    @classmethod
    def get_activity_points(self, activity_points: int):
        return f'🪙 Получены очки активнрности: {activity_points}'
