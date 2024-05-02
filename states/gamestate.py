class GameState:
    def __init__(self, master):
        self.master = master
        self.cell_size = master.cell_size
        self.width = master.width
        self.height = master.height
        self.screen = master.screen

    def start(self):
        pass

    def stop(self):
        pass

    def event(self, events):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

