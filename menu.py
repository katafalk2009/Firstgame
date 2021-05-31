"""
Module with starting and pause menu.
"""
from Firstgame.camera import *
import pygame


class Menu:
    """
    Starting menu class.
    """
    background = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    background.fill(BG_COLOUR)
    ACTIVE_COLOUR = (150, 0, 0)
    COLOUR = (250, 250, 250)
    MENU_POS_X = 500
    MENU_POS_Y = 200

    def __init__(self, items):
        self.items = items
        self.font = pygame.font.SysFont('Arial', 50)
        self.active_item = 10
        self.testmodeone = False

    def render(self, item, window, number, colour):
        font_item = self.font.render(item, False, colour)
        window.blit(font_item, (self.MENU_POS_X, self.MENU_POS_Y+50*number))

    def play_menu(self, window):
        """
        Starting menu mechanics.
        :param window:
        :return:
        """
        done = True
        while done:
            window.blit(self.background, (0, 0))
            mp = pygame.mouse.get_pos()
            for number, item in enumerate(self.items):
                if self.MENU_POS_X+100 > mp[0] > self.MENU_POS_X and\
                        self.MENU_POS_Y+50*(number+1) > mp[1] > self.MENU_POS_Y+50*number:
                    self.render(item, window, number, self.ACTIVE_COLOUR)
                    self.active_item = number
                else:
                    self.render(item, window, number, self.COLOUR)
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise SystemExit
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.active_item == 0:
                        done = False
                    if self.active_item == 1:
                        self.testmodeone=True
                        done = False
                    if self.active_item == 2:
                        raise SystemExit


def pause(window):
    """
    In-game pause.
    :return:
    """
    font = pygame.font.SysFont('Arial', 50)
    pause_screen = font.render('pause', False, (250, 250, 250))
    window.blit(pause_screen, (500, 500))
    pygame.display.update()
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            return False
