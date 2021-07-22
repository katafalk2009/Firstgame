from Firstgame.environment import *
from Firstgame.player import *
from Firstgame.menu import *
import Firstgame.bottesting
import pygame


class Game:
    background = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    background.fill(BG_COLOUR)
    timer = pygame.time.Clock()

    def __init__(self, level, testmodeon):
        self.hero = Player(200, 500, 'h.png')
        self.entities = pygame.sprite.Group()
        self.movables = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.platforms = []
        self.spikesplatforms = []
        self.monsters = []
        self.consumables = []
        self.healthbar = HealthBar('hp.png')
        self.done = True
        self.right = self.left = self.up = False
        self.testmodeon = testmodeon
        self.gotomenu = False
        x = y = 0
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = Platform(x, y, 'platform.png')
                    self.platforms.append(pf)
                    self.entities.add(pf)
                if col == 'E':
                    self.exitplatform = ExitPlatform(x, y, 'platform_e.png')
                    self.entities.add(self.exitplatform)
                if col == 'S':
                    spf = SpikesPlatform(x, y, 'platform_s.png')
                    self.spikesplatforms.append(spf)
                    self.entities.add(spf)
                if col == 'M':
                    mon = Monster(x, y, 'monster.png')
                    self.monsters.append(mon)
                    self.entities.add(mon)
                    self.movables.add(mon)
                if col == "R":
                    r = RUM(x, y, 'rum.png')
                    self.consumables.append(r)
                    self.entities.add(r)

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        self.total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        self.total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
        self.camera = Camera(camera_configure, self.total_level_width, self.total_level_height)
        self.entities.add(self.hero)

    def playgame(self, window):
        self.gotomenu = False

        '''Основной цикл игры'''
        while self.hero.done:

            self.timer.tick(60)
            for e in pygame.event.get():  # Перебираем события
                if e.type == pygame.QUIT:  # для определения времени выхода
                    raise SystemExit
                if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                    self.left = self.right = self.up = False
                    pause(window)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    self.left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    self.right = True
                if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                    self.right = False
                if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                    self.left = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    self.up = True
                if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                    self.up = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.hero.shoot()
                    if self.hero.projectile:
                        self.projectiles.add(self.hero.projectile)
                        self.entities.add(self.hero.projectile)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LALT:
                    self.hero.atack()
                    self.projectiles.add(self.hero.sword)
                    self.entities.add(self.hero.sword)
                if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                    self.up = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.hero.done = False
                    self.gotomenu = True
            if self.testmodeon:
                Firstgame.bottesting.bot_play(self)
            window.blit(self.background, (0, 0))
            self.camera.update(self.hero)
            self.hero.update(self.left, self.right, self.up, self.platforms, self.exitplatform,
                             self.spikesplatforms, self.monsters, self.consumables, self.entities, self.projectiles)
            self.movables.update(self.hero, self.entities, self.movables, self.monsters)
            self.projectiles.update(self.monsters, self.platforms, self.spikesplatforms, self.entities, self.projectiles)
            for ent in self.entities:
                window.blit(ent.image, self.camera.apply(ent))
            for x in range(self.hero.health):
                window.blit(self.healthbar.image, (50*(x+1), 50))
            if self.hero.health == 0:
                self.hero.die()
            pygame.display.update()
