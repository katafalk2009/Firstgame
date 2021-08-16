import pygame
import time


def go_left():
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))


def go_right():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))



def jump():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))


def stopjump():
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))


def shoot():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))


def bot_play(game):
    if game.hero.rect.x < 800:
        go_right()
    else:
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
    if 550<game.hero.rect.x< 600:
        jump()
    else:
        stopjump()
    if game.hero.rect.x == 800:
        shoot()
    else:
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE))
    # print('gameup', game.up)
    # print('geroy', game.hero.rect.x)
    # if game.hero.rect.x < 800:
    #     go_right()
    # else:
    #     pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
    #
    # for i in game.spikes_platforms:
    #     player_platform_collision = i.rect.x - game.hero.rect.x
    #     print(player_platform_collision)
    #     if 51 > player_platform_collision > 0:
    #         jump()
    #         break
    #     else:
    #         stopjump()
    # for i in game.monsters:
    #     player_platform_collision = i.rect.x - game.hero.rect.x
    #     print(player_platform_collision)
    #     if 200 > player_platform_collision > 0:
    #         shoot()






