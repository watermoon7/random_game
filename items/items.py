from equipable import Equipable
from placeable import Placeable
from weapon import Weapon
from tool import Tool
from item import Item


# DO NOT DO IT THIS WAY THIS IS SHIT
# lol

item_dict = {
    "equipable": Equipable,
    "placeable": Placeable,
    "weapon": Weapon,
    "tool": Tool,
    "item": Item,
}
def create_item(name, type_, *args):
    return item_dict[type_](
        name, *args
    )

weapons = {
    "Iron Sword": None,
}