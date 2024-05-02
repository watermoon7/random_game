import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, actual_pos, display_pos, size, type_, color=(255, 255, 255)):
        super().__init__()
        self.actual_pos = actual_pos
        self.size = size
        self.type_ = type_
        self.color = color

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = display_pos


