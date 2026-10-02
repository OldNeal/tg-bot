from pathlib import PurePath

class LogPaths:
    logs = PurePath('logs/')
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
    