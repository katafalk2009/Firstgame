"""
Module for environment. Platform types, different objects.
"""
from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y, img):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/%s" % (ICON_DIR, img))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.destruct = False


class ExitPlatform(Platform):
    pass


class SpikesPlatform(Platform):
    pass


class Consumables(sprite.Sprite):
    def __init__(self, x, y, filename):
        sprite.Sprite.__init__(self)
        self.image = Surface((16, 16))
        self.image.fill((0, 0, 0))
        self.image = image.load(filename)
        self.rect = Rect(x, y, 16, 16)
        self.destruct = False


class RUM(Consumables):
    pass
