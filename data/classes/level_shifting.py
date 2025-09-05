import pygame
from data.classes.level import Level
from data.classes.player import Player
from data.classes.camera import Camera
from data.classes.enemy import EnemyPassive, EnemyActive, EnemyArcher, EnemyMage, BossEnemy
from data.classes.npc_placeholder import NPCPlaceholder

class LevelShifter:
    def __init__(self):
        self.in_teleport = False

    def handle_teleport(self, player, level):
        teleport_triggered = False
        from_teleport_pos = None
        target_type = None
        target_level = None

        for tile_type, tile_rect in level.tiles:
            if tile_type in ("teleport_q", "teleport_3", "teleport_4", "teleport_2") and player.rect.colliderect(tile_rect):
                teleport_triggered = True
                if not self.in_teleport:
                    self.in_teleport = True
                    from_teleport_pos = tile_rect.topleft

                    if tile_type == "teleport_q":
                        target_type = "teleport_q"
                        if level.current_map == level.level_map1:
                            target_level = 2
                        elif level.current_map == level.level_map2:
                            target_level = 1

                    elif tile_type == "teleport_3":
                        target_type = "teleport_3"
                        if level.current_map == level.level_map1:
                            target_level = 3
                        elif level.current_map == level.level_map3:
                            target_level = 1

                    elif tile_type == "teleport_4":
                        target_type = "teleport_4"
                        if level.current_map == level.level_map2:
                            target_level = 4
                        elif level.current_map == level.level_map4:
                            target_level = 2

                    elif tile_type == "teleport_2":
                        target_type = "teleport_2"
                        if level.current_map == level.level_map4:
                            target_level = 2

                    break

        if not teleport_triggered:
            self.in_teleport = False

        if not from_teleport_pos or target_level is None:
            return player, level, None, None, None

        new_level = Level(level_number=target_level)

        min_distance = float("inf")
        target_teleport = None
        for tp_rect in new_level.teleport_tiles:
            if any(tp[0] == target_type and tp[1] == tp_rect for tp in new_level.tiles):
                dist = (tp_rect.x - from_teleport_pos[0]) ** 2 + (tp_rect.y - from_teleport_pos[1]) ** 2
                if dist < min_distance:
                    min_distance = dist
                    target_teleport = tp_rect

        if target_teleport:
            spawn_x = target_teleport.x
            spawn_y = target_teleport.y - 32
        else:
            spawn_x = new_level.spawn_x
            spawn_y = new_level.spawn_y

        new_player = Player(spawn_x, spawn_y)
        new_camera = Camera(new_player)

        new_enemies = []
        for data in new_level.enemy_spawns:
            if len(data) == 4:
                type_, x, y, model_name = data
            elif len(data) == 3:
                type_, x, y = data
                model_name = None
            else:
                continue
            if type_ == "passive":
                new_enemies.append(EnemyPassive(x, y))
            elif type_ == "active":
                new_enemies.append(EnemyActive(x, y))
            elif type_ == "archer":
                new_enemies.append(EnemyArcher(x, y))
            elif type_ == "mage":
                new_enemies.append(EnemyMage(x, y, model_name or "default_mage"))
            if type_ == "boss":
                new_enemies.append(BossEnemy(x, y))

        new_npcs = []
        for data in new_level.npc_spawns:
            if len(data) == 4:
                x, y, mode, messages = data
                model_name = "scarecrow"
            elif len(data) == 5:
                x, y, mode, messages, model_name = data
            else:
                continue
            new_npcs.append(NPCPlaceholder(x, y, mode, messages, model_name))

        return new_player, new_level, new_camera, new_enemies, new_npcs
