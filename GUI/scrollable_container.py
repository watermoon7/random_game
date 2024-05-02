import pygame
from GUI.widget import Widget, WidgetContainer, Vector, Color
from typing import Tuple, List
pygame.font.init()


class ScrollableContainer(WidgetContainer):
    """Scrollable widget container"""

    def __init__(self, pos: Vector, width: int, height: int, item_height: int,
                 separation: int = 0, margin: Tuple[int, int] or int = (0, 0),
                 background_color: Color = (255, 255, 255)):
        margin = (margin, margin) if isinstance(margin, int) else tuple(margin)
        super().__init__(pos, width, height, margin, background_color)

        self.item_height = item_height
        self.separation = separation
        self.scroll_offset = 0

    def add_item(self, item: Widget, relative_pos: Vector or None = None) -> None:
        """For adding widgets to the container"""
        if relative_pos is None:
            pos = (
                self.pos[0] + self.margin[0],
                self.pos[1] + self.margin[1] + len(self.items) * (self.item_height + self.separation)
            )
        else:
            pos = (
                self.pos[0] + relative_pos[0],
                self.pos[1] + relative_pos[1]
            )
        item.set_pos(pos)
        self.items.append(item)

    def event(self, events: List[pygame.event.Event], clip_rect: pygame.Rect = None) -> None:
        """Handles pygame events."""
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll(event.y)

        for item in self.items:
            item.event(events, clip_rect=self.rect if clip_rect is None else clip_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the widget and all its items."""
        clip_rect = self.rect
        screen.set_clip(clip_rect)

        pygame.draw.rect(screen, self.background_color, self.rect)

        for item in self.items:
            item.draw(screen)

        screen.set_clip(None)

    def scroll(self, direction: int) -> None:
        """Handles the scrolling of the widgets"""
        self.scroll_offset += direction * 12
        self.scroll_offset = min(self.scroll_offset, 0)
        max_offset = self.height - (len(self.items) * self.item_height + (len(self.items) - 2) * self.separation)
        self.scroll_offset = max(self.scroll_offset, max_offset)

        for i, item in enumerate(self.items):
            item_pos = (
                self.pos[0] + self.margin[0],
                self.pos[1] + i * self.item_height + (i - 1) * self.separation + self.scroll_offset + self.margin[1]
            )
            item.set_pos(item_pos)
