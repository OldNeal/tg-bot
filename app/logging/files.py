from pathlib import Path
from app.exception.logs import DontExistCategoryException, DontHavePermissionException, DontLogFileException
from app.logging.paths import LogPaths

class LogFiles:
    @classmethod
    def get_by_name(cls, category: str, name: str):
        base = LogPaths.get(category)
        if base is None:
            raise DontExistCategoryException(all_categories=list(cls.categories.keys()))
        base = Path(base)

        if not name or "/" in name or "\\" in name or name in (".", ".."):
            raise DontHavePermissionException()
        
        file = (Path(base / Path(name)))

        if not file.is_relative_to(base):
            raise DontHavePermissionException()

        if file.suffix.lower() != '.log':
            raise DontLogFileException()
        
        if not file.is_file():
            raise DontLogFileException()
        
        return file

    @classmethod
    def get_by_mask(cls, mask_type: str):
        return [file for file in Path(LogPaths.logs).rglob('*.log') if file.name.split('_', maxsplit=1)[0] == mask_type]

    @classmethod
    def get_by_type(cls, type: str):
        return [file for file in Path(LogPaths.get(type)).glob('*.log')]

    @classmethod
    def get_all(cls):
        return [file for file in Path(LogPaths.logs).rglob('*.log')]
