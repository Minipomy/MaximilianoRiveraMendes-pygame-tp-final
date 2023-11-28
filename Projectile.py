import pygame as pg

class Projectile:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 10, 10)

    def update(self):
        self.rect.move_ip(0, -2)

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 0), self.rect)