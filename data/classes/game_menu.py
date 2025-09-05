import pygame

class GameMenu:
    def __init__(self):
        self.options = ["Продолжить","Главное меню"] # "Сохранить", "Загрузить", 
        self.selected_index = 0
        self.visible = False
        self.growth_progress = 0

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.growth_progress = 0

    def move_selection(self, dx, dy):
        if not self.visible:
            return
        self.selected_index = (self.selected_index + dy) % len(self.options)

    def select(self):
        if not self.visible:
            return None
        return self.options[self.selected_index]

    def draw(self, surface):
        if not self.visible:
            return

        if self.growth_progress < 1:
            self.growth_progress += 0.1
        else:
            self.growth_progress = 1

        width = int(surface.get_width() * 0.6 * self.growth_progress)
        height = int(surface.get_height() * 2 // 3 * self.growth_progress)
        x = (surface.get_width() - width) // 2
        y = (surface.get_height() - height) // 2

        bg = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 200), (0, 0, width, height), border_radius=12)
        surface.blit(bg, (x, y))

        if self.growth_progress < 0.95:
            return

        font = pygame.font.SysFont(None, 40)
        item_height = height // (len(self.options) + 1)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (220, 220, 220)
            text = font.render(option, True, color)
            tx = x + width // 2 - text.get_width() // 2
            ty = y + item_height * (i + 1) - text.get_height() // 2
            surface.blit(text, (tx, ty))

    def handle_input(self, events):
        if not self.visible:
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_selection(0, -1)
                elif event.key == pygame.K_s:
                    self.move_selection(0, 1)
                elif event.key == pygame.K_RETURN:
                    return self.select()
        return None