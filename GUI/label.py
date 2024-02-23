import pygame, sys


class Label:
    def __init__(self, master, pos, width, height, text, font_size=20):
        self.master = master
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

        self.rect = pygame.Rect(*pos, width, height)

        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect(center=(pos[0] + width / 2, pos[1] + height / 2))

    def event(self, events):
        ...

    def draw(self):
        pygame.draw.rect(self.master.screen, pygame.Color("lightyellow4"), self.rect)
        self.master.screen.blit(self.text_surface, self.text_rect)


    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text

