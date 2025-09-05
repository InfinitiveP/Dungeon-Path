import pygame
from data.classes.settings import TILE_SIZE
from data.classes.physics import apply_gravity, handle_collisions

class EnemyLogic:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE * 2)
        self.start_x = x
        self.start_y = y
        self.direction = 1
        self.speed = 2
        self.move_range = 6 * TILE_SIZE
        self.vel_y = 0
        self.on_ground = False
        self.wait_timer = 0
        self.attack_pending = False
        self.attack_progress = 0
        self.attack_distance = TILE_SIZE * 2
        self.attack_speed = 12
        self.returning_to_spawn = False
        self.damage = 1
        self.has_hit_player = False
        self.is_dead = False
        self.hp = 1
        self.blink_timer = 0
        self.blink_duration = 15  # сколько кадров будет мигать
        self.blink_frequency = 5  # как часто мигать (раз в X кадров)


        self.projectiles = []
        self.projectile_speed = 7
        self.projectile_cooldown = 0
        self.level_tiles = []

    def apply_gravity_and_collisions(self, dx, dy, tiles):
        self.vel_y = apply_gravity(self.vel_y)
        dy += self.vel_y
        self.vel_y, self.on_ground = handle_collisions(self.rect, dx, dy, self.vel_y, tiles)
        return dx, dy

    def take_damage(self, amount, attack_direction=None):
        if hasattr(self, "state") and self.state != "alive":
            return

        self.hp -= amount

        if attack_direction is not None:
            push_distance = TILE_SIZE
            push_rect = self.rect.copy()
            push_rect.x += push_distance if attack_direction > 0 else -push_distance

            if not any(tile[0] in ("floor", "barrier") and push_rect.colliderect(tile[1]) for tile in self.level_tiles):
                self.rect = push_rect

        if hasattr(self, 'animations') and 'hit' in getattr(self.animations, 'animations', {}):
            self.animations.set_animation('hit')

        if self.hp <= 0:
            if hasattr(self, 'state'):
                self.state = "dying"
                if 'dying' in getattr(self.animations, 'animations', {}):
                    self.animations.set_animation('dying')
            else:
                self.is_dead = True

        if self.attack_pending:
            self.attack_pending = False
            self.attack_progress = 0
            self.wait_timer = 30
            self.has_hit_player = False

        self.blink_timer = self.blink_duration  # начинаем мигание

    def perform_melee_attack(self, tiles, player):
        dx = self.direction * self.attack_speed
        self.attack_progress += abs(dx)
        self.apply_gravity_and_collisions(dx, 0, tiles)

        if self.rect.colliderect(player.rect) and not self.has_hit_player:
            player.take_damage(self.damage, self.rect.x)
            self.has_hit_player = True

        if self.attack_progress >= self.attack_distance:
            self.attack_pending = False
            self.attack_progress = 0
            self.wait_timer = 30
            self.has_hit_player = False

    def return_to_spawn(self, tiles, speed=None):
        if abs(self.rect.x - self.start_x) < 5:
            self.returning_to_spawn = False
            return

        direction = 1 if self.rect.x < self.start_x else -1
        move_speed = speed if speed is not None else self.speed
        dx = direction * move_speed
        self.rect.x += dx
        _, _ = self.apply_gravity_and_collisions(0, 0, tiles)

    def chase_player(self, player, chase_speed):
        self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
        self.rect.x += self.direction * chase_speed

    def check_patrol_bounds(self):
        if abs(self.rect.x - self.start_x) > self.move_range * 0.99:
            self.direction *= -1
            self.wait_timer = 60

    def check_aggro(self, player, range_tiles):
        if not self.has_line_of_sight(player, self.level_tiles):
            return False

        aggro_range = range_tiles * TILE_SIZE
        distance_x = player.rect.centerx - self.rect.centerx
        distance_y = abs(player.rect.centery - self.rect.centery)

        if distance_y < TILE_SIZE:
            if (self.direction == 1 and 0 < distance_x <= aggro_range) or (self.direction == -1 and 0 > distance_x >= -aggro_range):
                return True
        return False

    def check_archer_aggro(self, player, range_tiles):
        if not self.has_line_of_sight(player, self.level_tiles):
            return False

        aggro_range = range_tiles * TILE_SIZE
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        if (self.direction == 1 and dx > 0 and abs(dy) <= dx * 0.5 and (dx**2 + dy**2)**0.5 <= aggro_range) or \
           (self.direction == -1 and dx < 0 and abs(dy) <= abs(dx) * 0.5 and (dx**2 + dy**2)**0.5 <= aggro_range):
            return True
        return False

    def has_line_of_sight(self, player, tiles):
        x1, y1 = self.rect.centerx, self.rect.centery
        x2, y2 = player.rect.centerx, player.rect.centery

        steps = int(max(abs(x2 - x1), abs(y2 - y1)) / (TILE_SIZE / 4))
        if steps == 0:
            return True

        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        for step in range(1, steps):
            check_x = x1 + dx * step
            check_y = y1 + dy * step
            check_rect = pygame.Rect(check_x, check_y, 4, 4)

            if any(tile[0] in ("floor", "barrier") and check_rect.colliderect(tile[1]) for tile in tiles):
                return False

        return True

    def perform_projectile_attack(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)

        velocity_x = (dx / distance) * self.projectile_speed
        velocity_y = (dy / distance) * self.projectile_speed

        arrow = pygame.Rect(
            self.rect.centerx,
            self.rect.centery,
            TILE_SIZE // 4,
            TILE_SIZE // 8
        )
        self.projectiles.append((arrow, velocity_x, velocity_y))

    def update_projectiles(self, tiles, player):
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        updated_projectiles = []
        for arrow, velocity_x, velocity_y in self.projectiles:
            arrow.x += velocity_x
            arrow.y += velocity_y

            if arrow.colliderect(player.rect):
                player.take_damage(self.damage, self.rect.x)
                continue

            if not (0 <= arrow.x <= TILE_SIZE * 100 and 0 <= arrow.y <= TILE_SIZE * 100):
                continue

            if any(arrow.colliderect(tile[1]) for tile in tiles):
                continue

            updated_projectiles.append((arrow, velocity_x, velocity_y))

        self.projectiles = updated_projectiles

    def draw_basic(self, screen, color, offset_x, offset_y):
        pygame.draw.rect(
            screen,
            color,
            (self.rect.x - offset_x, self.rect.y - offset_y + 1, self.rect.width, self.rect.height)
        )
        eye_x = self.rect.right - 5 - offset_x if self.direction == 1 else self.rect.left + 5 - offset_x
        eye_y = self.rect.y - offset_y + self.rect.height // 4
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 3)

    def draw_projectiles(self, screen, offset_x, offset_y, projectile_type="arrow"):
        for arrow, _, _ in self.projectiles:
            if projectile_type == "arrow":
                pygame.draw.rect(screen, (255, 255, 0), (arrow.x - offset_x, arrow.y - offset_y, arrow.width, arrow.height))
            elif projectile_type == "fireball":
                center = (int(arrow.centerx - offset_x), int(arrow.centery - offset_y))
                radius = TILE_SIZE // 2
                pygame.draw.circle(screen, (255, 140, 0), center, radius)

    def _update_idle_or_attack(self):
        if hasattr(self, 'animations'):
            if self.attack_pending:
                self.animations.set_animation('attack')
            else:
                self.animations.set_animation('idle')
            self.animations.update_direction(self.direction)
            self.animations.update()

    def _update_idle(self):
        if hasattr(self, 'animations'):
            self.animations.set_animation('idle')
            self.animations.update()

    def _update_run(self):
        if hasattr(self, 'animations'):
            self.animations.set_animation('run')
            self.animations.update_direction(self.direction)
            self.animations.update()

    def _handle_death_states(self):
        if hasattr(self, 'state'):
            if self.state == 'dying':
                # Один раз проигрываем звук смерти
                if not hasattr(self, '_played_dying_sound'):
                    self.play_sound("dying")
                    self._played_dying_sound = True

                # Проверка завершения анимации смерти
                if self.animations.frame_index == len(self.animations.animations.get('dying', [])) - 1:
                    self.state = 'dead'
                    self.dead_timer = 250
                    if hasattr(self, 'animations'):
                        self.animations.set_animation('dead')

            elif self.state == 'dead':
                self.dead_timer -= 1
                if self.dead_timer <= 0:
                    self.state = 'decomposing'
                    if hasattr(self, 'animations'):
                        self.animations.set_animation('decomposing')
            elif self.state == 'decomposing':
                frames = self.animations.animations.get('decomposing', [])
                if self.animations.frame_index == len(frames) - 1:
                    self.is_dead = True

            if hasattr(self, 'animations'):
                self.animations.update()

    def draw_enemy_hp(self, screen, offset_x, offset_y):
        if self.hp <= 0:
            return

        diamond_size = 10
        horizontal_spacing = 2
        vertical_spacing = 0

        start_x = self.rect.centerx - offset_x
        start_y = self.rect.y - offset_y - 30

        layout = []

        if self.hp >= 6:
            layout = [
                (-diamond_size//2 - horizontal_spacing//2, -diamond_size*2 - vertical_spacing),
                (diamond_size//2 + horizontal_spacing//2, -diamond_size*2 - vertical_spacing),
                (0, -diamond_size - vertical_spacing//2),
                (-diamond_size//2 - horizontal_spacing//2, 0),
                (diamond_size//2 + horizontal_spacing//2, 0),
                (0, diamond_size + vertical_spacing//2)
            ]
        elif self.hp == 5:
            layout = [
                (diamond_size//2 + horizontal_spacing//2 + 2, -diamond_size*2 - vertical_spacing),
                (0, -diamond_size - vertical_spacing//2),
                (-diamond_size//2 - horizontal_spacing//2, 0),
                (diamond_size//2 + horizontal_spacing//2, 0),
                (0, diamond_size + vertical_spacing//2)
            ]
        elif self.hp == 4:
            layout = [
                (0, -diamond_size - vertical_spacing//2),
                (-diamond_size//2 - horizontal_spacing//2, 0),
                (diamond_size//2 + horizontal_spacing//2, 0),
                (0, diamond_size + vertical_spacing//2)
            ]
        elif self.hp == 3:
            layout = [
                (-diamond_size//2 - horizontal_spacing//2, -diamond_size - vertical_spacing//2),
                (diamond_size//2 + horizontal_spacing//2, -diamond_size - vertical_spacing//2),
                (0, 0)
            ]
        elif self.hp == 2:
            layout = [
                (diamond_size//2 + horizontal_spacing//2, -diamond_size - vertical_spacing//2),
                (0, 0)
            ]
        elif self.hp == 1:
            layout = [
                (0, 0)
            ]

        for dx, dy in layout:
            center_x = start_x + dx
            center_y = start_y + dy

            points = [
                (center_x, center_y - diamond_size // 2),
                (center_x + diamond_size // 2, center_y),
                (center_x, center_y + diamond_size // 2),
                (center_x - diamond_size // 2, center_y)
            ]

            pygame.draw.polygon(screen, (105, 0, 0), points, width=4)
            pygame.draw.polygon(screen, (200, 0, 0), points, width=0)

    def draw_enemy(self, screen, offset_x, offset_y, show_colliders=True, show_hp=True, ui=None):
        should_draw = True
        if self.blink_timer > 0:
            if (self.blink_timer // self.blink_frequency) % 2 == 0:
                should_draw = False  # скрываем на определённые кадры
            self.blink_timer -= 1

        if should_draw and hasattr(self, 'animations'):
            image = self.animations.get_image()
            if image:
                size, offset = self.animations.get_current_animation_settings()
                scaled_image = pygame.transform.scale(image, size)
                screen.blit(
                    scaled_image,
                    (self.rect.x - offset_x + offset[0], self.rect.y - offset_y + offset[1])
                )
    
        if show_colliders:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height),
                2
            )

        if show_hp and self.hp > 0:
            self.draw_enemy_hp(screen, offset_x, offset_y)