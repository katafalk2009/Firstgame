"""
Module, responsible for camera issues.
"""
from pygame import Rect
WIN_WIDTH = 800
WIN_HEIGHT = 640
BG_COLOUR = (0, 100, 50)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):  # функция, которая двигает все объекты вслед за уровнем
        return target.rect.move(self.state.topleft)

    def update(self, target):  # функция сдвигает квадрат уровня относительно экрана
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # функция центрирования камеры
    w, h = camera.width, camera.height
    l, t = -target_rect.x + WIN_WIDTH / 2, -target_rect.y + WIN_HEIGHT / 2  # двигаем уровень вверх и влево от героя
    l = min(0, l)  # Не движемся дальше левой границы
    t = min(0, t)  # Не движемся дальше верхней границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    return Rect(l, t, w, h)
