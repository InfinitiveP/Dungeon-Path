from data.classes.settings import *

def apply_gravity(vel_y):
    vel_y += 0.5
    if vel_y > 12:
        vel_y = 12
    return vel_y

def handle_collisions(rect, dx, dy, vel_y, tiles):
    rect.x += dx
    for tile_type, tile_rect in tiles:
        if rect.colliderect(tile_rect):
            if dx > 0:
                rect.right = tile_rect.left
            if dx < 0:
                rect.left = tile_rect.right

    rect.y += dy
    for tile_type, tile_rect in tiles:
        if rect.colliderect(tile_rect):
            if dy > 0:
                rect.bottom = tile_rect.top
                vel_y = 0
                on_ground = True
                return vel_y, on_ground
            if dy < 0:
                rect.top = tile_rect.bottom
                vel_y = 0

    on_ground = False
    return vel_y, on_ground