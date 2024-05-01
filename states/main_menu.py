import pygame
import numpy as np
from player import Player
from states.gamestate import GameState
from GUI.button import Button
from GUI.text_input import TextInput
from GUI.scrollable_container import ScrollableContainer
from world.block import Block
from world.generate import generate_chunk
from world.save import save


class MainMenu(GameState):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.screen = master.screen

        self.size = (master.width, master.height)
        self.width, self.height = self.size

        self.grid = (30, 20)
        self.grid_cell_size = np.array(self.size) / np.array(self.grid)
        self.grid_cell_width = self.grid_cell_size[0]
        self.grid_cell_height = self.grid_cell_size[1]

        with open("world/world_data.txt", 'r') as f:
            self.world_names = [name for name in f.read().split("\n") if name]

        self.new_world_input = TextInput(
            self.grid_cell_size,
            self.grid_cell_width * 28,
            self.grid_cell_height * 2,
            font_size=40,
        )

        self.main_widgets = [
            Button(
                self.grid_cell_size,
                self.grid_cell_width * 15,
                self.grid_cell_height * 5,
                command=self.change_widgets,
                args=["play"],
                text="Play",
                font_size=40,
            ),
            Button(
                [self.grid_cell_width, 7 * self.grid_cell_height],
                self.grid_cell_width * 15,
                self.grid_cell_height * 5,
                command=self.change_widgets,
                args=["options"],
                text="Options",
                font_size=40,
            ),
            Button(
                [self.grid_cell_width, 13 * self.grid_cell_height],
                self.grid_cell_width * 15,
                self.grid_cell_height * 5,
                command=self.master.stop,
                text="Quit",
                font_size=40,
            )
        ]
        world_buttons = ScrollableContainer(self.grid_cell_size, self.grid_cell_width * 15,
                                            self.grid_cell_height * 10, self.grid_cell_height, separation=10)
        for i, name in enumerate(self.world_names):
            world_buttons.add_item(
                Button(
                    [self.grid_cell_width, (2 * i + 1) * self.grid_cell_height],
                    self.grid_cell_width * 15,
                    self.grid_cell_height,
                    command=self.enter_level,
                    args=[name],
                    text=name,
                )
            )
        self.play_widgets = [
            Button(
                [self.grid_cell_width, self.height - 2 * self.grid_cell_height],
                self.grid_cell_width * 28,
                self.grid_cell_height,
                command=self.change_widgets,
                args=["main"],
                text="Return to the main menu!",
            ),
            Button(
                [self.grid_cell_width, self.height - 4 * self.grid_cell_height],
                self.grid_cell_width * 28,
                self.grid_cell_height,
                command=self.change_widgets,
                args=["new_world"],
                text="New world!",
            ),
            world_buttons,
        ]
        self.new_world_widgets = [
            self.new_world_input,
            Button(
                [self.grid_cell_width, self.height - 2 * self.grid_cell_height],
                self.grid_cell_width * 28,
                self.grid_cell_height,
                command=self.new_world,
                args=None,
                text="Create",
            )
        ]
        self.options_widgets = [
            Button(
                [self.grid_cell_width, 3 * self.grid_cell_height],
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 1"
            ),
            Button(
                [4 * self.grid_cell_width, 3 * self.grid_cell_height],
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 2"
            ),
            Button(
                [7 * self.grid_cell_width, 3 * self.grid_cell_height],
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 3"
            ),
            Button(
                [10 * self.grid_cell_width, 3 * self.grid_cell_height],
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 4"
            ),
            Button(
                [13 * self.grid_cell_width, 3 * self.grid_cell_height],
                self.grid_cell_width * 2,
                self.grid_cell_height,
                text="Option 5"
            ),
            Button(
                self.grid_cell_size,
                self.grid_cell_width * 28,
                self.grid_cell_height,
                command=self.change_widgets,
                args=["main"],
                text="Back",
            )
        ]

        self.widget_interface = {
            "main": self.main_widgets,
            "play": self.play_widgets,
            "options": self.options_widgets,
            "new_world": self.new_world_widgets,
        }
        self.current_interface = "main"
        self.widgets = self.widget_interface[self.current_interface]

    def reset_play_button_positions(self):
        ...

    def change_widgets(self, interface):
        if interface in self.widget_interface:
            if self.current_interface == "play":
                self.reset_play_button_positions()
            self.current_interface = interface
            self.widgets = self.widget_interface[self.current_interface]
        else:
            print("No widget interface called:", interface)

    def start(self):
        self.change_widgets("main")

    def enter_level(self, name):
        self.master.loaded_level = name
        self.master.change_state("game")

    def new_world(self):
        name = self.new_world_input.get_text()
        self.master.loaded_level = name
        self.new_world_input.set_text("")
        if not name or name in self.world_names:
            return

        self.world_names.append(name)

        self.play_widgets.append(
            Button(
                [self.grid_cell_width, (2 * len(self.world_names) - 1) * self.grid_cell_height],
                self.grid_cell_width * 15,
                self.grid_cell_height,
                command=self.enter_level,
                args=[name],
                text=name
            )
        )

        # generate more than one chunk
        chunk = generate_chunk(self.master.width, self.master.height, self.master.cell_size)

        blocks = pygame.sprite.Group()
        for y, row in enumerate(chunk):
            for x, col in enumerate(row):
                if col == "g":
                    block_position = [
                        x * self.master.cell_size,
                        y * self.master.cell_size
                    ]
                    block = Block(
                        [x, y],
                        block_position,
                        self.master.cell_size,
                        'grass',
                        pygame.Color('springgreen3')
                    )
                    blocks.add(block)

        world = {"00": blocks}
        world_data = {
            chunk: {
                str(i.actual_pos): i.type_ for i in world[chunk]
            } for chunk in world
        }

        save(name, world_data, Player(self).dump())
        self.master.change_state("game")

    def event(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.master.running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.change_widgets("main")
                elif e.key == pygame.K_RETURN and self.current_interface == "new_world":
                    self.new_world()

        for widget in self.widgets:
            widget.event(events)

    def render(self, screen):
        # what is this line for??? just use screen.fill dumbness.
        screen.fill((0, 100, 150))

        for widget in self.widgets:
            widget.draw(screen)

        pygame.display.flip()
