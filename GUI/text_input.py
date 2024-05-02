import pygame
from GUI.widget import TextWidget, Vector, Color
from typing import List

pygame.font.init()


class TextInput(TextWidget):
    def __init__(self, pos: Vector, width: int, height: int, default_text: str = "",
                 font_size: int = 20, center_text: bool = True, input_characters: str or List = None,
                 line_length: int = 30, text_color: Color = (255, 255, 255)) -> None:
        super().__init__(pos, width, height, default_text, font_size, center_text, line_length, text_color)
        self.input_characters = input_characters

        self.active = False
        self.hover = False
        self.rect = pygame.Rect(*pos, width, height)

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        if center_text:
            self.text_rect = self.text_surface.get_rect(center=(pos[0] + width / 2, pos[1] + height / 2))
        else:
            self.text_rect = self.text_surface.get_rect(midleft=(pos[0], pos[1] + height / 2))

    def event(self, events: List[pygame.event.Event], clip_rect: pygame.Rect = None) -> None:
        """Handles events"""
        pos = pygame.mouse.get_pos()
        collided = self.rect.collidepoint(pos)
        condition = True if clip_rect is None else clip_rect.collidepoint(pos)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and condition:
                if collided:
                    self.active = True
                else:
                    self.active = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.active = False

                if self.active:
                    if e.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        char = e.unicode
                        if self.input_characters is None:
                            self.text += e.unicode
                        else:
                            if char in self.input_characters:
                                self.text += e.unicode

                self.render_text()

        if collided:
            self.hover = True
        else:
            self.hover = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget"""
        if self.active:
            pygame.draw.rect(screen, pygame.Color("lightgreen"), self.rect)
        elif self.hover:
            pygame.draw.rect(screen, pygame.Color("green"), self.rect)
        else:
            pygame.draw.rect(screen, pygame.Color("forestgreen"), self.rect)

        self.draw_text(screen)
