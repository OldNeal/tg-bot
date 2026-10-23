import random

from app.tg.text.utils import TextHTML

class Templates:
    directory_path = './app/tg/text/templates'

    def __init__(self, *, templates_file_path: str | None = None, templates_file_name: str | None = None, templates: list[str] | None = None):
        self.templates_file_path = templates_file_path
        self.templates_file_name = templates_file_name
        self.templates = templates

    def random(self):
        msgs: list[str] = []
        if self.templates_file_path:
            with open(self.templates_file_path, encoding='UTF_8') as f:
                msgs.extend(f.readlines())
        if self.templates_file_name:
            with open(f'{self.directory_path}/{self.templates_file_name}', encoding='UTF_8') as f:
                msgs.extend(f.readlines())
        if self.templates:
            msgs.extend(self.templates)
        return random.choice(msgs)

class BaseText:
    html = TextHTML

    @classmethod
    def json(self, data: dict):
        text = self.html.json_format(data, 4)
        return self.html.anchor('start-json') + text.pre('json').details('JSON', text.count('\n') > 10) + self.html('Вверх').href('#start-json')