import pygame as pg
from constants import *

class Projectile(pg.sprite.Sprite):
    def __init__(self, projectile_data, pos_x, pos_y, direction:bool):
        super().__init__()
        self.image = pg.Surface((projectile_data.get("size_x"), projectile_data.get("size_y")))
        self.image.fill((255, 0, 0))
        # self.image = pg.image.load('./Recursos/Traps/player_laser.png')
        self.direction = direction
        self.velocity = projectile_data.get("velocity")
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        match self.direction:
            case True:
                self.rect.x += self.velocity
                if self.rect.x >= SCREEN_WIDTH:
                    self.kill()
            case False:
                self.rect.x -= self.velocity
                if self.rect.x <= 0:
                    self.kill()