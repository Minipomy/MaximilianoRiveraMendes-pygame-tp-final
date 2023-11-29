import pygame as pg
from constants import *

class Projectile(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pg.Surface((50, 10))
        self.image.fill((255, 0, 0))
        # self.image = pg.image.load('./Recursos/Traps/player_laser.png')
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, direction):
        match direction:
            case True:
                self.rect.x += 20
                if self.rect.x >= SCREEN_WIDTH:
                    self.kill()
            case False:
                self.rect.x -= 20
                if self.rect.x <= 0:
                    self.kill()