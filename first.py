
from Firstgame.levels import *
from Firstgame.game import *


def main():
    """
    Main loop of program.
    :return:
    """
    while True:
        pygame.init()
        window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Pirates')
        menu = Menu(['start', 'test', 'quit'])
        menu.play_menu(window)
        winlevel = True
        level = 0
        with shelve.open('savefile') as db:
            db['health'] = health = 3
        while health > 0:
            if winlevel:
                level += 1
            game = Game(levels['level%d' % level], menu.testmodeone)
            game.playgame(window)
            health = game.hero.health
            winlevel = game.hero.winlevel
            if (level == 2 and winlevel) or game.gotomenu:
                break


if __name__ == "__main__":
    main()
