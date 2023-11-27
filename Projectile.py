import pygame as pg

class Projectile(pg.sprite.Sprite):
    def __init__(self,) -> None:
        super().__init__()
        self.image = ""
        self.y = y
        self.x = x
        self.rect = self.image.get_rect()