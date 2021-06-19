from pygame import *
MONSTER_SPEED = 1


class Monster(sprite.Sprite):
    def __init__(self, x, y, filename):  # конструктор: расположение объекта, файл с модел.
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image = image.load(filename)
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(x, y, 32, 32)
        self.xvel = 0
        self.movedistance = 200
        self.right = True
        self.left = False
        self.destruct = False
        self.hero_distance = 'away'
        self.health = 10
        self.stunned = False

    def move(self):
        if self.movedistance > 0:
            self.xvel = MONSTER_SPEED
            self.movedistance -= MONSTER_SPEED
        else:
            self.movedistance = 200
            self.left, self.right = self.right, self.left
        if self.right:
            self.rect.x += self.xvel
        else:
            self.rect.x -= self.xvel

    def come_to_hero(self):
        if self.distanceX > 0:
            self.rect.x -= self.xvel
        else:
            self.rect.x += self.xvel

    def attack(self, hero):
        hero.health-=1

    def check_hero_distance(self, hero):
        self.distanceX = self.rect.x-hero.rect.x
        self.distanceY = self.rect.y-hero.rect.y
        if 50 < abs(self.distanceX) < 200 and abs(self.distanceY) < 200:  # создать переменные и настроить дист.
            self.hero_distance = 'in_vision'
        elif abs(self.distanceX) <= 30:
            self.hero_distance = 'nearby'

    def update(self, hero, entities, movables, monsters):
        self.check_hero_distance(hero)
        if self.hero_distance == 'away':
            self.move()
        elif self.hero_distance == 'in_vision':
            self.come_to_hero()
        if self.health == 0:
            entities.remove(self)
            movables.remove(self)
            monsters.remove(self)
