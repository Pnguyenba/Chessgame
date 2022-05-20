import pygame
import pygame_menu
from data.constants import *
import main

pygame.init()
screen = pygame.display.set_mode((WIDTH , HEIGHT))

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    main.GameStart()

def menuScreen():
    menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
