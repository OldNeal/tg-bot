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
        return await self.state.update_data(**{self.prefix + k: v for k, v in kwargs.items()} | {self.prefix + 'state_keys': state_keys + [self.prefix + k for k in kwargs.keys() if self.prefix + k not in state_keys]})
    
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
        data = await self.state.get_data()
        new_data = {k:v for k, v in data.items() if k not in data.get(self.prefix + 'state_keys', [])}
        return await self.state.set_data(new_data)

    async def set_data(self, data: dict):
        return await self.state.set_data({self.prefix + k: v for k, v in data.items() if not v is None})

    async def remove_value(self, key: str):
        data = await self.get_data()
        state_keys = data.get('state_keys', [])
        data['state_keys'] = [k for k in state_keys if key not in k]
        return await self.set_data({k: v for k, v in data.items() if key != k})

    async def save_message(self, chat_id: int, message_id: int):
        return await self.update_data(chat_id=chat_id, message_id=message_id)
    
    async def get_message(self) -> tuple[int, int]:
        return await self.get_value('chat_id'), await self.get_value('message_id')
    
    async def remove_message(self):
        await self.remove_value('chat_id')
        await self.remove_value('message_id')
    

class MainFSM(FSMUtils):
    prefixs = ['main']

class BeyonderFSM(FSMUtils):
    prefixs = ['beyonder']

class WikiFSM(FSMUtils):
    prefixs = ['wiki']

class OrganFSM(FSMUtils):
    prefixs = ['organ']
