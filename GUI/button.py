import pygame
from GUI.utils import lighten_color
from GUI.widget import TextWidget, Vector, Color
from typing import List

pygame.font.init()


class Button(TextWidget):
    """Button widget"""

    def __init__(self, pos: Vector, width: int, height: int, text: str = None, font_size: int = 20,
                 command=None, args: List or None = None, toggle: bool = False, line_length: int = 30,
                 default_color: Color = None, toggle_color: Color = None, toggled: bool = False,
                 do_hover_color: bool = True, do_pressed_color: bool = True, round_edges: int = 0,
                 center_text: bool = True, text_color: Color = (255, 255, 255)) -> None:
        super().__init__(pos, width, height, text, font_size, center_text, line_length, text_color)
        self.command = command
        self.args = args if isinstance(args, (list, tuple)) else None if args is None else [args]
        self.toggle = toggle
        self.do_hover_color = do_hover_color
        self.do_pressed_color = do_pressed_color
        self.round_edges = round_edges

        self.default_color = pygame.Color('cornflowerblue') if default_color is None else default_color
        self.toggled_color = pygame.Color('mediumseagreen') if toggle_color is None else toggle_color

        self.pressed = False
        self.hover = False
        self.toggled = toggled

    def event(self, events: List[pygame.event.Event], clip_rect: pygame.Rect = None) -> None:
        """Handles events."""
        pos = pygame.mouse.get_pos()
        condition = True if clip_rect is None else clip_rect.collidepoint(pos)
        if self.rect.collidepoint(pos) and condition:
            self.hover = True
            if any([e.type == pygame.MOUSEBUTTONUP and e.button == 1 for e in events]):
                self.toggled = not self.toggled
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

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget."""
        if self.toggled and self.toggle:
            color = self.toggled_color
        else:
            color = self.default_color

        if self.pressed and self.do_pressed_color:
            color = lighten_color(color, amount=100)
        elif self.hover and self.do_hover_color:
            color = lighten_color(color, amount=50)

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=self.round_edges
        )
        self.draw_text(screen)
