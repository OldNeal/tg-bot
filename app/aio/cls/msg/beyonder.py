from app.aio.cls.msg.base import Templates, BaseText
from datetime import datetime, timedelta
from app.validate.base import BaseValidate

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
    def kill(self):
        return self.kill_template.random().format_map(self.data.model_dump())
    
    @property
    def time_info(self):
        return self.html(self.data.user.fullname).openmessage(self.data.user.tg_id) + self.html.joined([
            f'📅 Послед. продвижение: {datetime.fromisoformat(self.data.last_upseq).date()}',
            f'⚡ След. продвижение: {datetime.fromisoformat(self.data.next_upseq).date()}',
            f'⏳ Осталось дней: {self.data.upseq_days}',
        ]).blockquote()
    
    @property
    def time_redact(self):
        return self.html(self.data.user.fullname).openmessage(self.data.user.tg_id) + self.html.joined([
            f'📅 Старая дата: {datetime.fromisoformat(self.data.old_time).date()}',
            f'⚡ Новая дата: {datetime.fromisoformat(self.data.new_time).date()}',
            f'{'➖ Убрано' if self.data.operator == '-' else '➕ Добавлено'} дней: {timedelta(seconds=self.data.seconds).days}',
        ]).blockquote()
    
    @property
    def time_replace(self):
        return self.html(self.data.user.fullname).openmessage(self.data.user.tg_id) + self.html.joined([
            f'📅 Старая дата: {datetime.fromisoformat(self.data.old_time).date()}',
            f'⚡ Новая дата: {datetime.fromisoformat(self.data.new_time).date()}'
        ]).blockquote()
