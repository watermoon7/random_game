from typing import List, Tuple
from GUI.utils import split_words_into_lines
import pygame
pygame.font.init()

type Vector = List[int, int] or Tuple[int, int]
type Color = Tuple[int, int, int] or pygame.Color


"""
In this module, there are widget base classes
Widget - the base class for all widgets
TextWidget - the base class for all widgets with text
WidgetContainer - base class for widgets which can contain other widgets
"""


class Widget:
    """Base class for all widgets."""

    def __init__(self, pos: Vector, width: int, height: int) -> None:
        self.original_pos = pos
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(*pos, width, height)

    def event(self, events: List[pygame.event.Event], clip_rect: pygame.Rect = None) -> None:
        """Handles events."""
        ...

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the widget."""
        ...

    def update_pos(self) -> None:
        """Used to update the position of pygame objects in the widget."""
        self.rect = pygame.Rect(*self.pos, self.width, self.height)

    def reset_pos(self) -> None:
        """Resets the position of the widget."""
        self.pos = self.original_pos
        self.update_pos()

    def set_pos(self, new_pos: Vector) -> None:
        """Used to set the position of the widget."""
        self.pos = new_pos
        self.update_pos()

    def translate(self, translation: Vector) -> None:
        """Translates the widget"""
        self.pos = (self.pos[0] + translation[0], self.pos[1] + translation[1])
        self.update_pos()


class TextWidget(Widget):

    def __init__(self, pos: Vector, width: int, height: int, text: str, font_size: int,
                 center_text: bool, line_length: int, text_color: Color) -> None:
        super().__init__(pos, width, height)
        self.text = str(text)
        self.font_size = font_size
        self.font = pygame.font.Font("assets/fonts/Roboto/Roboto-Medium.ttf", font_size)
        self.center_text = center_text
        self.line_length = line_length
        self.text_color = text_color

        self.render_text()

    def render_text(self):
        """Method to render the text on the widget
        Splits the text into lines, and then aligns the text within a text rectangle."""
        self.lines = [self.font.render(line, True, self.text_color)
                      for line in split_words_into_lines(self.text.split(), self.line_length)]
        if self.center_text:
            self.line_rects = [
                line.get_rect(
                    center=(self.pos[0] + self.width / 2, self.pos[1] + (i+1) * self.height / (len(self.lines)+1))
                ) for i, line in enumerate(self.lines)
            ]
        else:
            self.line_rects = [
                line.get_rect(
                    midleft=(self.pos[0], self.pos[1] + (i+1) * self.height / (len(self.lines)+1))
                ) for i, line in enumerate(self.lines)
            ]

    def draw_text(self, screen: pygame.Surface) -> None:
        """Method to draw the text on the widget"""
        for text_surface, text_rect in zip(self.lines, self.line_rects):
            screen.blit(text_surface, text_rect)

    def update_pos(self) -> None:
        """Used to update the position of pygame objects in the widget."""
        self.rect = pygame.Rect(*self.pos, self.width, self.height)
        self.render_text()

    def get_text(self) -> str:
        """Getter method to get the text of the widget"""
        return self.text

    def set_text(self, text: str) -> None:
        """Setter method to set the text of the widget"""
        self.text = text
        self.render_text()


class WidgetContainer(Widget):
    """An object that can contain multiple widgets"""

    def __init__(self, pos: Vector, width: int, height: int, margin: Tuple[int, int],
                 background_color: Color = (255, 255, 255)) -> None:
        super().__init__(pos, width, height)
        self.items = []
        self.margin = margin
        self.background_color = background_color

    def add_item(self, item: Widget, relative_pos: Vector) -> None:
        """For adding widgets to the container"""
        pos = (
            self.pos[0] + relative_pos[0],
            self.pos[1] + relative_pos[1]
        )
        item.set_pos(pos)
        self.items.append(item)

    def remove_item(self, item: Widget) -> None:
        """For removing widgets from the container"""
        try:
            self.items.remove(item)
        except ValueError as exception:
            print(f"Item: {item} not found. Error: {exception}")

    def event(self, events: List[pygame.event.Event], clip_rect: pygame.Rect = None) -> None:
        """Handles pygame events."""
        for item in self.items:
            item.event(events, clip_rect=self.rect if clip_rect is None else clip_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget and all its items."""
        pygame.draw.rect(screen, self.background_color, self.rect)

        for item in self.items:
            item.draw(screen)

    def update_pos(self) -> None:
        """Used to update the position of pygame objects in the widget."""
        self.rect = pygame.Rect(*self.pos, self.width, self.height)
        for item in self.items:
            item.update_pos()

    def reset_pos(self) -> None:
        """Resets the position of the widget."""
        self.pos = self.original_pos
        self.update_pos()
        for item in self.items:
            item.reset_pos()

    def set_pos(self, new_pos: Vector) -> None:
        """Used to set the position of the widget."""
        translation = (-(self.pos[0] - new_pos[0]), -(self.pos[1] - new_pos[1]))
        self.translate(translation)

    def translate(self, translation: Vector) -> None:
        """Translates the widget"""
        self.pos = (self.pos[0] + translation[0], self.pos[1] + translation[1])
        self.update_pos()
        for item in self.items:
            item.translate(translation)
