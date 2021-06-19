import pygame


def go_left():
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))


def go_right():
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))


def jump():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))


def stopjump():
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))


def bot_play(game):
    pygame.event.clear(eventtype=pygame.KEYDOWN)
    print('gameup', game.up)
    print('geroy', game.hero.rect.x)
    if game.hero.rect.x < 400:
        go_right()
    for i in game.spikesplatforms:
        print('платформа', i.rect.x)
        if i.rect.x == game.hero.rect.x:
            jump()
            break





