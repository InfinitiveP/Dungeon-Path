import pygame
import random
from data.classes.enemy_logic import EnemyLogic
from data.classes.settings import TILE_SIZE
from data.classes.animations import Animations
from data.classes.models import Models
from data.classes.quests import quest1_stage, update_quest1_stage

SHOW_COLLIDERS = False
SHOW_ENEMY_HP = True

class EnemyPassive(EnemyLogic):
    def __init__(self, x, y, model_name="slime"):
        super().__init__(x, y)
        self.rect.height = TILE_SIZE
        model = Models.enemy_models[model_name]

        self.sounds = {}
        for name, path in model.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Не удалось загрузить звук: {path}")

        self.speed = 2
        self.move_range = 6 * TILE_SIZE
        self.attack_distance = 2 * TILE_SIZE
        self.attack_speed = 12
        self.damage = 1
        self.hp = 2

        self.state = 'alive'
        self.dead_timer = 0

        self.animations = Animations(
            model["path"],
            custom_settings=model.get("custom_settings"),
            base_direction=model.get("base_direction", 1)
        )

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def update(self, player, tiles):
        self.level_tiles = tiles

        if self.state == 'alive':
            if self.wait_timer > 0:
                self.wait_timer -= 1
                self._update_idle_or_attack()
                return

            if self.attack_pending:
                self.perform_melee_attack(tiles, player)
                self._update_idle_or_attack()
                return

            if self.returning_to_spawn:
                self.return_to_spawn(tiles)
                self._update_run()
                return

            dx = self.direction * self.speed
            old_x = self.rect.x
            self.apply_gravity_and_collisions(dx, 0, tiles)

            if self.rect.x == old_x:
                self.direction *= -1
                self.wait_timer = 60
                self._update_idle()
                return

            self.check_patrol_bounds()

            if self.check_aggro(player, 2):
                self.attack_pending = True
                self.attack_progress = 0
                self.wait_timer = 30

            if abs(self.rect.x - self.start_x) > self.move_range:
                self.returning_to_spawn = True

            self._update_run()

        self._handle_death_states()

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)
        self.play_sound("take_hit")

    def draw(self, screen, offset_x, offset_y):
        self.draw_enemy(screen, offset_x, offset_y, SHOW_COLLIDERS, SHOW_ENEMY_HP)


