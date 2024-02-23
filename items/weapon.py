from item import Item

class Weapon(Item):

    def __init__(self, name, damage, knockback, crit_chance, tooltip=None, uuid=None):
        super().__init__()
        self.name = name
        self.damage = damage
        self.knockback = knockback
        self.crit_chance = crit_chance
        self.tooltip = tooltip
