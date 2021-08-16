import environment
import pygame


MOVE_SPEED = 5
JUMP_POWER = 10
WIDTH = 50
HEIGHT = 50
GRAVITY = 0.5


class Player(pygame.sprite.Sprite):
    SHOOT_CD = 1000
    INVUL_TIME = 2000
    ATACK_CD = 500

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = pygame.image.load(filename)
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.watching = 1  # умножаем скорость 1 вправо, -1 влево
        self.winlevel = False
        self.done = True  # для проверки цикла игры
        self.health = 3
        self.destruct = False
        self.last_shoot_time = 0
        self.invul = False
        self.last_dmg = 0
        self.last_atack = 0
        self.sword = Sword(self.rect.x + WIDTH,
                           self.rect.y + HEIGHT / 2,
                           'sword.png')

    def update(self, left,  right, up, platforms, exitplatform,
               spikesplatforms, monsters, consumables, entities, projectiles):
        if not self.onGround:
            self.yvel += GRAVITY
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.watching = -1
        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.watching = 1
        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        self.onGround = False
        self.collide(exitplatform, monsters, consumables, entities)
        self.rect.x += self.xvel
        self.collideplatforms(self.xvel, 0, platforms+spikesplatforms)
        self.rect.y += self.yvel
        self.collideplatforms(0, self.yvel, platforms+spikesplatforms)
        self.check_invul_cd()
        self.check_atacking()

    def collideplatforms(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, environment.SpikesPlatform) and \
                        not self.invul:
                    p.damage(self)
                    self.become_invul()
                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо
                    self.xvel = 0
                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                    self.xvel = 0
                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает
                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def collide_rum(self, rum):
        if pygame.sprite.collide_rect(self, rum):
            if isinstance(rum, environment.RUM):
                rum.heal(self)
            return True

    def collide(self, exitplatform, monsters, consumables, entities):
        for m in monsters:
            if pygame.sprite.collide_rect(self, m) and not self.invul:
                m.attack(self)
                self.become_invul()
        if pygame.sprite.collide_rect(self, exitplatform):
            self.endlevel()
        for c in consumables:
            if self.collide_rum(c):
                consumables.remove(c)
                entities.remove(c)

    def endlevel(self):
        self.done = False
        self.winlevel = True

    def die(self):
        # with shelve.open('savefile') as db:
        # db['health'] = self.health
        self.done = False
        self.winlevel = False

    def shoot(self):
        if pygame.time.get_ticks() > self.last_shoot_time + self.SHOOT_CD:
            self.projectile = Projectile(self.rect.x+32, self.rect.y+20,
                                         'projectile.png', self.watching)
            self.last_shoot_time = pygame.time.get_ticks()

    def atack(self):
        if pygame.time.get_ticks() > self.last_atack + self.ATACK_CD:
            self.last_atack = pygame.time.get_ticks()
            self.sword.hidden = False
            if self.watching < 0:
                self.sword.image = pygame.image.load('swordleft.png')
            else:
                self.sword.image = pygame.image.load('sword.png')


    def become_invul(self):
        if pygame.time.get_ticks() > self.last_dmg + self.INVUL_TIME:
            self.invul = True
            self.last_dmg = pygame.time.get_ticks()
        else:
            return

    def check_invul_cd(self):
        if pygame.time.get_ticks() > self.last_dmg + self.INVUL_TIME:
            self.invul = False
        else:
            return

    def check_atacking(self):
        self.sword.rect.x = self.rect.x + WIDTH
        if self.watching<1:
            self.sword.rect.x = self.sword.rect.x - WIDTH - 20
        self.sword.rect.y = self.rect.y + HEIGHT / 2
        if pygame.time.get_ticks() > self.last_atack + 300:
            self.sword.hidden = True


class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load(filename)
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(x, y, 20, 20)
        self.damage = 5
        self.hidden = True

    def collide(self, monsters, platforms, spikesplatforms,
                entities, projectiles):
        for m in monsters:
            if pygame.sprite.collide_rect(self, m):
                m.health -= self.damage
        if self.hidden:
            entities.remove(self)
            projectiles.remove(self)

    def update(self, *args):
        self.collide(*args)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, watching):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 8))
        self.image = pygame.image.load(filename)
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(x, y, 8, 8)
        self.xvel = 5*watching
        self.damage = 5
        self.destruct = False

    def update(self, *args):
        self.rect.x += self.xvel
        self.collide(*args)

    def collide(self, monsters, platforms, spikesplatforms,
                entities, projectiles):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.destruct = True
        for sp in spikesplatforms:
            if pygame.sprite.collide_rect(self, sp):
                self.destruct = True
        for m in monsters:
            if pygame.sprite.collide_rect(self, m) and not self.destruct\
                    and not m.destruct:
                self.destruct = True
                m.health -= self.damage
        if self.destruct:
            entities.remove(self)
            projectiles.remove(self)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = pygame.image.load(filename)
        self.image.set_colorkey((0, 0, 0))
