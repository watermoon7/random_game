import pygame
import numpy as np
from player import Player
from world.save import save
from world.load import load
from world.block import Block
from states.gamestate import GameState


class GameLoop(GameState):
    def __init__(self, master):
        super().__init__(master)
        self.background_color = pygame.Color('lightskyblue1')
        self.chunks = {}
        self.loaded_chunks = []

        self.player = Player(self)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)

    def save(self):
        world_name = self.master.loaded_level
        world_data = {chunk: {str(i.actual_pos): i.type_ for i in self.chunks[chunk]} for chunk in self.chunks}

        save(world_name, world_data, self.player.dump())

    def load(self):
        self.chunks = {}
        self.loaded_chunks = ["00"]

        data = load(self.master.loaded_level)
        world = data["world"]
        player = data["player"]
        self.player.load(player)

        for chunk in world:
            blocks = pygame.sprite.Group()
            for pos, type_ in world[chunk].items():
                if type_ == "grass":
                    x, y = list(map(int, pos[1:-1].split(", ")))
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
            self.chunks[chunk] = blocks

    def start(self):
        self.load()

    def stop(self):
        self.save()

    def event(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.master.running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.master.change_state("pause")
                elif e.key == pygame.K_r:
                    self.player.reposition([0, 0])
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()

                if mouse[0]:
                    for chunk in self.loaded_chunks:
                        for block in self.chunks[chunk]:
                            if block.rect.collidepoint(pos):
                                self.chunks["00"].remove(block)
                elif mouse[2]:
                    pos = [pos[0]//self.cell_size, pos[1]//self.cell_size]
                    self.chunks["00"].add(Block(pos, (pos[0] * self.cell_size, pos[1] * self.cell_size), self.cell_size, "grass", pygame.Color('springgreen3')))

    def update(self):
        for chunk in self.loaded_chunks:
            blocks = pygame.sprite.Group()
            for b in self.chunks[chunk]:
                blocks.add(b)

            self.player.move(self.master.dt, blocks)

    def render(self, screen):
        screen.fill(self.background_color)
        for chunk in self.loaded_chunks:
            self.chunks[chunk].draw(screen)
        self.sprites.draw(screen)
        pygame.display.flip()
