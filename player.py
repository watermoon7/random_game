import pygame
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.multiplier = self.master.cell_size/30
        self.width = int(self.master.cell_size * 0.9)
        self.height = int(self.master.cell_size * 1.5)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color('darkolivegreen1'))
        self.rect = self.image.get_rect()

        self.friction_coefficient = 0.8
        self.air_resistance_coefficient = 0.91

        self.reset()

    def __repr__(self):
        return f"Pos: {self.pos}\nVelocity: {self.velocity}\nAcceleration: {self.acceleration}"

    def move(self, dt, blocks):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration[0] = -self.speed
        elif keys[pygame.K_d]:
            self.acceleration[0] = self.speed

        if keys[pygame.K_SPACE] and self.jump and self.grounded:
            self.jump = False
            self.velocity[1] = -1200 * self.multiplier

        self.pos[0] += dt*self.velocity[0] + 0.5*(dt**2)*self.acceleration[0]
        self.rect.x = self.pos[0]

        b = pygame.sprite.spritecollide(self, blocks, False)
        if b:
            if self.velocity[0] > 0:  # going right
                self.pos[0] = b[0].rect.left - self.width
                self.jump = True
            else:  # going left
                self.pos[0] = b[0].rect.right
            self.velocity[0] = 0
            self.acceleration[0] = 0
            self.rect.x = self.pos[0]

        self.pos[1] += dt*self.velocity[1] + 0.5*(dt**2)*self.acceleration[1]
        self.rect.y = self.pos[1]

        b = pygame.sprite.spritecollide(self, blocks, False)
        if b:
            if self.velocity[1] > 0:  # going down
                self.pos[1] = b[0].rect.top - self.height
                self.jump = True
            else:  # going up
                self.pos[1] = b[0].rect.bottom
            self.rect.y = self.pos[1]
            self.velocity[1] = 0
            self.grounded = True
            self.acceleration[0] = self.acceleration[0] * self.friction_coefficient
        else:
            self.grounded = False


        self.velocity = self.air_resistance_coefficient * (self.velocity + dt*self.acceleration)
        self.acceleration[0] = self.acceleration[0] * self.air_resistance_coefficient
        if self.velocity[0] > 0:
            self.velocity[0] = min(self.velocity[0], 400 * self.multiplier)
        else:
            self.velocity[0] = max(self.velocity[0], -400 * self.multiplier)

        if self.velocity[1] > 0:
            self.velocity[1] = min(self.velocity[1], 1000 * self.multiplier)
        else:
            self.velocity[1] = max(self.velocity[1], -1000 * self.multiplier)

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def reposition(self, pos):
        self.pos = pos
        self.rect.x, self.rect.y = pos

    def dump(self):
        return {
            "pos": list(self.pos),
            "velocity": list(self.velocity),
            "acceleration": list(self.acceleration),
            "jump": self.jump,
            "grounded": self.grounded,
            "speed": self.speed,
            "inventory": self.inventory,
        }

    def load(self, d):
        self.pos = np.array(d["pos"])
        self.velocity =  np.array(d["velocity"])
        self.acceleration = np.array(d["acceleration"])
        self.jump = d["jump"]
        self.grounded = d["grounded"]
        self.speed = d["speed"]
        self.inventory = d["inventory"]

    def reset(self):
        self.pos = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.acceleration = np.array([0, 2400], dtype=float) * self.multiplier
        self.jump = False
        self.grounded = False
        self.speed = 1650 * self.multiplier
        self.inventory = {}

