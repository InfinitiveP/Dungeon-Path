import os
import pygame
import sys
import configparser
from data.classes import settings

class SettingsMenu:
    def __init__(self):
        self.options = ["1280x720", "1920x1080"]
        self.resolutions = [(1280, 720), (1920, 1080)]
        self.selected_index = 0
        self.visible = False

    def move_selection(self, direction):
        if not self.visible:
            return
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select(self):
        if not self.visible:
            return

        selected_resolution = self.resolutions[self.selected_index]

        # Обновляем config.cfg
        config_path = "data/config.cfg"
        import configparser
        config = configparser.ConfigParser()
        config.read(config_path)

        config["graphics"]["WIDTH"] = str(selected_resolution[0])
        config["graphics"]["HEIGHT"] = str(selected_resolution[1])

        with open(config_path, "w") as configfile:
            config.write(configfile)

        # Перезапускаем игру
        pygame.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def draw(self, surface):
        if not self.visible:
            return

        surface.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 48)
        title_font = pygame.font.SysFont(None, 64)
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        title = title_font.render("Настройки", True, (255, 255, 255))
        surface.blit(title, (center_x - title.get_width() // 2, center_y - 150))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            text = font.render(option, True, color)
            surface.blit(text, (center_x - text.get_width() // 2, center_y - 30 + i * 60))

        help_font = pygame.font.SysFont(None, 24)
        help_text = help_font.render("Навигация: AWSD  |  Выбрать: ENTER", True, (150, 150, 150))
        surface.blit(help_text, (40, center_y))

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_selection(-1)
                elif event.key == pygame.K_s:
                    self.move_selection(1)
                elif event.key == pygame.K_RETURN:
                    return self.select()
                elif event.key == pygame.K_ESCAPE:
                    return "main_menu"
        return None
