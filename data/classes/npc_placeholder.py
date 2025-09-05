import pygame
from data.classes.enemy_logic import EnemyLogic
from data.classes.settings import TILE_SIZE
from data.classes.models import Models
from data.classes.animations import Animations

show_colliders = False

class NPCPlaceholder(EnemyLogic):
    def __init__(self, x, y, mode, messages, model_name="scarecrow"):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE * 2)
        self.triggered = False
        self.trigger_distance = 2 * TILE_SIZE
        self.messages = messages if isinstance(messages, list) else [messages]
        self.current_message_index = 0
        self.is_talking = False
        self.mode = mode

        self.growth_progress = 0

        # Для режима 2
        self.displayed_text = ''
        self.text_progress = 0
        self.text_speed = 3  # сколько кадров на одну букву
        self.text_timer = 0

        # Загружаем модель и анимацию
        model = Models.environment_models[model_name]
        self.animations = Animations(
            model["path"],
            custom_settings=model.get("custom_settings"),
            base_direction=model.get("base_direction", 1) if "base_direction" in model else 1
        )
        self.animations.set_animation('idle')

    def update(self, player, tiles):
        self.level_tiles = tiles

        distance_x = abs(self.rect.centerx - player.rect.centerx)
        distance_y = abs(self.rect.centery - player.rect.centery)

        if distance_x <= self.trigger_distance and distance_y <= self.trigger_distance:
            if not self.triggered:
                # только что вошёл в зону триггера
                if self.mode == 2:
                    self.displayed_text = ''
                    self.text_progress = 0
                    self.text_timer = 0
            self.triggered = True

            if self.growth_progress < 1:
                self.growth_progress += 0.1
        else:
            if self.triggered:
                # только что вышел из зоны триггера
                if self.mode == 2:
                    self.displayed_text = ''
                    self.text_progress = 0
                    self.text_timer = 0

            self.triggered = False
            self.is_talking = False
            self.current_message_index = 0

            if self.growth_progress > 0:
                self.growth_progress -= 0.1

        self.growth_progress = max(0, min(self.growth_progress, 1))

        # Обновляем печать текста только в режиме 2
        if self.mode == 2 and self.triggered and self.growth_progress >= 1:
            if self.text_progress < len(self.messages[self.current_message_index]):
                self.text_timer += 1
                if self.text_timer >= self.text_speed:
                    self.text_timer = 0
                    self.text_progress += 1
                    self.displayed_text = self.messages[self.current_message_index][:self.text_progress]

    def draw(self, screen, offset_x, offset_y):
        frame = self.animations.get_image()
        if frame:
            size, draw_offset = self.animations.get_current_animation_settings()
            frame = pygame.transform.scale(frame, size)

            screen.blit(frame, (
                self.rect.x + draw_offset[0] - offset_x,
                self.rect.y + draw_offset[1] - offset_y
            ))
        self.animations.update()

        if self.growth_progress > 0:
            self.draw_npc_text_box(screen, offset_x, offset_y)
        
        if show_colliders:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height),
                2
            )

    def draw_npc_text_box(self, screen, offset_x, offset_y):
        font = pygame.font.SysFont(None, 24)
        max_width = 200

        full_text = self.messages[self.current_message_index] if self.mode != 2 else self.displayed_text
        text_height = font.get_height()

        # Создаём список символов
        words = full_text.split(" ")
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            width, _ = font.size(test_line)
            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        total_height = text_height * len(lines) + 20
        max_line_width = max((font.size(line)[0] for line in lines), default=0)

        full_box_width = max_line_width + 20
        full_box_height = total_height

        current_width = int(full_box_width * self.growth_progress)
        current_height = int(full_box_height * self.growth_progress)

        center_x = self.rect.centerx - offset_x
        box_x = center_x - current_width // 2
        box_y = self.rect.top - full_box_height - 20 - offset_y + (full_box_height - current_height) // 2

        s = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))

        corner_size = 4
        if current_width > 2 * corner_size and current_height > 2 * corner_size:
            pygame.draw.rect(s, (0, 0, 0, 0), (0, 0, corner_size, corner_size))
            pygame.draw.rect(s, (0, 0, 0, 0), (current_width - corner_size, 0, corner_size, corner_size))
            pygame.draw.rect(s, (0, 0, 0, 0), (0, current_height - corner_size, corner_size, corner_size))
            pygame.draw.rect(s, (0, 0, 0, 0), (current_width - corner_size, current_height - corner_size, corner_size, corner_size))

        screen.blit(s, (box_x, box_y))

        if self.growth_progress > 0.9:
            # Посимвольная отрисовка
            symbol_index = 0
            for line_index, line in enumerate(lines):
                x_offset = 0
                for char in line:
                    if self.mode == 2 and symbol_index >= self.text_progress:
                        break  # не рисуем ещё не допечатанные буквы

                    letter_surface = font.render(char, True, (255, 255, 255))

                    letter_x = center_x - max_line_width // 2 + x_offset
                    letter_y = box_y + 10 + line_index * text_height

                    # Только одна активная буква дрожит
                    if self.mode == 2:
                        if symbol_index == self.text_progress - 1 and self.text_progress < len(self.messages[self.current_message_index]):
                            import random
                            shake_x = random.randint(-1, 1)
                            shake_y = random.randint(-1, 1)
                            letter_x += shake_x
                            letter_y += shake_y

                    screen.blit(letter_surface, (letter_x, letter_y))
                    x_offset += letter_surface.get_width()
                    symbol_index += 1

    def interact(self):
        if not self.triggered:
            return

        self.is_talking = True
        self.current_message_index += 1
        if self.current_message_index >= len(self.messages):
            self.current_message_index = 0

        self.growth_progress = 0  # Сброс анимации роста при переключении текста

        # Сброс печатания для режима 2
        self.displayed_text = ''
        self.text_progress = 0
        self.text_timer = 0
