from datetime import datetime, timedelta
from math import ceil

from app.tg.text.base import Templates, BaseText
from app.validate.base import BaseValidate
from app.validate.api import AnswerTimeInfo

class BeyonderText(BaseText):
    drink_template = Templates(templates_file_name='drink.txt')
    upseq_template = Templates(templates_file_name='upseq.txt')
    downseq_template = Templates(templates_file_name='downseq.txt')
    kill_template = Templates(templates_file_name='kill.txt')

    def __init__(self, data: BaseValidate):
        self.data = data
  
    @property
    def drink(self):
        return self.drink_template.random().format_map(self.data.model_dump())

    @property
    def upseq(self):
        return self.upseq_template.random().format_map(self.data.model_dump())
    
    @property
    def downseq(self):
        return self.downseq_template.random().format_map(self.data.model_dump())
    
    @property
    def accert_kill(self):
        return self.kill_template.random().format_map(self.data.model_dump())

    def kill(self, tg_id: int, is_admin: bool):
        telegram = self.data.user.telegram
        if (telegram and telegram.tg_id == tg_id) or not is_admin:
            return f'☠️ {self.html('Вы').openmessage(tg_id)} хотите потерять контроль?'
        return f'☠️ {self.html('Вы').openmessage(tg_id)} хотите, чтобы потусторонний {self.user_mention(self.data.purpose)} потерял контроль?'
    
    @property
    def cancel_kill(self):
        return f'{self.user_mention(self.data.purpose)} смог успокоиться и не потерять контроль'
    
    @classmethod
    def time_info(self, data: AnswerTimeInfo):
        time = timedelta(seconds=data.total_seconds)
        total_seconds = max(0, ceil(time.total_seconds()))
        hours, seconds = divmod(total_seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if time.total_seconds() > 0:
            time_text = '⏳ Осталось '
            if time.days <= 0:
                if hours > 0:
                    time_text += f'{hours} ч. '
                if minutes > 0:
                    time_text += f'{minutes} мин. '
                if seconds > 0:
                    time_text += f'{seconds} сек.'
            else:
                time_text += f'дней: {time.days}'
        else:
            time_text = '🚀 Вы можете продвинуться'
        return self.user_mention(data.purpose) + self.html.joined([
            f'📅 Послед. продвижение: {datetime.fromisoformat(data.last_upseq).date()}',
            f'⚡ След. продвижение: {datetime.fromisoformat(data.next_upseq).date()}',
            time_text,
        ]).blockquote()
    
    @property
    def time_redact(self):
        time = timedelta(seconds=self.data.seconds)
        total_seconds = max(0, ceil(time.total_seconds()))
        hours, seconds = divmod(total_seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if time.days <= 0:
            time_text = ''
            if hours > 0:
                time_text += f'{hours} ч. '
            if minutes > 0:
                time_text += f'{minutes} мин. '
            if seconds > 0:
                time_text += f'{seconds} сек. '
        else:
            time_text = f'{hours} ч. {minutes} мин. {seconds} сек.'
        return self.user_mention(self.data.purpose) + self.html.joined([
            f'📅 Старая дата: {datetime.fromisoformat(self.data.old_time).date()}',
            f'⚡ Новая дата: {datetime.fromisoformat(self.data.new_time).date()}',
            f'{'➖ Убрано' if self.data.operator == '-' else '➕ Добавлено'} {f'дней: {time.days}' if time.days > 0 else time_text}',
        ]).blockquote()
    
    @property
    def time_replace(self):
        return self.user_mention(self.data.purpose) + self.html.joined([
            f'📅 Старая дата: {datetime.fromisoformat(self.data.old_time).date()}',
            f'⚡ Новая дата: {datetime.fromisoformat(self.data.new_time).date()}'
        ]).blockquote()
    
    @property
    def info(self):
        beyonder = [f'🔮 Обычный смертный']
        user = self.data.purpose.telegram

        if self.data.beyonder:
            if self.data.beyonder.seq > 0:
                beyonder = [f'🔮 Путь: {self.data.beyonder.path_name}',
                f'🧪 Последовательноcть: {self.data.beyonder.seq} - {self.data.beyonder.seq_name}']
            elif self.data.beyonder.seq == 0:
                beyonder = [f'🎗 {self.data.beyonder.seq_name}']
            elif self.data.beyonder.seq < 0:
                beyonder = [f'🏵 {self.data.beyonder.seq_name}']

        return self.user_mention(self.data.purpose) + self.html(self.html.joined([
            f'🏷 ID: {user.tg_id} ({self.data.purpose.user_id})',
            f'🔗 Юз: {self.html(user.username or '❌').escape().openmessage(user.tg_id)}'
            ] + beyonder)).blockquote()
    
    def list(self, max_page: int, page: int, count: int):
        return f'📊 Статистика пути "{self.html(f'{self.html(self.data.path.emodzi or '🎗️').emoji(self.data.path.custom_emodzi_id)} {self.data.path.name}')}" {f'[{page+1}/{max_page} стр.]' if max_page > 1 else ''}' + self.html.joined([
            f'🏵 ВД: {self.user_mention(self.data.ga.user) if self.data.ga else '❌'}',
            f'🧪 Потусторонних: {count}'
        ]).blockquote()
