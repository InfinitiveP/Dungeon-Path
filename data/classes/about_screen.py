import pygame

class AboutScreen:
    def __init__(self):
        self.visible = False
        self.selected_index = 0  # только одна кнопка: Назад

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_s]:
                    self.selected_index = 0  # всегда "Назад"
                elif event.key == pygame.K_RETURN:
                    return "Назад"
        return None

    def draw(self, surface):
        if not self.visible:
            return

        surface.fill((10, 10, 10))
        font = pygame.font.SysFont("data/fonts/RuneScape-ENA.ttf", 36)
        big_font = pygame.font.SysFont("data/fonts/RuneScape-ENA.ttf", 48)
        screen_center_x = surface.get_width() // 2

        text_lines = [
            "🕹 Проект от Infinitive",
            "Студенческий проект, с потенциалом на развитие в будущем.",
            "",
            "Сначала - простой платформер, созданный ради обучения.",
            "Сейчас - маленький мир с инвентарем, диалогами, переходами ",
            "между уровнями и механиками выживания.",
            "Это не RPG. Но и не просто платформер.",
            "Это то, что выросло само по себе - благодаря любви к деталям и ",
            "ощущению свободы в разработке.",
        ]

        for i, line in enumerate(text_lines):
            text = font.render(line, True, (200, 200, 200))
            surface.blit(text, (screen_center_x - text.get_width() // 2, 100 + i * 40))

        # Кнопка Назад — под текстом
        total_height = 100 + len(text_lines) * 40 + 40  # + отступ
        color = (255, 255, 0) if self.selected_index == 0 else (200, 200, 200)
        back_text = big_font.render("Назад", True, color)
        surface.blit(back_text, (screen_center_x - back_text.get_width() // 2, total_height))
