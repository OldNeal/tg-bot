from aiogram.fsm.context import FSMContext

class FSMUtils:
    prefixs: list[str] = []
    
    def __init__(self, state: FSMContext | None, prefix_two: str = ''):
        self.state = state
        self.prefix_two = prefix_two
 
    def add_prefix(self, *prefix_two: str):
        return FSMUtils(self.state, (self.prefix + '_'.join(prefix_two)).removeprefix('_').removesuffix('_'))

    @property
    def prefix(self):
        return '_'.join(self.prefixs + [self.prefix_two])
    
    async def get_value(self, key: str, default = None):
        return await self.state.get_value(self.prefix + key, default)
    
    async def update_data(self, **kwargs):
        state_keys = await self.get_value('state_keys', [])
        return await self.state.update_data(**{self.prefix + k: v for k, v in kwargs.items()} | {self.prefix + 'state_keys': state_keys + [self.prefix + k for k in kwargs.keys()]})
    
    async def set_state(self, new_state = None):
        return await self.state.set_state(new_state)
 
    async def get_state(self):
        return await self.state.get_state()

    async def get_data(self):
        data = await self.state.get_data()
        return {k.replace(self.prefix, ''):v for k,v in data.items()}

    async def clear(self):
        return await self.state.clear()
    
    async def clear_this_state(self):
        data = await self.get_data()
        new_data = {k:v for k, v in data.items() if k not in data.get(self.prefix + 'state_keys', [])}
        return await self.state.set_data(new_data)

class MainFSM(FSMUtils):
    prefixs = ['main']

class BeyonderFSM(FSMUtils):
    prefixs = ['beyonder']

class WikiFSM(FSMUtils):
    prefixs = ['wiki']

class OrganFSM(FSMUtils):
    prefixs = ['organ']
