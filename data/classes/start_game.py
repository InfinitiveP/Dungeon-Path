import pygame
import random
from data.classes.settings import *
from data.classes.player import Player
from data.classes.level import Level
from data.classes.camera import Camera
from data.classes.input_handler import InputHandler
from data.classes.enemy import EnemyPassive, EnemyActive, EnemyArcher, EnemyMage, BossEnemy
from data.classes.npc_placeholder import NPCPlaceholder
from data.classes.level_shifting import LevelShifter
from data.classes.inventory import Inventory
from data.classes.ui import UI
from data.classes.game_menu import GameMenu
#from data.classes.main_menu import MainMenu

def start_game(screen):
    pygame.mixer.init()
    pygame.mixer.music.load("data/sounds/music/bg_theme.wav")
    pygame.mixer.music.set_volume(0.4)  # громкость от 0.0 до 1.0
    pygame.mixer.music.play(-1)  # -1 — зациклить
    clock = pygame.time.Clock()
    level = Level(level_number=1)
    inventory = Inventory()
    player = Player(level.spawn_x + TILE_SIZE, level.spawn_y - TILE_SIZE)
    player.ui = UI(player, inventory)
    camera = Camera(player)
    level_shifter = LevelShifter()
    input_handler = InputHandler(inventory)
    game_menu = GameMenu()

    enemies = []
    for data in level.enemy_spawns:
        if isinstance(data, tuple):
            if len(data) == 4:
                type_, x, y, model_name = data
            elif len(data) == 3:
                type_, x, y = data
                model_name = None
            else:
                continue

            if type_ == "passive":
                enemies.append(EnemyPassive(x, y))
            elif type_ == "active":
                enemies.append(EnemyActive(x, y))
            elif type_ == "archer":
                enemies.append(EnemyArcher(x, y))
            elif type_ == "mage":
                enemies.append(EnemyMage(x, y, model_name or "default_mage"))
            elif type_ == "boss":
                enemies.append(BossEnemy(x, y))

    npcs = []
    for data in level.npc_spawns:
        if len(data) == 4:
            x, y, mode, messages = data
        elif len(data) == 5:
            x, y, mode, messages, model_name = data
        else:
            continue
        npcs.append(NPCPlaceholder(x, y, mode, messages, model_name))

    run = True
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    fade_alpha = 255
    fade_duration_seconds = 2
    fade_step = 255 / (FPS * fade_duration_seconds)
    black_screen_timer = FPS * 0.5
    transition_state = None  # None, "fade_out", "fade_in"

    while run:
        clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_menu.toggle()

        if game_menu.visible:
            selected = game_menu.handle_input(events)
            if selected == "Продолжить":
                game_menu.toggle()
            elif selected == "Главное меню":
                return
        else:
            input_handler.handle_events(player, events, npcs)
            keys = pygame.key.get_pressed()
            input_handler.handle_input(player, keys)

            player.update(level.tiles, enemies)
            camera.update()

            if transition_state is None:
                new_player, new_level, new_camera, new_enemies, new_npcs = level_shifter.handle_teleport(player, level)
                if all(obj is not None for obj in (new_player, new_level, new_camera, new_enemies, new_npcs)):
                    transition_state = "fade_out"
                    next_transition_data = (new_player, new_level, new_camera, new_enemies, new_npcs)
                    fade_alpha = 0

            elif transition_state == "fade_out":
                fade_alpha = min(fade_alpha + fade_step, 255)
                if fade_alpha >= 255:
                    player, level, camera, enemies, npcs = next_transition_data
                    player.ui = UI(player, inventory)
                    transition_state = "fade_in"
                    fade_alpha = 255

            elif transition_state == "fade_in":
                fade_alpha = max(fade_alpha - fade_step, 0)
                if fade_alpha <= 0:
                    transition_state = None

            for npc in npcs:
                npc.update(player, level.tiles)

            alive_enemies = []
            for enemy in enemies:
                enemy.update(player, level.tiles)
                if enemy.is_dead:
                    if random.random() < 1:
                        heart_rect = pygame.Rect(enemy.rect.x, enemy.rect.y, TILE_SIZE, TILE_SIZE)
                        level.tiles.append(("heart", heart_rect))
                        print("Выпало сердечко!")
                else:
                    alive_enemies.append(enemy)
            enemies = alive_enemies

        screen.fill((135, 206, 235))
        level.draw(screen, camera.offset_x, camera.offset_y)

        for npc in npcs:
            npc.draw(screen, camera.offset_x, camera.offset_y)
        for enemy in enemies:
            enemy.draw(screen, camera.offset_x, camera.offset_y)
        player.draw(screen, camera.offset_x, camera.offset_y)

        for tile_type, tile_rect in level.tiles:
            if tile_type == "heart":
                center_x = tile_rect.x + TILE_SIZE // 2 - camera.offset_x
                center_y = tile_rect.y + TILE_SIZE // 2 - camera.offset_y
                inventory.draw_heart(screen, center_x, center_y)

        for tile_type, tile_rect in level.tiles:
            if tile_type == "speed_boots":
                center_x = tile_rect.x + TILE_SIZE // 2 - camera.offset_x
                center_y = tile_rect.y + TILE_SIZE // 2 - camera.offset_y
                inventory.draw_boot(screen, center_x, center_y)

        inventory.draw(screen)
        game_menu.draw(screen)

        if black_screen_timer > 0:
            black_screen_timer -= 1
            fade_surface.set_alpha(255)
            screen.blit(fade_surface, (0, 0))
        elif transition_state in ("fade_out", "fade_in"):
            fade_surface.set_alpha(int(fade_alpha))
            screen.blit(fade_surface, (0, 0))
        elif fade_alpha > 0:
            fade_alpha = max(fade_alpha - fade_step, 0)
            fade_surface.set_alpha(int(fade_alpha))
            screen.blit(fade_surface, (0, 0))

        if level.is_dark:
            darkness = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, 220))

            # Центр круга в координатах экрана
            cx = player.rect.centerx - camera.offset_x
            cy = player.rect.centery - camera.offset_y

            pixel_size = 45  # размер пикселя светового круга
            radius = TILE_SIZE * 4  # радиус освещённой области

            for x in range(-radius, radius + 1, pixel_size):
                for y in range(-radius, radius + 1, pixel_size):
                    if x**2 + y**2 <= radius**2:
                        screen_x = cx + x - (pixel_size // 2)
                        screen_y = cy + y - (pixel_size // 2)
                        pygame.draw.rect(darkness, (0, 0, 0, 0), pygame.Rect(screen_x, screen_y, pixel_size, pixel_size))

            screen.blit(darkness, (0, 0))





        pygame.display.update()

    pygame.quit()
    return
