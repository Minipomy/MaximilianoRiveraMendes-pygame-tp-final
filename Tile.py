import pygame as pg
from constants import DEBUG

class Tile(pg.sprite.Sprite):
    def __init__(self, tile_data):
        super().__init__()
        self.pos_x = tile_data.get("pos_x")
        self.pos_y = tile_data.get("pos_y")
        self.location = (self.pos_x, self.pos_y)
        self.image = pg.image.load(tile_data.get("tile_img")).convert_alpha()
        self.rect = self.image.get_rect(center = self.location)

    
    def draw(self, screen):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            # pg.draw.rect(screen, 'green', self.rect.bottom)
        screen.blit(self.image, self.rect)