class EnemyActive(EnemyLogic):
    def __init__(self, x, y, model_name="skeleton"):
        super().__init__(x, y)
        model = Models.enemy_models[model_name]

        self.sounds = {}
        for name, path in model.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Не удалось загрузить звук: {path}")

        self.patrol_speed = 2
        self.chase_speed = 5
        self.move_range = 12 * TILE_SIZE
        self.attack_distance = 3 * TILE_SIZE
        self.attack_speed = 8
        self.damage = 2
        self.hp = 3

        self.state = 'alive'
        self.dead_timer = 0
        self.is_dead = False

        self.sprite_width = TILE_SIZE * 2
        self.sprite_height = TILE_SIZE * 2
        self.sprite_offset_x = -TILE_SIZE // 2
        self.sprite_offset_y = 0

        self.animations = Animations(
            model["path"],
            custom_settings=model.get("custom_settings"),
            base_direction=model.get("base_direction", 1)
        )

        self.attack_pending = False
        self.attack_progress = 0
        self.attack_timer = 0
        self.wait_timer = 0
        self.is_aggro = False
        self.chosen_attack_animation = "attack1"
        self.last_step_time = 0

    def play_sound(self, name, player=None):
        sound = self.sounds.get(name)
        if not sound:
            return

        if name == "step" and player:
            max_dx = 800
            max_dy = 350
            dx = abs(self.rect.centerx - player.rect.centerx)
            dy = abs(self.rect.centery - player.rect.centery)
            if dx > max_dx or dy > max_dy:
                return

        sound.play()

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)
        self.play_sound("take_hit")

    def update(self, player, tiles):
        self.level_tiles = tiles

        if self.state == 'alive':
            if self.wait_timer > 0:
                self.wait_timer -= 1
                if self.attack_pending:
                    if self.attack_timer == 0:
                        self.chosen_attack_animation = random.choice(["attack1", "attack2"])
                        self.animations.set_animation(self.chosen_attack_animation)
                    self.attack_timer += 1
                else:
                    self.animations.set_animation('idle')

                self.animations.update_direction(self.direction)
                self.animations.update()
                return

            if self.attack_pending:
                dx = self.direction * self.attack_speed
                self.apply_gravity_and_collisions(dx, 0, tiles)
                self.attack_progress += abs(dx)

                if self.rect.colliderect(player.rect) and not self.has_hit_player:
                    player.take_damage(self.damage, self.rect.x)
                    self.has_hit_player = True

                if self.attack_progress >= self.attack_distance:
                    self.attack_pending = False
                    self.attack_timer = 0
                    self.has_hit_player = False
                    self.wait_timer = 30

                self.animations.update_direction(self.direction)
                self.animations.update()
                return

            if self.returning_to_spawn:
                if self.check_aggro(player, 5):
                    self.returning_to_spawn = False
                    self.is_aggro = True
                    return

                direction_to_spawn = 1 if self.rect.x < self.start_x else -1
                self.direction = direction_to_spawn

                self.return_to_spawn(tiles, self.chase_speed)

                self.animations.set_animation('run')
                self.animations.update_direction(self.direction)
                self.animations.update()
                return

            distance_to_player_x = player.rect.centerx - self.rect.centerx

            if self.check_aggro(player, 5):
                self.is_aggro = True
            else:
                self.is_aggro = False

            if self.is_aggro:
                self.chase_player(player, self.chase_speed)

                # 🔊 Шаги при агрессии
                if self.on_ground:
                    now = pygame.time.get_ticks()
                    if now - self.last_step_time > 300:
                        self.play_sound("step", player)
                        self.last_step_time = now

                if abs(distance_to_player_x) <= 2 * TILE_SIZE:
                    self.attack_pending = True
                    self.attack_progress = 0
                    self.wait_timer = 30
            else:
                dx = self.direction * self.patrol_speed
                old_x = self.rect.x
                dx, dy = self.apply_gravity_and_collisions(dx, 0, tiles)

                if self.rect.x == old_x:
                    self.direction *= -1
                    self.wait_timer = 60
                    self.animations.set_animation('idle')
                    self.animations.update()
                    return

                self.check_patrol_bounds()
                if self.on_ground:
                    now = pygame.time.get_ticks()
                    if now - self.last_step_time > 300:
                        self.play_sound("step", player)
                        self.last_step_time = now

            if abs(self.rect.x - self.start_x) > self.move_range:
                self.returning_to_spawn = True

            self.animations.set_animation('run')
            self.animations.frame_durations['run'] = 4 if self.is_aggro else 8
            self.animations.update_direction(self.direction)
            self.animations.update()

        self._handle_death_states()

    def draw(self, screen, offset_x, offset_y):
        self.draw_enemy(screen, offset_x, offset_y, SHOW_COLLIDERS, SHOW_ENEMY_HP)




class EnemyArcher(EnemyLogic):
    def __init__(self, x, y, model_name="archer"):
        super().__init__(x, y)
        model = Models.enemy_models[model_name]

        self.sounds = {}
        for name, path in model.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f" удалось загрузить звук: {path}")

        self.speed = 2
        self.move_range = 6 * TILE_SIZE
        self.attack_range = 10 * TILE_SIZE
        self.damage = 1
        self.projectile_speed = 13
        self.attack_cooldown = 120
        self.projectile_cooldown = 0
        self.hp = 2

        self.state = 'alive'
        self.dead_timer = 0
        self.is_dead = False

        self.attack_pending = False
        self.wait_timer = 0

        self.last_step_time = 0

        self.animations = Animations(
            model["path"],
            custom_settings=model.get("custom_settings"),
            base_direction=model.get("base_direction", 1)
        )

    def play_sound(self, name, player=None):
        sound = self.sounds.get(name)
        if not sound:
            return

        if player:
            max_dx = 800  # по горизонтали
            max_dy = 350  # по вертикали (можно подстроить)

            dx = abs(self.rect.centerx - player.rect.centerx)
            dy = abs(self.rect.centery - player.rect.centery)

            if dx > max_dx or dy > max_dy:
                return  # игрок слишком далеко по X или Y

        sound.play()

    def update(self, player, tiles):
        self.level_tiles = tiles

        if self.state == 'alive':
            moving = False

            if self.wait_timer > 0:
                self.wait_timer -= 1
                if self.wait_timer == 0 and self.attack_pending:
                    self.perform_projectile_attack(player)
                    self.attack_pending = False
                else:
                    if self.attack_pending:
                        self.animations.set_animation('attack')
                    else:
                        self.animations.set_animation('idle')

                self.animations.update_direction(self.direction)
                self.animations.update()
                return

            self.update_projectiles(tiles, player)

            if self.returning_to_spawn:
                self.return_to_spawn(tiles)
            elif self.check_archer_aggro(player, 8):
                if self.projectile_cooldown <= 0 and not self.attack_pending:
                    self.play_sound("human_bow_setup")
                    self.attack_pending = True
                    self.projectile_cooldown = self.attack_cooldown
                    self.wait_timer = 30
                    self.animations.set_animation('attack')
            else:
                dx = self.direction * self.speed
                old_x = self.rect.x
                dx, dy = self.apply_gravity_and_collisions(dx, 0, tiles)

                if self.rect.x == old_x:
                    self.direction *= -1
                    self.wait_timer = 60
                else:
                    moving = True
                    self.check_patrol_bounds()

            if abs(self.rect.x - self.start_x) > self.move_range:
                self.returning_to_spawn = True

            if not self.attack_pending:
                if moving:
                    self.animations.set_animation('run')
                    if moving and self.on_ground:
                        now = pygame.time.get_ticks()
                        if now - self.last_step_time >= 300:
                            self.play_sound("step", player)
                            self.last_step_time = now
                else:
                    self.animations.set_animation('idle')

        self._handle_death_states()

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)
        self.play_sound("human_take_hit")

    def draw(self, screen, offset_x, offset_y):
        self.draw_enemy(screen, offset_x, offset_y, SHOW_COLLIDERS, SHOW_ENEMY_HP)
        self.draw_projectiles(screen, offset_x, offset_y, projectile_type="arrow")


