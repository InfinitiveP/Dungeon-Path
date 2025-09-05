
import os
import pygame
from data.classes.settings import TILE_SIZE

class Animations:
    def __init__(self, base_path, frame_durations=None, custom_settings=None, base_direction=1):
        """
        base_path - папка с анимациями
        frame_durations - длительность кадров
        custom_settings - настройки для каждой анимации:
            {'attack': {'size': (w, h), 'offset': (x, y)}, ...}
        base_direction - направление модели по умолчанию (1 вправо, -1 влево)
        """
        self.animations = {}
        self.frame_durations = frame_durations or {}
        self.custom_settings = custom_settings or {}
        self.base_direction = base_direction
        self.current_direction = base_direction
        self.is_player = False

        # Загружаем все анимации
        for animation_name in os.listdir(base_path):
            anim_folder = os.path.join(base_path, animation_name)
            if os.path.isdir(anim_folder):
                frames = []
                for file_name in sorted(os.listdir(anim_folder)):
                    if file_name.endswith(('.png', '.gif')):
                        img_path = os.path.join(anim_folder, file_name)
                        image = pygame.image.load(img_path).convert_alpha()
                        frames.append(image)
                self.animations[animation_name] = frames

        self.current_animation = 'idle'
        self.frame_index = 0
        self.timer = 0

    def set_animation(self, name):
        if name != self.current_animation:
            self.current_animation = name
            self.frame_index = 0
            self.timer = 0

    def update_direction(self, direction):
        self.current_direction = direction

    def update(self):
        frames = self.animations.get(self.current_animation, [])
        if not frames:
            return

        duration = self.frame_durations.get(self.current_animation, 6)
        self.timer += 1
        if self.timer >= duration:
            self.timer = 0
            self.frame_index += 1
            if self.frame_index >= len(frames):
                if self.current_animation in ('dying', 'decomposing'):
                    self.frame_index = len(frames) - 1
                else:
                    self.frame_index = 0

    def get_image(self):
        frames = self.animations.get(self.current_animation, [])
        if not frames:
            return None
        image = frames[self.frame_index]

        # Зеркалирование по направлению
        if self.current_direction != self.base_direction:
            image = pygame.transform.flip(image, True, False)

        return image

    def get_current_animation_settings(self):
        """
        Вернёт (размер (w, h), смещение (x, y)) для текущей анимации
        """
        settings = self.custom_settings.get(self.current_animation, {})
        size = settings.get("size", (64, 64))
        offset = settings.get("offset", (0, 0))

        if self.is_player and self.current_direction != self.base_direction:
            # Делаем красивое смещение при флипе
            offset = (-offset[0] - size[0] + TILE_SIZE, offset[1])

        return size, offset
