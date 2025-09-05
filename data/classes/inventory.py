import pygame
from data.classes.settings import TILE_SIZE, WIDTH, HEIGHT

class Inventory:
    def __init__(self, rows=3, cols=5):
        self.rows = rows
        self.cols = cols
        self.slots = [[0 for _ in range(cols)] for _ in range(rows)]
        self.selected_row = 0
        self.selected_col = 0
        self.visible = False
        self.growth_progress = 0

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.growth_progress = 0  # запускаем анимацию открытия

    def move_selection(self, dx, dy):
        if not self.visible:
            return
        self.selected_row = (self.selected_row + dy) % self.rows
        self.selected_col = (self.selected_col + dx) % self.cols

    def use_selected_item(self, player=None):
        if not self.visible:
            return

        item = self.slots[self.selected_row][self.selected_col]
        print(f"Используется предмет: {item}")

        if item == "heart" and player:
            player.hp += 1
            print("+1 HP! Текущее HP:", player.hp)
            self.slots[self.selected_row][self.selected_col] = 0

        if item == "speed" and player:
            player.speed *= 2
            player.speed_boost_timer = 60 * 60  # 1 минута (60 FPS)
            print("Зелье скорости активировано!")
            self.slots[self.selected_row][self.selected_col] = 0

    def add_item(self, item):
        print(f"Пытаемся добавить предмет: {item}")
        for row in range(self.rows):
            for col in range(self.cols):
                if self.slots[row][col] == 0:
                    self.slots[row][col] = item
                    print(f"✅ Предмет {item} добавлен в ячейку ({row}, {col})")
                    return True
        print("Нет свободного места в инвентаре!")
        return False

    def draw_heart(self, surface, x, y):
        pygame.draw.circle(surface, (255, 0, 0), (x - 5, y), 7)
        pygame.draw.circle(surface, (255, 0, 0), (x + 5, y), 7)
        pygame.draw.polygon(surface, (255, 0, 0), [(x - 12, y), (x, y + 12), (x + 12, y)])

    def draw_boot(self, surface, x, y):
        pygame.draw.rect(surface, (80, 80, 80), (x - 12, y + 8, 24, 6))
        pygame.draw.rect(surface, (160, 100, 60), (x - 10, y - 10, 20, 18), border_radius=4)
        pygame.draw.rect(surface, (180, 120, 80), (x - 6, y - 10, 12, 6), border_radius=2)
        for i in range(3):
            pygame.draw.line(surface, (50, 30, 20), (x - 6, y - 4 + i * 4), (x + 6, y - 4 + i * 4), 1)


    def draw(self, surface):
        if not self.visible:
            return

        # Анимация появления
        if self.growth_progress < 1:
            self.growth_progress += 0.1
        else:
            self.growth_progress = 1

        inv_width = int((WIDTH * 2 // 3) * self.growth_progress)
        inv_height = int((HEIGHT * 2 // 3) * self.growth_progress)
        start_x = (WIDTH - inv_width) // 2
        start_y = (HEIGHT - inv_height) // 2

        # Полупрозрачный черный фон с мягким скруглением
        s = pygame.Surface((inv_width, inv_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        pygame.draw.rect(s, (0, 0, 0, 200), (0, 0, inv_width, inv_height), border_radius=12)
        surface.blit(s, (start_x, start_y))

        if self.growth_progress < 0.95:
            return  # Не рисуем содержимое до завершения анимации

        cell_w = inv_width // self.cols
        cell_h = inv_height // self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                x = start_x + col * cell_w
                y = start_y + row * cell_h

                # Фон ячейки — черный, граница — светло-серая
                pygame.draw.rect(surface, (30, 30, 30), (x, y, cell_w - 2, cell_h - 2), border_radius=6)
                pygame.draw.rect(surface, (150, 150, 150), (x, y, cell_w - 2, cell_h - 2), 1, border_radius=6)

                # Выделение текущей ячейки
                if row == self.selected_row and col == self.selected_col:
                    pygame.draw.rect(surface, (255, 255, 0), (x, y, cell_w - 2, cell_h - 2), 3, border_radius=6)

                # Отображение предмета
                item = self.slots[row][col]
                if item == "heart":
                    self.draw_heart(surface, x + cell_w // 2, y + cell_h // 2)
                elif item == "speed":
                    self.draw_boot(surface, x + cell_w // 2, y + cell_h // 2)
                elif item != 0:
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(item), True, (255, 255, 255))
                    surface.blit(text, (x + 5, y + 5))

