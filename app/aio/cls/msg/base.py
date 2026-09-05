from app.aio.cls.msg.utils import TextHTML
import random

class Templates:
    directory_path = './app/aio/cls/msg/templates'

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

