from app.tg.callback.base import BaseCall, PageCall


class ItemInventoryCall(BaseCall, prefix='item_inventory'):
    pass


class ItemInfoCall(BaseCall, prefix='item_info'):
    item_id: int
    source: str
    page: int
    owned_quantity: int | None = None


class ItemQuantityCall(ItemInfoCall, prefix='item_quantity'):
    action: str


class ItemInventoryPageCall(PageCall, prefix='item_inventory_page'):
    pass


class ItemsPageCall(PageCall, prefix='items_page'):
    pass
