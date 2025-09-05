import pygame
import random
from data.classes.settings import TILE_SIZE

class UI:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

        # Шейк сердечек
        self.hp_shake_timer = 0
        self.hp_shake_offset = [0 for _ in range(player.max_hp)]
        self.hp_shake_cooldown = 360  # 6 секунд * 60 FPS
        self.hp_shake_progress = 0

        # Частицы разрушения
        self.damage_particles = []

        # Дрожание всех сердечек при уроне
        self.damage_shake_timer = 0

    def spawn_damage_particles(self, index):
        center_x = 20 + index * 30
        center_y = 20
        for _ in range(10):
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            lifetime = random.randint(20, 40)
            self.damage_particles.append([center_x, center_y, dx, dy, lifetime])

    def update(self):
        if self.damage_shake_timer > 0:
            for i in range(self.player.max_hp):
                self.hp_shake_offset[i] = random.randint(-3, 3)
            self.damage_shake_timer -= 1
        else:
            self.hp_shake_timer += 1
            if self.hp_shake_timer >= self.hp_shake_cooldown:
                self.hp_shake_timer = 0
                self.hp_shake_progress = 20
            if self.hp_shake_progress > 0:
                for i in range(self.player.max_hp):
                    self.hp_shake_offset[i] = random.randint(-1, 1)
                self.hp_shake_progress -= 1
            else:
                self.hp_shake_offset = [0 for _ in range(self.player.max_hp)]

        for p in self.damage_particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
        self.damage_particles = [p for p in self.damage_particles if p[4] > 0]

    def draw_heart(self, surface, x, y, color):
        pygame.draw.circle(surface, color, (x - 5, y), 7)
        pygame.draw.circle(surface, color, (x + 5, y), 7)
        pygame.draw.polygon(surface, color, [(x - 12, y), (x, y + 12), (x + 12, y)])

    def draw(self, screen):
        for i in range(self.player.max_hp):
            x = 20 + i * 30 + self.hp_shake_offset[i]
            y = 20 + self.hp_shake_offset[i]
            if i < self.player.hp:
                self.draw_heart(screen, x, y, (255, 0, 0))
            else:
                self.draw_heart(screen, x, y, (100, 0, 0))

        # 👞 Отображаем таймер зелья скорости
        if self.player.speed_boost_timer > 0:
            seconds = self.player.speed_boost_timer // 60
            font = pygame.font.SysFont(None, 28)
            text = font.render(f"Скорость: {seconds}s", True, (255, 255, 255))
            screen.blit(text, (20, 50))

        for p in self.damage_particles:
            pygame.draw.circle(screen, (255, 0, 0), (int(p[0]), int(p[1])), 2)

    def trigger_damage_effects(self):
        self.damage_shake_timer = 15
