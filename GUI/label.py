import pygame
from GUI.widget import TextWidget, Vector, Color
pygame.font.init()


class Label(TextWidget):
    """Simple text display widget"""

    def __init__(self, pos: Vector, width: int, height: int, text: str, font_size: int = 20,
                 background_color: Color = None, center_text: bool = True, line_length: int = 30,
                 text_color: Color = (255, 255, 255)) -> None:
        super().__init__(pos, width, height, text, font_size, center_text, line_length, text_color)
        self.background_color = background_color

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget."""
        if self.background_color is not None:
            pygame.draw.rect(screen, self.background_color, self.rect)
        self.draw_text(screen)
