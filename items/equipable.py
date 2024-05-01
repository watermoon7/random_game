from item import Item

class Equipable(Item):

    def __init__(self, name, defense, tooltip=None):
        super().__init__()
        self.name = name
        self.damage = defense
        self.tooltip = tooltip
