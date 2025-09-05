from data.classes.settings import TILE_SIZE

class Models:
    enemy_models = {
        "default_mage": {
            "path": 'data/textures/enemies/mage',
            "custom_settings": {
                'attack': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE),
                },
                'idle': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 2),
                    'offset': (-TILE_SIZE // 3, 0),
                },
                'run': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 2),
                    'offset': (-TILE_SIZE // 3, 0),
                },
                'dying': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 2),
                    'offset': (-TILE_SIZE // 2, 0),
                },
                'dead': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                    'offset': (-TILE_SIZE // 2, TILE_SIZE // 2),
                },
                'decomposing': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                    'offset': (-TILE_SIZE // 2, TILE_SIZE // 2),
                },
            },
            "base_direction": 1,

            "sounds": {
                "human_take_hit": "data/sounds/enemies/human_take_hit.wav",
                "step": "data/sounds/enemies/human_step.wav",
                "fireball_sound": "data/sounds/enemies/fireball_sound.wav",
                "dying": "data/sounds/enemies/human_dying.wav",
            }
        },

        "skeleton": {
            "path": "data/textures/enemies/skeleton",
            "custom_settings": {
                "idle": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "run": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "attack1": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "attack2": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "hit": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "dying": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "dead": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "decomposing": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
                "hit": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 0.6),
                },
            },
            "base_direction": 1,

            "sounds": {
                "take_hit": "data/sounds/enemies/skeleton_take_hit.wav",
                "dying": "data/sounds/enemies/skeleton_take_hit.wav",
                "step": "data/sounds/enemies/skeleton_step.wav",
            }
        },

        "slime": {
            "path": "data/textures/enemies/slime",
            "custom_settings": {
                "idle": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "run": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "attack": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "hit": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "dying": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "dead": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
                "decomposing": {
                    "size": (TILE_SIZE * 3.5, TILE_SIZE * 3.5),
                    "offset": (-TILE_SIZE * 1.3, -TILE_SIZE * 1.6),
                },
            },
            "base_direction": 1,

            "sounds": {
                "take_hit": "data/sounds/enemies/slime_take_hit.wav",
                "dying": "data/sounds/enemies/Slime_Death.wav",
            }
        },
        "archer": {
            "path": "data/textures/enemies/archer",
            "custom_settings": {
                'attack': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 0.9),
                },
                'idle': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 0.9),
                },
                'run': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 0.8),
                },
                'dying': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 0.9),
                },
                'dead': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 0.9),
                },
                'decomposing': {
                    'size': (TILE_SIZE * 3, TILE_SIZE * 3.5),
                    'offset': (-TILE_SIZE * 1, -TILE_SIZE * 1),
                },
            },
            "base_direction": 1,

            "sounds": {
                "human_take_hit": "data/sounds/enemies/human_take_hit.wav",
                "step": "data/sounds/enemies/human_step.wav",
                "human_bow_setup": "data/sounds/enemies/human_bow_setup.wav",
                "dying": "data/sounds/enemies/human_dying.wav",
            }
        },

        "golem": {
            "path": "data/textures/enemies/golem",
            "custom_settings": {
                "idle": {
                    "size": (TILE_SIZE * 6, TILE_SIZE * 6),
                    "offset": (-TILE_SIZE * 2, -TILE_SIZE * 1.9)
                },
                "attack": {
                    "size": (TILE_SIZE * 6, TILE_SIZE * 6),
                    "offset": (-TILE_SIZE * 2, -TILE_SIZE * 1.9)
                },
                "dying": {
                    "size": (TILE_SIZE * 6, TILE_SIZE * 6),
                    "offset": (-TILE_SIZE * 2, -TILE_SIZE * 1.9)
                },
                "dead": {
                    "size": (TILE_SIZE * 6, TILE_SIZE * 6),
                    "offset": (-TILE_SIZE * 2, -TILE_SIZE * 1.9)
                },
                "decomposing": {
                    "size": (TILE_SIZE * 6, TILE_SIZE * 6),
                    "offset": (-TILE_SIZE * 2, -TILE_SIZE * 1.9)
                },
            },
            "base_direction": 1,

            "sounds": {
                "aoe_earth_attack": "data/sounds/enemies/aoe_earth_attack.wav",
                "golem_take_hit": "data/sounds/enemies/golem_take_hit.wav",
                "golem_dying": "data/sounds/enemies/golem_dying.wav",
            }
        },
    }

    player_models = {
        "main_hero_skin1": {
            "path": 'data/textures/main_hero/skin1',
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'run': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'jump': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'fall': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'attack1': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 3, 1),
                },
                'attack2': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 3, 1),
                },
                'dying': {
                    'size': (TILE_SIZE * 5.5, TILE_SIZE * 4),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'dead': {
                    'size': (TILE_SIZE * 4, TILE_SIZE * 5.5),
                    'offset': (-TILE_SIZE * 2, 1),
                },
                'decomposing': {
                    'size': (TILE_SIZE * 4, TILE_SIZE * 5.5),
                    'offset': (-TILE_SIZE * 2, 1),
                },
            },
            "base_direction": 1,
            
            "sounds": {
                "step": "data/sounds/player/step.wav",
                "attack": "data/sounds/player/attack.wav",
                "take_hit": "data/sounds/player/take_hit.wav",
                "jump": "data/sounds/player/jump.wav"
            }
        }
    }

    environment_models = {
        "scarecrow": {
            "path": "data/textures/environment/decorations/scarecrow",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 1.5, TILE_SIZE * 2.5),
                    "offset": (-TILE_SIZE * 0.25, -TILE_SIZE * 0.45),
                },
            },
        },
        "pointer": {
            "path": "data/textures/environment/decorations/pointer",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 1, TILE_SIZE * 1.5),
                    "offset": (-TILE_SIZE * 0, -TILE_SIZE * -0.55),
                },
            },
        },
        "default_home": {
            "path": "data/textures/environment/decorations/default_home",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 20, TILE_SIZE * 15),
                    "offset": (-TILE_SIZE * 10, -TILE_SIZE * 11.2)
                },
            },
        },
        "2floor_home": {
            "path": "data/textures/environment/decorations/2floor_home",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 20, TILE_SIZE * 15),
                    "offset": (-TILE_SIZE * 10, -TILE_SIZE * 11.2),
                },
            },
        },
        "forger_home": {
            "path": "data/textures/environment/decorations/forger_home",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 20, TILE_SIZE * 15),
                    "offset": (-TILE_SIZE * 7, -TILE_SIZE * 11.2),
                },
            },
        },
        "tavern_home": {
            "path": "data/textures/environment/decorations/tavern_home",
            "custom_settings": {
                'idle': {
                    'size': (TILE_SIZE * 20, TILE_SIZE * 15),
                    "offset": (-TILE_SIZE * 1, -TILE_SIZE * 11.2),
                },
            },
        },
    }

    level_backgrounds = {
        1: "data/textures/background/field/field_bg.jpg",     # Поле
        2: "data/textures/background/forest/forest_bg.jpg",   # Лес
        3: "data/textures/background/forest/forest_bg.jpg",   # Лес
        4: "data/textures/background/cave/cave_bg.jpg",       # Пещера
    }

    buildings_textures = {
        "2floor_home": {
            "path": "data/textures/environment/homes/2floor_home.png",
            "size": (TILE_SIZE * 6, TILE_SIZE * 5),
        },
        "default_home": {
            "path": "data/textures/environment/homes/default_home.png",
            "size": (TILE_SIZE * 4, TILE_SIZE * 3),
        },
        "forger_home": {
            "path": "data/textures/environment/homes/forger_home.png",
            "size": (TILE_SIZE * 5, TILE_SIZE * 3),
        },
        "tavern_home": {
            "path": "data/textures/environment/homes/tavern_home.png",
            "size": (TILE_SIZE * 5, TILE_SIZE * 4),
        },
    }
