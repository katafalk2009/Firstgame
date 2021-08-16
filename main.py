import pygame
import levels
import shelve
import game
import camera
import menu


def main():
    """
    Main loop of program.
    :return:
    """
    while True:
        pygame.init()
        window = pygame.display.set_mode((camera.WIN_WIDTH, camera.WIN_HEIGHT))
        pygame.display.set_caption('Pirates')
        menu_ = menu.Menu(['start', 'test', 'quit'])
        menu_.play_menu(window)
        winlevel = True
        level = 0
        with shelve.open('savefile') as db:
            db['health'] = health = 3
        while health > 0:
            if winlevel:
                level += 1
            game_ = game.Game(levels.levels['level%d' % level],
                              menu_.test_mode_on)
            game_.playgame(window)
            health = game_.hero.health
            winlevel = game_.hero.winlevel
            if (level == 2 and winlevel) or game_.gotomenu:
                break


if __name__ == "__main__":
    main()
