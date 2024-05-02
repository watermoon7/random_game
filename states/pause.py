import pygame, sys
import numpy as np
from utils import add
from GUI.button import Button
from states.gamestate import GameState


class Pause(GameState):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.pos = tuple(map(int, (master.width * 0.1, master.height * 0.1)))
        self.size = tuple(map(int, (master.width * 0.8, master.height * 0.8)))
        self.screen_rect = pygame.Rect((*self.pos, *self.size))

        self.grid = (16, 12)
        self.grid_cell_size = np.array(self.size) / np.array(self.grid)
        self.grid_cell_width = self.grid_cell_size[0]
        self.grid_cell_height = self.grid_cell_size[1]

        self.main_buttons = (
            Button(
                add(self.pos, self.grid_cell_size),
                self.grid_cell_width * 14,
                self.grid_cell_height,
                command=self.master.change_state,
                args=["game"],
                text="Return to game",
            ),  # return to game button
            Button(
                add(self.pos, self.grid_cell_size, [0, 2 * self.grid_cell_height]),
                self.grid_cell_width * 14,
                self.grid_cell_height,
                command=self.change_buttons,
                args=["options"],
                text="Options",
            ),  # options button
            Button(
                add(self.pos, self.grid_cell_size, [0, 4 * self.grid_cell_height]),
                self.grid_cell_width * 14,
                self.grid_cell_height,
                command=self.master.change_state,
                args=["main_menu"],
                text="Quit"
            ),  # quit
        )
        self.options_buttons = (
            Button(
                add(self.pos, self.grid_cell_size),
                self.grid_cell_width * 2,
                self.grid_cell_height,
                command=self.change_buttons,
                args=["main"],
                text="Option 1"
            ),
            Button(
                add(self.pos, self.grid_cell_size, [3 * self.grid_cell_width, 0]),
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 2"
            ),
            Button(
                add(self.pos, self.grid_cell_size, [6 * self.grid_cell_width, 0]),
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 3"
            ),
            Button(
                add(self.pos, self.grid_cell_size, [9 * self.grid_cell_width, 0]),
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 4"
            ),
            Button(
                add(self.pos, self.grid_cell_size, [12 * self.grid_cell_width, 0]),
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 5"
            )
        )

        self.button_interface = {
            "main": self.main_buttons,
            "options": self.options_buttons,
        }
        self.current_interface = "main"
        self.buttons = self.button_interface[self.current_interface]

    def change_buttons(self, interface):
        if interface in self.button_interface:
            self.current_interface = interface
            self.buttons = self.button_interface[self.current_interface]
        else:
            print("No button interface called:", interface)

    def event(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.current_interface != "main":
                        self.change_buttons("main")
                    else:
                        self.master.change_state("game")

        for button in self.buttons:
            button.event(events)

    def render(self, screen):
        pygame.draw.rect(self.master.screen, (0, 100, 150), self.screen_rect)

        for button in self.buttons:
            button.draw(screen)

        pygame.display.update()

    def start(self):
        self.running = True
        self.current_interface = "main"
        self.buttons = self.button_interface[self.current_interface]

    def stop(self):
        ...
