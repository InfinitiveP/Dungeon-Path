import pygame
from data.classes.settings import WIDTH, HEIGHT, FPS
from data.classes.main_menu import MainMenu
from data.classes.about_screen import AboutScreen
from data.classes.start_game import start_game
from data.classes.settings_menu import SettingsMenu

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("data/sounds/music/main_menu_theme.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Path")
clock = pygame.time.Clock()

menu = MainMenu()
about = AboutScreen()
settings_menu = SettingsMenu()

run = True
while run:
    clock.tick(FPS)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    screen.fill((20, 20, 20))

    if menu.visible:
        result = menu.handle_input(events)

        if result == "Играть":
            pygame.mixer.music.stop()  # остановить музыку
            menu.visible = False
            start_game(screen)
            pygame.mixer.music.load("data/sounds/music/main_menu_theme.wav")  # перезапустить после выхода из игры
            pygame.mixer.music.play(-1)
            menu.visible = True

        elif result == "Настройки":
            menu.visible = False
            settings_menu.visible = True

        elif result == "Об Игре":
            menu.visible = False
            about.visible = True

        elif result == "Выход":
            run = False

        menu.draw(screen)

    elif settings_menu.visible:
        result = settings_menu.handle_input(events)
        if result == "main_menu":
            settings_menu.visible = False
            menu.visible = True

        settings_menu.draw(screen)

    elif about.visible:
        result = about.handle_input(events)
        if result == "Назад":
            about.visible = False
            menu.visible = True

        about.draw(screen)

    pygame.display.update()

pygame.quit()