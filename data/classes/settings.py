import configparser
import pygame

config = configparser.ConfigParser()
config.read("data/config.cfg")

WIDTH = int(config["graphics"]["WIDTH"])
HEIGHT = int(config["graphics"]["HEIGHT"])
FPS = int(config["graphics"]["FPS"])
TILE_SIZE = int(config["graphics"]["TILE_SIZE"])

def get_key(key_str):
    return getattr(pygame, key_str)

def get_keys(key_list_str):
    return {get_key(k.strip()) for k in key_list_str.split(",")}

# Управление
INVENTORY_TOGGLE = get_key(config["controls"]["INVENTORY_TOGGLE"])
USE_ITEM = get_keys(config["controls"]["USE_ITEM"])
MOVE_LEFT = get_key(config["controls"]["MOVE_LEFT"])
MOVE_RIGHT = get_key(config["controls"]["MOVE_RIGHT"])
MOVE_UP = get_key(config["controls"]["MOVE_UP"])
MOVE_DOWN = get_key(config["controls"]["MOVE_DOWN"])
JUMP = get_key(config["controls"]["JUMP"])
ATTACK = get_key(config["controls"]["ATTACK"])
INTERACT = get_key(config["controls"]["INTERACT"])
SWITCH_LEVEL = get_key(config["controls"]["SWITCH_LEVEL"])
