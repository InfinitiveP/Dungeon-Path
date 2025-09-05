from data.classes.settings import *
import pygame

class InputHandler:
    def __init__(self, inventory):
        self.inventory = inventory

    def handle_input(self, player, keys):
        if self.inventory.visible:
            return  # блокируем управление игроком, если открыт инвентарь

        player.move_left = keys[MOVE_LEFT]
        player.move_right = keys[MOVE_RIGHT]

        if keys[JUMP] and player.can_jump:
            player.jump_request = True
            player.can_jump = False

        if keys[ATTACK] and player.can_attack and not player.is_attacking:
            player.start_attack()
            player.can_attack = False

    def handle_events(self, player, events, npcs=None):
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == JUMP:
                    player.can_jump = True
                if event.key == ATTACK:
                    player.can_attack = True

            if event.type == pygame.KEYDOWN:
                if event.key == INVENTORY_TOGGLE:
                    self.inventory.toggle()

                if self.inventory.visible:
                    if event.key == MOVE_LEFT:
                        self.inventory.move_selection(-1, 0)
                    elif event.key == MOVE_RIGHT:
                        self.inventory.move_selection(1, 0)
                    elif event.key == MOVE_UP:
                        self.inventory.move_selection(0, -1)
                    elif event.key == MOVE_DOWN:
                        self.inventory.move_selection(0, 1)
                    elif event.type == pygame.KEYDOWN and event.key in USE_ITEM:
                        self.inventory.use_selected_item(player)
                else:
                    if event.key == INTERACT and npcs:
                        for npc in npcs:
                            if hasattr(npc, 'interact') and npc.triggered:
                                npc.interact()
