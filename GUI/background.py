import pygame
from GUI.widget import Widget, Vector, Color


class Background(Widget):
    """Basic widget"""

    def __init__(self, pos: Vector, width: int, height: int, color: Color = (255, 255, 255)) -> None:
        super().__init__(pos, width, height)
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget."""
        pygame.draw.rect(screen, self.color, self.rect)
