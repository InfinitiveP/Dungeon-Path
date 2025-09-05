from data.classes.settings import *

class Camera:
    
    def __init__(self, player):
        self.player = player
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        SMOOTHING = 0.1
        camera_target_x = self.player.rect.centerx - WIDTH // 2
        camera_target_y = self.player.rect.centery - HEIGHT // 2

        self.offset_x += (camera_target_x - self.offset_x) * SMOOTHING
        self.offset_y += (camera_target_y - self.offset_y) * SMOOTHING