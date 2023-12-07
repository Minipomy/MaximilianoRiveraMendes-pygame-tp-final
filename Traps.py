import pygame as pg
from auxiliar import SurfaceManager as sf
from constants import SAW_ON

class Traps(pg.sprite.Sprite):
    def __init__(self, trap_data, location):
        super().__init__()
        self.on = sf.get_surface_from_spritesheet(trap_data.get("trap_img"), 3, 1, flip=True)
        self.trap_data = trap_data
        self.initial_frame = 0
        self.player_animation_time = 0
        self.actual_animation = self.on
        self.frame_rate = trap_data.get("frame_rate")
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect(center = location)

    #   Limitacion de FPS 
    def do_animation(self, delta_ms):
        self.player_animation_time += delta_ms
        if self.player_animation_time >= self.frame_rate:
            self.player_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0

    #   Actualizacion    
    def update(self, delta_ms):
        self.do_animation(delta_ms)
        self.image = self.actual_animation[self.initial_frame]