class EnemyMage(EnemyLogic):
    def __init__(self, x, y, model_name="default_mage"):
        super().__init__(x, y)
        model = Models.enemy_models[model_name]

        self.sounds = {}
        for name, path in model.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Не удалось загрузить звук: {path}")

        self.speed = 2
        self.move_range = 6 * TILE_SIZE
        self.damage = 4
        self.projectile_speed = 7
        self.attack_cooldown = 120
        self.projectile_cooldown = 0
        self.hp = 2

        self.state = 'alive'
        self.dead_timer = 0
        self.is_dead = False

        self.sprite_width = TILE_SIZE * 2
        self.sprite_height = TILE_SIZE * 2
        self.sprite_offset_x = -TILE_SIZE // 2
        self.sprite_offset_y = 0

        self.animations = Animations(
            model["path"],
            custom_settings=model["custom_settings"],
            base_direction=model["base_direction"]
        )
    
    def play_sound(self, name, player=None):
        sound = self.sounds.get(name)
        if not sound:
            return

        if player:
            max_dx = 800
            max_dy = 350
            dx = abs(self.rect.centerx - player.rect.centerx)
            dy = abs(self.rect.centery - player.rect.centery)
            if dx > max_dx or dy > max_dy:
                return

        sound.play()

    def update(self, player, tiles):
        self.level_tiles = tiles

        if self.state == 'alive':
            moving = False

            if self.wait_timer > 0:
                self.wait_timer -= 1
                if self.wait_timer == 0 and self.attack_pending:
                    self.perform_projectile_attack(player)
                    self.attack_pending = False
                else:
                    if self.attack_pending:
                        self.animations.set_animation('attack')
                    else:
                        self.animations.set_animation('idle')

                self.animations.update_direction(self.direction)
                self.animations.update()
                return

            self.update_projectiles(tiles, player)

            if self.returning_to_spawn:
                self.return_to_spawn(tiles)
            elif self.check_archer_aggro(player, 8):
                if self.projectile_cooldown <= 0 and not self.attack_pending:
                    self.play_sound("fireball_sound", player)
                    self.attack_pending = True
                    self.projectile_cooldown = self.attack_cooldown
                    self.wait_timer = 30
                    self.animations.set_animation('attack')
            else:
                dx = self.direction * self.speed
                old_x = self.rect.x
                dx, dy = self.apply_gravity_and_collisions(dx, 0, tiles)

                if self.rect.x == old_x:
                    self.direction *= -1
                    self.wait_timer = 60
                else:
                    moving = True
                    self.check_patrol_bounds()

            if abs(self.rect.x - self.start_x) > self.move_range:
                self.returning_to_spawn = True

            if not self.attack_pending:
                if moving:
                    self.animations.set_animation('run')
                else:
                    self.animations.set_animation('idle')

        self._handle_death_states()

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)
        self.play_sound("human_take_hit")

    def draw(self, screen, offset_x, offset_y):
        self.draw_enemy(screen, offset_x, offset_y, SHOW_COLLIDERS, SHOW_ENEMY_HP)
        self.draw_projectiles(screen, offset_x, offset_y, projectile_type="fireball")

