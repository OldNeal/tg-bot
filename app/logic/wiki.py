from app.logic.base import BaseLogic

class WikiLogic(BaseLogic):
    async def all_seqs(self):
        return await self.client.get_seqs()
    

    async def path(self, name: str | None = None, id: int | None = None):
        return await self.client.get_path(name, id)
    
    async def all_paths(self):
        return await self.client.get_paths()
    
    async def search_path(self, value: str):
        return await self.client.search_path(value)


    async def ga(self, name: str | None = None, id: int | None = None):
        return await self.client.get_ga(name, id)

    async def all_gas(self):
        return await self.client.get_gas()

    async def search_ga(self, value: str):
        return await self.client.search_ga(value)
    
    
    async def all_groups(self):
        return await self.client.get_groups()

    async def search_group(self, name: str):
        return await self.client.get_group(name)
    