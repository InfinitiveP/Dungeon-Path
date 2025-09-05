import pygame
from data.classes.settings import *
from data.classes.quests import get_quest1_text, get_quest1_text_guardian, get_quest1_text_questwall, get_quest1_text_vilager1
import data.classes.quests as quests
from data.classes.models import Models

import os

class Level:
    def __init__(self, level_number=1):
        self.level_map1 = [
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 15, 0, 13],
            [13, "t1", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t2", 13],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]


        self.level_map2 = [
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [1, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [1, "t3", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t1", 13],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.level_map3 = [
            [13, 13, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 13, 13],
            [13, 13, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13],
            [13, 13, 13, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13],
            [13, 0, 14, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13],
            [13, "t2", 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.level_map4 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 13],
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t4", 0, 13],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.tiles = []
        self.enemy_spawns = []
        self.npc_spawns = []
        self.current_map = self.level_map1 if level_number == 1 else self.level_map2
        self.teleport_tiles = []
        self.spawn_x = 0
        self.spawn_y = 0
        self.background_image = pygame.image.load(Models.level_backgrounds[level_number]).convert()
        self.background_scroll_speed = 0.25  # скорость параллакса
        self.is_dark = level_number in (4,)  # указываем номера уровней с темнотой
        # Выбор карты
        if level_number == 1:
            self.load_level1()
        elif level_number == 2:
            self.load_level2()
        elif level_number == 3:
            self.current_map = self.level_map3
            self.load_level3()
        elif level_number == 4:
            self.current_map = self.level_map4
            self.load_level4()
        else:
            raise ValueError(f"Неизвестный номер карты: {level_number}")
        
        self.floor_textures_top = []
        self.floor_textures_middle = []
        self.floor_textures_bottom = []

        base_path = "data/textures/environment/ground"

        # Верхний слой: Ground2.png – Ground5.png
        for i in range(2, 6):
            path = os.path.join(base_path, f"Ground{i}.png")
            self.floor_textures_top.append(pygame.image.load(path).convert_alpha())

        # Средний слой: Ground23.png – Ground26.png
        for i in range(23, 27):
            path = os.path.join(base_path, f"Ground{i}.png")
            self.floor_textures_middle.append(pygame.image.load(path).convert_alpha())

        # Нижний слой: Ground43.png – Ground45.png
        for i in range(43, 46):
            path = os.path.join(base_path, f"Ground{i}.png")
            self.floor_textures_bottom.append(pygame.image.load(path).convert_alpha())

    def load_level1(self):
        for y, row in enumerate(self.level_map1):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                # 1 - обычный пол
                if tile == 1:
                    self.tiles.append(("floor", rect))
                # 2 - маркер
                elif tile == 2:
                    self.tiles.append(("marker", rect))
                # 3 - спавн игрока
                elif tile == 3:
                    self.spawn_x = x * TILE_SIZE
                    self.spawn_y = y * TILE_SIZE
                # 4 - таверна с доской обьявлений
                elif tile == 4:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, get_quest1_text_questwall(),
                                                                              "tavern_home"))
                # 5 - дефлтный дом
                elif tile == 5:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["простой дом"],
                                                                              "default_home"))
                # 6 - дом кузнеца
                elif tile == 6:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["кузница"],
                                                                              "forger_home"))
                elif tile == 10:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, get_quest1_text(), "scarecrow"))
                
                # 8 - спавн непися
                elif tile == 8:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, get_quest1_text_vilager1(), "scarecrow"))
                elif tile == 9:
                    self.enemy_spawns.append(("boss", x * TILE_SIZE, y * TILE_SIZE))
                # 7 - дом управляющего
                elif tile == 7:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["дом управдяющего"],
                                                                              "2floor_home"))
                elif tile == "t1":
                    self.tiles.append(("teleport_q", rect))
                    self.teleport_tiles.append(rect)
                elif tile == "t2":
                    if quests.quest1_stage == 2:
                        self.tiles.append(("teleport_3", rect))
                        self.teleport_tiles.append(rect)
                elif tile == 11:
                    self.tiles.append(("heart", rect))
                elif tile == 12:
                    self.tiles.append(("speed_boots", rect))
                elif tile == 13:
                    self.tiles.append(("barrier", rect))
                # 13 - спавн непися
                elif tile == 14:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["Великий лес"],
                                                                              "pointer"))
                # 13 - спавн непися
                elif tile == 15:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, get_quest1_text_guardian(),
                                                                              "scarecrow"))

    def load_level2(self):
        for y, row in enumerate(self.level_map2):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                # 1 - обычный пол
                if tile == 1:
                    self.tiles.append(("floor", rect))
                # 2 - маркер
                elif tile == 2:
                    self.tiles.append(("marker", rect))
                # 3 - спавн игрока
                elif tile == 3:
                    self.spawn_x = x * TILE_SIZE
                    self.spawn_y = y * TILE_SIZE
                # 4 - спавн пассивного врага
                elif tile == 4:
                    self.enemy_spawns.append(("passive", x * TILE_SIZE, y * TILE_SIZE))
                # 5 - спавн активного врага
                elif tile == 5:
                    self.enemy_spawns.append(("active", x * TILE_SIZE, y * TILE_SIZE))
                # 6 - спавн арчера
                elif tile == 6:
                    self.enemy_spawns.append(("archer", x * TILE_SIZE, y * TILE_SIZE))
                # 7 - спавн мага
                elif tile == 7:
                    self.enemy_spawns.append(("mage", x * TILE_SIZE, y * TILE_SIZE, "default_mage"))
                # 8 - спавн NPCPlaceholder
                elif tile == 8:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, ["Мобы находятся слева",
                                                                              "На каждом из 4х уровней по 1 уникальному мобу",
                                                                              "Атакавать ты вожешь нажимая на клавишу SHIFT"],
                                                                              "scarecrow"))
                elif tile == "t1":
                    self.tiles.append(("teleport_q", rect))
                    self.teleport_tiles.append(rect)
                elif tile == "t2":
                    self.tiles.append(("teleport_3", rect))
                    self.teleport_tiles.append(rect)
                elif tile == "t3":
                    self.tiles.append(("teleport_4", rect))
                    self.teleport_tiles.append(rect)
                elif tile == 13:
                    self.tiles.append(("barrier", rect))
                elif tile == 14:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, ["Не ходите туда!!!",
                                                                              "Вас ждёт смерть!!"],
                                                                              "pointer"))
                elif tile == 15:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["Главная комната"],
                                                                              "pointer"))

    def load_level3(self):
        for y, row in enumerate(self.level_map3):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                # 1 - обычный пол
                if tile == 1:
                    self.tiles.append(("floor", rect))
                # 2 - маркер
                elif tile == 2:
                    self.tiles.append(("marker", rect))
                # 3 - спавн игрока
                elif tile == 3:
                    self.spawn_x = x * TILE_SIZE
                    self.spawn_y = y * TILE_SIZE
                # 4 - спавн пассивного врага
                elif tile == 4:
                    self.enemy_spawns.append(("passive", x * TILE_SIZE, y * TILE_SIZE))
                # 5 - спавн активного врага
                elif tile == 5:
                    self.enemy_spawns.append(("active", x * TILE_SIZE, y * TILE_SIZE))
                # 6 - спавн арчера
                elif tile == 6:
                    self.enemy_spawns.append(("archer", x * TILE_SIZE, y * TILE_SIZE))
                # 7 - спавн мага
                elif tile == 7:
                    self.enemy_spawns.append(("mage", x * TILE_SIZE, y * TILE_SIZE, "default_mage"))
                # 8 - спавн NPCPlaceholder
                elif tile == 8:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2, ["Поздравляю, ты прошёл игру!!!",
                                                                              "Делать тебе больше нечего, можешь настакать весь инвентарь предметов, или просто быть мобов в лесу",
                                                                              "А если тебе надоест просто ливай)"], "scarecrow"))
                elif tile == "t2":
                    self.tiles.append(("teleport_3", rect))
                    self.teleport_tiles.append(rect)
                elif tile == 11:
                    self.tiles.append(("heart", rect))
                elif tile == 12:
                    self.tiles.append(("speed_boots", rect))
                elif tile == 13:
                    self.tiles.append(("barrier", rect))
                elif tile == 14:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["Деревня"],
                                                                              "pointer"))
                    
    def load_level4(self):
        for y, row in enumerate(self.level_map4):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    self.tiles.append(("floor", rect))
                elif tile == 2:
                    self.tiles.append(("marker", rect))
                elif tile == 3:
                    self.spawn_x = x * TILE_SIZE
                    self.spawn_y = y * TILE_SIZE
                elif tile == 4:
                    self.enemy_spawns.append(("passive", x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 5:
                    self.enemy_spawns.append(("active", x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 6:
                    self.enemy_spawns.append(("archer", x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 7:
                    self.enemy_spawns.append(("mage", x * TILE_SIZE, y * TILE_SIZE, "default_mage"))
                elif tile == 8:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 2,
                        ["Инвентарь открывается на TAB", "Выбирай предмет клавишами WASD", "Примени F"],
                        "scarecrow"))
                elif tile == 9:
                    if quests.quest1_stage == 1:
                        self.enemy_spawns.append(("boss", x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 11:
                    self.tiles.append(("heart", rect))
                elif tile == 12:
                    self.tiles.append(("speed_boots", rect))
                elif tile == 13:
                    self.tiles.append(("barrier", rect))
                elif tile == 14:
                    self.npc_spawns.append((x * TILE_SIZE, y * TILE_SIZE, 1, ["Добро пожаловать в большую комнату!"], "pointer"))
                elif tile == "t3":
                    self.tiles.append(("teleport_4", rect))
                    self.teleport_tiles.append(rect)
                elif tile == "t4":
                    self.tiles.append(("teleport_2", rect))
                    self.teleport_tiles.append(rect)
                elif tile == "t4":
                    self.tiles.append(("teleport_2", rect))
                    self.teleport_tiles.append(rect)

    def draw(self, screen, camera_x, camera_y):
        screen_rect = screen.get_rect()

        bg_x = -camera_x * self.background_scroll_speed

        screen_width, screen_height = screen.get_size()
        bg_width, bg_height = self.background_image.get_size()

        # Масштаб по высоте с сохранением пропорций
        scale_factor = screen_height / bg_height
        scaled_width = int(bg_width * scale_factor)
        scaled_height = screen_height

        scaled_bg = pygame.transform.scale(self.background_image, (scaled_width, scaled_height))

        # Зацикливаем фон по X
        for x in range(-scaled_width, screen_width + scaled_width, scaled_width):
            screen.blit(scaled_bg, (x + bg_x, 0))

        for tile_type, tile in self.tiles:
            moved_tile = tile.move(-camera_x, -camera_y)
            if moved_tile.colliderect(screen_rect):
                if tile_type == "floor":
                    # Вычисляем координаты тайла в сетке
                    tx = tile.x // TILE_SIZE
                    ty = tile.y // TILE_SIZE

                    # Проверяем, есть ли над ним ещё floor
                    above = any(t for t_type, t in self.tiles if t_type == "floor" and t.x // TILE_SIZE == tx and t.y // TILE_SIZE == ty - 1)

                    if not above:
                        textures = self.floor_textures_top
                    else:
                        # Считаем глубину вниз
                        depth = 0
                        for dy in range(1, 20):  # проверим максимум 20 блоков вниз
                            if any(t for t_type, t in self.tiles if t_type == "floor" and t.x // TILE_SIZE == tx and t.y // TILE_SIZE == ty - dy):
                                break
                            depth += 1

                        if depth == 1:
                            textures = self.floor_textures_middle
                        else:
                            textures = self.floor_textures_bottom

                    # Выбираем текстуру по позиции
                    index = (tx + ty) % len(textures)
                    tex = pygame.transform.scale(textures[index], (TILE_SIZE, TILE_SIZE))
                    screen.blit(tex, moved_tile.topleft)
                elif tile_type == "marker":
                    pygame.draw.rect(screen, (144, 238, 144), moved_tile)  # Салатовый маркер
                elif tile_type == "barrier":
                    pass