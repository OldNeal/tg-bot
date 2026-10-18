from pathlib import PurePath

from config import settings

class LogPaths:
    logs = PurePath(settings.log_files_path)
    base = logs / PurePath('base/')
    beyonder = logs / PurePath('beyonder/')
    organ = logs / PurePath('organ/')

    categories = {
        'base':base,
        'beyonder':beyonder,
        'organ':organ
    }

    @classmethod
    def get(cls, category: str):
        path = cls.categories.get(category)
        return path
    