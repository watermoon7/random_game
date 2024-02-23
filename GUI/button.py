import pygame
from utils import add
pygame.font.init()


class Button:
    def __init__(self, master, pos, width, height, text=None, command=None, args=None, font_size=20):
        self.master = master
        self.original_pos = pos
        self.pos = pos
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text = text
        self.command = command
        self.args = args

        self.default_color = pygame.Color('cornflowerblue')
        self.hover_color = pygame.Color('lightblue')
        self.pressed_color = pygame.Color('turquoise')
        self.pressed = False
        self.hover = False

        self.font = pygame.font.Font("assets/fonts/Roboto/Roboto-Medium.ttf", font_size)
        self.text_surface = self.font.render(text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect(center=(pos[0] + width/2, pos[1] + height/2))

        self.rect = pygame.Rect((*self.pos, self.width, self.height))

    def event(self, events):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            if any([e.type == pygame.MOUSEBUTTONUP and e.button == 1 for e in events]):
                if self.command is not None:
                    if self.args is None:
                        self.command()
                    else:
                        self.command(*self.args)
            else:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                else:
                    self.pressed = False
        else:
            self.hover = False
            self.pressed = False


    def draw(self):
        if self.pressed:
            color = self.pressed_color
        elif self.hover:
            color = self.hover_color
        else:
            color = self.default_color

        pygame.draw.rect(
            self.master.screen,
            color,
            self.rect
        )
        if self.text is not None:
            self.master.screen.blit(self.text_surface, self.text_rect)

    def translate(self, vector):
        self.pos = add(self.pos, vector)
        self.x, self.y = self.pos

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect(center=(self.pos[0] + self.width/2, self.pos[1] + self.height/2))

        self.rect = pygame.Rect((*self.pos, self.width, self.height))

    def set_default_position(self):
        self.pos = self.original_pos
        self.x, self.y = self.pos

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect(center=(self.pos[0] + self.width / 2, self.pos[1] + self.height / 2))

        self.rect = pygame.Rect((*self.pos, self.width, self.height))

    def set_pos(self, pos):
        self.pos = pos
        self.x, self.y = self.pos

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2)

        self.rect = pygame.Rect((*self.pos, self.width, self.height))


