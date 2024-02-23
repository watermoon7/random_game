import pygame, sys


class TextInput:
    def __init__(self, master, pos, width, height, default_text="", font_size=20):
        self.master = master
        self.pos = pos
        self.width = width
        self.height = height
        self.text = default_text
        self.font_size = font_size

        self.active = False
        self.hover = False
        self.rect = pygame.Rect(*pos, width, height)

        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        self.text_rect = self.text_surface.get_rect(center=(pos[0] + width / 2, pos[1] + height / 2))

    def event(self, events):
        pos = pygame.mouse.get_pos()
        collided = self.rect.collidepoint(pos)
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if collided:
                    self.active = True
                else:
                    self.active = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                  self.text = self.text[:-1]

                if self.active:
                    char = e.unicode
                    if char.isalnum() or char in [" "]:
                            self.text += e.unicode

                self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
                self.text_rect = self.text_surface.get_rect(center=(self.pos[0] + self.width / 2, self.pos[1] + self.height / 2))

        if collided:
            self.hover = True
        else:
            self.hover = False


    def draw(self):
        if self.active:
            pygame.draw.rect(self.master.screen, pygame.Color("lightgreen"), self.rect)
        elif self.hover:
            pygame.draw.rect(self.master.screen, pygame.Color("green"), self.rect)
        else:
            pygame.draw.rect(self.master.screen, pygame.Color("forestgreen"), self.rect)

        if self.text is not None:
            self.master.screen.blit(self.text_surface, self.text_rect)


    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