class BossEnemy(EnemyLogic):
    def __init__(self, x, y, model_name="golem"):
        super().__init__(x, y)
        model = Models.enemy_models[model_name]

        self.sounds = {}
        for name, path in model.get("sounds", {}).items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Не удалось загрузить звук: {path}")

        self.sprite_width = TILE_SIZE * 2
        self.sprite_height = TILE_SIZE * 4
        self.rect.width = self.sprite_width
        self.rect.height = self.sprite_height

        self.hp = 6
        self.damage = 3
        self.projectile_speed = 9

        self.state = 'alive'
        self.dead_timer = 0
        self.is_dead = False

        self.animations = Animations(
            model["path"],
            custom_settings=model.get("custom_settings"),
            base_direction=model.get("base_direction", 1)
        )

        self.attack_pending = False
        self.attacking = False
        self.windup_timer = 0
        self.attack_cooldown_timer = 0
        self.has_hit_player = False

        self.aggro_zone = pygame.Rect(
            self.rect.centerx - 10 * TILE_SIZE,
            self.rect.centery - 10 * TILE_SIZE,
            20 * TILE_SIZE,
            20 * TILE_SIZE
        )

        # AOE атака
        self.aoe_tiles = []
        self.aoe_active = False
        self.aoe_rise_speed = 4
        self.aoe_max_height = TILE_SIZE
        self.aoe_lifetime_timer = 0

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def update(self, player, tiles):
        self.level_tiles = tiles
        self.aggro_zone.center = self.rect.center

        if self.state != 'alive':
            self._handle_death_states()
            if not self.is_dead:
                self.is_dead = True
                self.play_sound("golem_dying")
            if quest1_stage == 1:
                update_quest1_stage(2)
            return

        # Перерыв между атаками
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1
            if self.animations.current_animation != "attack" or self.animations.frame_index >= len(self.animations.animations["attack"]) - 1:
                self.animations.set_animation("idle")
            self.animations.update_direction(self.direction)
            self.animations.update()
            return

        # Фаза подготовки (анимация замаха)
        if self.windup_timer > 0:
            self.windup_timer -= 1
            self.animations.update_direction(self.direction)
            self.animations.update()
            if self.windup_timer == 0 and self.attack_pending:
                self.perform_aoe_attack()
                self.update_aoe_tiles(player)  # шипы начнут расти сразу же
                return

        # Если шипы активны
        if self.aoe_active:
            self.update_aoe_tiles(player)
            self.animations.update()
            return

        # Начало новой атаки
        if not self.attack_pending and not self.attacking and self.windup_timer == 0 and not self.aoe_active and self.attack_cooldown_timer == 0:
            if self.aggro_zone.colliderect(player.rect):
                self.attack_pending = True
                self.attacking = True
                self.windup_timer = 30
                self.animations.set_animation("attack")
                self.animations.update_direction(self.direction)


        # Если ничего не происходит
        if self.animations.current_animation != "attack" or self.animations.frame_index >= len(self.animations.animations["attack"]) - 1:
            self.animations.set_animation("idle")

        self.animations.update_direction(self.direction)
        self.animations.update()

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)
        self.play_sound("golem_take_hit")

    def perform_aoe_attack(self):
        self.play_sound("aoe_earth_attack")
        self.spawn_aoe_tiles()
        self.attack_pending = False
        self.attacking = False
        self.attack_cooldown_timer = 120  # 2 сек перерыв
        self.has_hit_player = False

    def spawn_aoe_tiles(self):
        self.aoe_tiles.clear()
        self.aoe_active = True
        self.aoe_lifetime_timer = 30  # 0.5 сек шипы стоят
        self.has_hit_player = False
        y = self.rect.bottom
        left = self.rect.centerx - 10 * TILE_SIZE
        for i in range(0, 20 * TILE_SIZE, TILE_SIZE):
            rect = pygame.Rect(left + i, y, TILE_SIZE, 0)
            self.aoe_tiles.append(rect)

    def update_aoe_tiles(self, player):
        all_raised = True
        for rect in self.aoe_tiles:
            # Проверка роста
            if rect.height < self.aoe_max_height:
                rect.height += self.aoe_rise_speed
                rect.y -= self.aoe_rise_speed
                all_raised = False

                # Урон только во время роста
                if not self.has_hit_player and rect.colliderect(player.rect):
                    player.take_damage(self.damage, self.rect.x)
                    self.has_hit_player = True

        if all_raised:
            self.aoe_active = False
            self.aoe_tiles.clear()


    def draw(self, screen, offset_x, offset_y):
        self.draw_enemy(screen, offset_x, offset_y, SHOW_COLLIDERS, SHOW_ENEMY_HP)

        if self.aoe_active:
            for rect in self.aoe_tiles:
                draw_rect = rect.move(-offset_x, -offset_y)
                pygame.draw.rect(screen, (255, 0, 0), draw_rect)
                pygame.draw.rect(screen, (0, 0, 0), draw_rect, width=1)
