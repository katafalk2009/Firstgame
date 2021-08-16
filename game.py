import environment
import player
import menu
import camera
import bottesting
import pygame
import monsters


class Game:
    background = pygame.Surface((camera.WIN_WIDTH, camera.WIN_HEIGHT))
    background.fill(camera.BG_COLOUR)
    timer = pygame.time.Clock()

    def __init__(self, level, test_mode_on):
        self.hero = player.Player(200, 500, 'h.png')
        self.entities = pygame.sprite.Group()
        self.movables = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.platforms = []
        self.spikes_platforms = []
        self.monsters = []
        self.consumables = []
        self.health_bar = player.HealthBar('hp.png')
        self.done = True
        self.right = self.left = self.up = False
        self.test_mode_on = test_mode_on
        self.gotomenu = False
        x = y = 0
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = environment.Platform(x, y, 'platform.png')
                    self.platforms.append(pf)
                    self.entities.add(pf)
                if col == 'E':
                    self.exitplatform = \
                        environment.ExitPlatform(x, y, 'platform_e.png')
                    self.entities.add(self.exitplatform)
                if col == 'S':
                    spf = environment.SpikesPlatform(x, y, 'platform_s.png')
                    self.spikes_platforms.append(spf)
                    self.entities.add(spf)
                if col == 'M':
                    mon = monsters.Monster(x, y, 'monster.png')
                    self.monsters.append(mon)
                    self.entities.add(mon)
                    self.movables.add(mon)
                if col == "R":
                    r = environment.RUM(x, y, 'rum.png')
                    self.consumables.append(r)
                    self.entities.add(r)

                x += environment.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += environment.PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        self.total_level_width = len(level[0]) * environment.PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        self.total_level_height = len(level) * environment.PLATFORM_HEIGHT  # высоту
        self.camera = camera.Camera(camera.camera_configure,
                                    self.total_level_width,
                                    self.total_level_height)
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
                    menu.pause(window)
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
            if self.test_mode_on:
                bottesting.bot_play(self)
            window.blit(self.background, (0, 0))
            self.camera.update(self.hero)
            self.hero.update(self.left, self.right, self.up, self.platforms,
                             self.exitplatform, self.spikes_platforms,
                             self.monsters, self.consumables,
                             self.entities, self.projectiles)
            self.movables.update(self.hero, self.entities, self.movables,
                                 self.monsters)
            self.projectiles.update(self.monsters, self.platforms,
                                    self.spikes_platforms, self.entities,
                                    self.projectiles)
            for ent in self.entities:
                window.blit(ent.image, self.camera.apply(ent))
            for x in range(self.hero.health):
                window.blit(self.health_bar.image, (50 * (x + 1), 50))
            if self.hero.health == 0:
                self.hero.die()
            pygame.display.update()
