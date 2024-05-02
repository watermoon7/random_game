from item import Item

class Placeable(Item):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.max_stack_size = 999