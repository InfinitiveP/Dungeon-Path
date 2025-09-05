import pygame
import random

from data.classes.settings import *
from data.classes.physics import apply_gravity, handle_collisions
from data.classes.ui import UI
from data.classes.animations import Animations
from data.classes.models import Models
from data.classes.inventory import Inventory

SHOW_COLLIDERS = False

class Player:
    def __init__(self, x, y, model="main_hero_skin1"):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE * 2)
        self.vel_y = 0
        self.on_ground = False
        self.move_left = False
        self.move_right = False
        self.jump_request = False
        self.can_jump = True
        self.can_attack = True
        self.in_teleport = False
        self.hp = 5
        self.max_hp = 5
        self.speed = 5
        self.speed_boost_timer = 0
        self.spawn_x = x
        self.spawn_y = y
        self.blink_timer = 0
        self.blink_duration = 15  # сколько кадров будет мигать
        self.blink_frequency = 5
        self.pickup_delay = 60
        self.step_timer = 0  # миллисекунды до следующего звука шага
        self.step_interval = 490 # частота шагов в мс
        self.last_step_time = 0
        self.step_interval = 490

        # Атака
        self.is_attacking = False
        self.attack_shifted = False
        self.has_hit = False
        self.attack_progress = 0
        self.attack_distance = TILE_SIZE
        self.attack_speed = 6
        self.attack_direction = 1
        self.chosen_attack_animation = "attack1"

        self.attack_windup = False
        self.attack_windup_timer = 0
        self.attack_duration = 20  # Длительность самой атаки после замаха

        # Смерть
        self.is_dying = False
        self.death_timer = 0

        # Интерфейс
        self.ui = UI(self, Inventory())

        # Анимации
        model_data = Models.player_models[model]
        self.sounds = {}
        for name, path in model_data.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Ошибка загрузки звука: {path}")
        self.animations = Animations(
            model_data["path"],
            custom_settings=model_data.get("custom_settings"),
            base_direction=model_data.get("base_direction", 1)
        )
        self.animations.is_player = True


    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def start_attack(self):
        if not self.is_attacking and not self.attack_windup and not self.is_dying:
            self.attack_windup = True
            self.attack_windup_timer = 10
            self.chosen_attack_animation = random.choice(["attack1", "attack2"])

            if self.move_right:
                self.attack_direction = 1
            elif self.move_left:
                self.attack_direction = -1

            self.play_sound("attack")
            self.animations.set_animation(self.chosen_attack_animation)

    def take_damage(self, amount, attacker_x):
        if self.hp > 0:
            self.ui.spawn_damage_particles(self.hp - 1)
            self.ui.trigger_damage_effects()
        self.hp -= amount
        self.play_sound("take_hit")
        self.blink_timer = self.blink_duration
        if self.hp <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_timer = 60  # 1 секунда на проигрывание анимации смерти
            self.animations.set_animation("dying")
        else:
            if self.rect.centerx < attacker_x:
                self.rect.x -= TILE_SIZE
            else:
                self.rect.x += TILE_SIZE

    def respawn(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.vel_y = 0
        self.hp = self.max_hp
        self.is_dying = False
        self.ui.damage_particles.clear()

    def update(self, tiles, enemies):

        dx = 0
        dy = 0

        self.ui.update()

        # Логика смерти
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.respawn()
            self.animations.update()
            return

        # Логика атаки
        if self.attack_windup:
            self.attack_windup_timer -= 1
            if self.attack_windup_timer <= 0:
                self.attack_windup = False
                self.is_attacking = True
                self.attack_progress = 0
                self.has_hit = False

                #Телепортируем хитбокс на тайл вперед по направлению атаки
                if not self.attack_shifted:
                    if self.attack_direction > 0:
                        self.rect.x += TILE_SIZE
                    else:
                        self.rect.x -= TILE_SIZE
                    self.attack_shifted = True

        elif self.is_attacking:
            dx = self.attack_direction * self.attack_speed
            self.attack_progress += abs(dx)
            if self.attack_progress >= self.attack_distance:
                self.is_attacking = False
                # --- Возвращаем хитбокс обратно ---
                if self.attack_shifted:
                    if self.attack_direction > 0:
                        self.rect.x -= TILE_SIZE
                    else:
                        self.rect.x += TILE_SIZE
                    self.attack_shifted = False

        else:
            if self.move_left:
                dx = -self.speed
                self.attack_direction = -1
            if self.move_right:
                dx = self.speed
                self.attack_direction = 1

            if self.jump_request:
                if self.on_ground:
                    self.vel_y = -14.5
                    self.play_sound("jump")
                self.jump_request = False

        # Применение гравитации
        self.vel_y = apply_gravity(self.vel_y)
        dy += self.vel_y

        # Обработка коллизий
        solid_tiles = [tile for tile in tiles if tile[0] in ("floor", "marker", "barrier")]
        self.vel_y, self.on_ground = handle_collisions(self.rect, dx, dy, self.vel_y, solid_tiles)

        # Проверка удара по врагам
        if self.is_attacking and not self.has_hit:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(1, self.attack_direction)
                    self.has_hit = True
                    #self.is_attacking = False
                    break

        # Выбор анимации
        if self.attack_windup:
            pass
        elif self.is_attacking:
            self.animations.set_animation(self.chosen_attack_animation)
        elif not self.on_ground:
            if self.vel_y < 0:
                self.animations.set_animation("jump")
            else:
                self.animations.set_animation("fall")
        elif self.move_left or self.move_right:
            self.animations.set_animation("run")

            now = pygame.time.get_ticks()
            if self.on_ground and now - self.last_step_time >= self.step_interval:
                self.play_sound("step")
                self.last_step_time = now
        else:
            self.animations.set_animation("idle")

        self.animations.update_direction(self.attack_direction)
        self.animations.update()

        if self.pickup_delay > 0:
            self.pickup_delay -= 1
        else:
            # Подбор предметов
            remaining_tiles = []
            for tile_type, tile_rect in tiles:
                if tile_type == "heart":
                    if self.rect.colliderect(tile_rect):
                        print("Игрок наступил на сердечко!")
                        if hasattr(self, 'ui') and hasattr(self.ui, 'inventory'):
                            added = self.ui.inventory.add_item("heart")
                            print("Добавление в инвентарь:", "успешно" if added else "инвентарь полон!")
                        continue
                elif tile_type == "speed_boots":
                    if self.rect.colliderect(tile_rect):
                        self.ui.inventory.add_item("speed")
                        print("Подобрано зелье скорости")
                        continue
                remaining_tiles.append((tile_type, tile_rect))
            tiles[:] = remaining_tiles

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = 5

    def draw(self, screen, offset_x, offset_y):
        image = self.animations.get_image()
        should_draw = True
        if self.blink_timer > 0:
            if (self.blink_timer // self.blink_frequency) % 2 == 0:
                should_draw = False
            self.blink_timer -= 1

        if image and should_draw:
            size, offset = self.animations.get_current_animation_settings()
            scaled_image = pygame.transform.scale(image, size)
            rect = self.rect
            adjusted_y = rect.y - (scaled_image.get_height() - rect.height)

            screen.blit(
                scaled_image,
                (
                    rect.x - offset_x + offset[0],
                    adjusted_y - offset_y + offset[1]
                )
            )

        if SHOW_COLLIDERS:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height),
                2
            )

        self.ui.draw(screen)
        
