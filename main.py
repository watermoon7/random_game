import pygame
from states import (
    game,
    main_menu,
    pause,
)


class RandomGame:
    def __init__(self, width, height, fps):
        self.dt = None
        self.width = width
        self.height = height
        self.screen_rect = pygame.Rect((0, 0, width, height))
        self.screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        self.cell_size = 10
        self.running = True

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.states = {
            "main_menu": main_menu.MainMenu(self),
            "game": game.GameLoop(self),
            "pause": pause.Pause(self),
        }
        self.current_state = self.states["main_menu"]
        self.loaded_level = ""

    def change_state(self, new_state):
        self.current_state.stop()
        self.current_state = self.states[new_state]
        self.current_state.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.dt = min(self.clock.tick(self.fps), 33) / 1000
            self.current_state.event(pygame.event.get())
            self.current_state.update()
            self.current_state.render(self.screen)

        pygame.quit()


if __name__ == "__main__":
    game = RandomGame(1200, 800, 60)
    game.run()
