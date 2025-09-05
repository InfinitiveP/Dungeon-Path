import pygame

class MainMenu:
    def __init__(self):
        self.options = ["Играть", "Настройки", "Об Игре", "Выход"]
        self.selected_index = 0
        self.visible = True

    def move_selection(self, direction):
        if not self.visible:
            return
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select(self):
        if not self.visible:
            return None
        return self.options[self.selected_index]

    def draw(self, surface):
        if not self.visible:
            return

        surface.fill((20, 20, 20))
        font = pygame.font.SysFont(None, 48)
        title_font = pygame.font.SysFont(None, 64)
        screen_center_x = surface.get_width() // 2
        screen_center_y = surface.get_height() // 2

        title = title_font.render("Главное меню", True, (255, 255, 255))
        surface.blit(title, (screen_center_x - title.get_width() // 2, screen_center_y - 150))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            text = font.render(option, True, color)
            surface.blit(text, (screen_center_x - text.get_width() // 2, screen_center_y - 30 + i * 60))
        # Подсказка по управлению
        help_font = pygame.font.SysFont(None, 24)
        help_text = help_font.render("Навигация: AWSD  |  Кнопка действия: ENTER", True, (150, 150, 150))
        surface.blit(help_text, (40, screen_center_y))

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_selection(-1)
                elif event.key == pygame.K_s:
                    self.move_selection(1)
                elif event.key == pygame.K_RETURN:
                    return self.select()
        return None
