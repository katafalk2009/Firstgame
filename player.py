
import shelve
from Firstgame.environment import RUM
from Firstgame.monsters import *
MOVE_SPEED = 5
JUMP_POWER = 10
WIDTH = 50
HEIGHT = 50
GRAVITY = 0.5


class Player(sprite.Sprite):
    SHOOT_CD = 1000
    INVUL_TIME = 2000
    ATACK_CD = 500

    def __init__(self, x, y, filename):  # конструктор: расположение объекта, файл с модел.
        sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load(filename)
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.watching = 1  # умножаем скорость 1 вправо, -1 влево
        self.winlevel = False
        self.done = True  # для проверки цикла игры
        with shelve.open('savefile') as db:
            self.health = db['health']
        self.destruct = False
        self.last_shoot_time = 0
        self.invul = False
        self.last_dmg = 0
        self.atacking = False
        self.last_atack = 0

    def update(self, left,  right, up, platforms, exitplatform, spikesplatforms, monsters, consumables, entities):
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
        self.collide(exitplatform, spikesplatforms, monsters, consumables, entities)
        self.rect.x += self.xvel
        self.collideplatforms(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collideplatforms(0, self.yvel, platforms)
        self.check_invul_cd()
        self.check_atacking()

    def collideplatforms(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
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

    def collide(self, exitplatform, spikesplatforms, monsters, consumables, entities):
        for sp in spikesplatforms:
            if sprite.collide_rect(self, sp) and (self.invul is not True):
                self.health -= 1
                self.become_invul()
        for m in monsters:
            if sprite.collide_rect(self, m) and not m.destruct and (self.invul is not True):
                if self.atacking:
                    pass
                else:
                    self.health -= 1
                    self.become_invul()
        if sprite.collide_rect(self, exitplatform):
            self.endlevel()
        for c in consumables:
            if sprite.collide_rect(self, c) and not c.destruct:
                if isinstance(c, RUM):
                    self.health += 1
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
        if time.get_ticks() > self.last_shoot_time + self.SHOOT_CD:
            self.projectile = Projectile(self.rect.x+32, self.rect.y+20, 'projectile.png', self.watching)
            self.last_shoot_time = time.get_ticks()
        else:
            return

    def atack(self):
        if time.get_ticks() > self.last_atack + self.ATACK_CD:
            self.last_atack = time.get_ticks()
            self.atacking = True
            self.sword = Sword(self.rect.x+WIDTH, self.rect.y+HEIGHT/2, 'sword.png', self.watching)
        else:
            return

    def become_invul(self):
        if time.get_ticks() > self.last_dmg + self.INVUL_TIME:
            self.invul = True
            self.last_dmg = time.get_ticks()
        else:
            return

    def check_invul_cd(self):
        if time.get_ticks() > self.last_dmg + self.INVUL_TIME:
            self.invul = False
        else:
            return

    def check_atacking(self):
        if self.atacking:
            self.sword.rect.x += self.xvel
            self.sword.rect.y += self.yvel
        if time.get_ticks() > self.last_atack + 300:
            if self.atacking:
                self.sword.destruct = True
            self.atacking = False


class Sword(sprite.Sprite):
    def __init__(self, x, y, filename, watching):
        sprite.Sprite.__init__(self)
        self.image = Surface((20, 20))
        self.image = image.load(filename)
        if watching < 0:
            self.image = transform.flip(self.image, True, False)
            x = x - WIDTH - 20
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, 20, 20)
        self.destruct = False
        self.damage = 5

    def collide(self, monsters, *args):
        for m in monsters:
            if sprite.collide_rect(self, m) and not self.destruct and not m.destruct:
                m.health -= self.damage

    def update(self, *args):
        self.collide(*args)


class Projectile(sprite.Sprite):
    def __init__(self, x, y, filename, watching):  # конструктор: расположение объекта, файл с модел.
        sprite.Sprite.__init__(self)
        self.image = Surface((8, 8))
        self.image = image.load(filename)
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, 8, 8)
        self.xvel = 5*watching
        self.destruct = False
        self.damage = 5

    def update(self, monsters, platforms, spikesplatforms):
        self.rect.x += self.xvel
        self.collide(monsters, platforms, spikesplatforms)

    def collide(self, monsters, platforms, spikesplatforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                self.destruct = True
        for sp in spikesplatforms:
            if sprite.collide_rect(self, sp):
                self.destruct = True
        for m in monsters:
            if sprite.collide_rect(self, m) and not self.destruct and not m.destruct:
                self.destruct = True
                m.health -= self.damage


class HealthBar(sprite.Sprite):
    def __init__(self, filename):  # конструктор: расположение объекта, файл с модел.
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image = image.load(filename)
        self.image.set_colorkey((0, 0, 0))
