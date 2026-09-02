from app.logic.base import BaseLogic
from app.logic.utils import class_decor

@class_decor
class StatsLogic(BaseLogic):
    async def all(self):
        return await self.client.stats_all()
    