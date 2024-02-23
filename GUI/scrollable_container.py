import pygame


class ScrollableContainer:
    def __init__(self, master, pos, width, height, item_height, separation=0, margin=(0, 0)):
        # item height is the height of each item. make sure they are all the same idot
        self.master = master
        self.pos = pos
        self.width = width
        self.height = height
        self.item_height = item_height
        self.separation = separation
        if isinstance(margin, int):
            self.margin = (margin, margin)
        else:
            self.margin = margin

        self.items = []
        self.offset = 0

        self.rect = pygame.Rect(pos, (width, height))

    def add_item(self, item):
        pos = (self.pos[0] + self.margin[0],
               self.pos[1] + self.margin[1] + len(self.items) * (self.item_height + self.separation))
        item.set_pos(pos)
        self.items.append(item)

    def event(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll(event.y)  # Scroll up or down

        # Pass events to each item for their individual event handling
        for item in self.items:
            item.event(events)

    def scroll(self, direction):
        self.offset += direction * 10  # Adjust the scroll speed as necessary
        self.offset = min(self.offset, 0)  # Prevent scrolling up beyond the first item
        max_offset = -(len(self.items) * (self.item_height + self.separation) - self.height)
        self.offset = max(self.offset, max_offset)  # Prevent scrolling down beyond the last item

        # Update the positions of all items based on the new scroll offset
        for i, item in enumerate(self.items):
            item_pos = (self.pos[0], self.pos[1] + i * (self.item_height + self.separation) + self.offset)
            item.set_pos(item_pos)

    def draw(self):
        # Optionally create a surface for the container and clip to prevent drawing outside the container bounds
        clip_rect = pygame.Rect(self.pos, (self.width, self.height))
        self.master.screen.set_clip(clip_rect)
        self.master.screen.fill((0, 100, 150))

        # Draw the container background (optional)
        pygame.draw.rect(self.master.screen, pygame.Color('grey'), self.rect)

        # Draw each item
        for item in self.items:
            item.draw()

        # Reset the clipping
        self.master.screen.set_clip(None)
