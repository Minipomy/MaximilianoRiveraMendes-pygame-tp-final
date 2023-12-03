import pygame as pg
from auxiliar import SurfaceManager as sf
from constants import DEBUG

class Fruit(pg.sprite.Sprite):
    def __init__(self, fruit_data, location):
        super().__init__()

        #   Atributos de ubicacion y de imagen
        # self.pos_x = fruit_data.get("pos_x")
        # self.pos_y = fruit_data.get("pos_y")
        self.location = location
        
        #   Atributos de animacion
        self.idle = sf.get_surface_from_spritesheet(fruit_data.get("fruit_img"), 17, 1)
        self.frame_rate = fruit_data.get("frame_rate")
        self.initial_frame = 0
        self.image = self.idle[self.initial_frame]
        self.rect = self.image.get_rect(center = self.location)
        self.fruit_animation_time = 0

    #   Limitacion de FPS 
    def do_animation(self, delta_ms):
        self.fruit_animation_time += delta_ms
        if self.fruit_animation_time >= self.frame_rate:
            self.fruit_animation_time = 0
            if self.initial_frame < len(self.idle) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0

    def update(self, delta_ms):
        self.do_animation(delta_ms)

    def draw(self, screen):
        if DEBUG:
            pg.draw.rect(screen, 'yellow', self.rect)
        self.image = self.idle[self.initial_frame]
        screen.blit(self.image, self.rect)