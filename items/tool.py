from item import Item

class Tool(Item):

    def __init__(self, name, power, damage, knockback, crit_chance, tooltip=None):
        super().__init__()
        self.name = name
        self.power = power
        self.damage = damage
        self.knockback = knockback
        self.crit_chance = crit_chance
        self.tooltip = tooltip
