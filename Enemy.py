import random
import pygame as pg
from auxiliar import SurfaceManager as sf
from constants import SCREEN_WIDTH, DEBUG, SCREEN_HEIGHT

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_data):
        super().__init__()
        
        # Imagenes del enemigo segun estado
        self.__iddle_r = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1, flip=True)
        self.__run_r = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1)
        self.__run_l = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1, flip=True)
        
        # Valores del enemigo 
        self.__move_x = 0
        self.__move_y = 0
        self.__location = (enemy_data.get("coord_x"), enemy_data.get("coord_y"))
        self.__speed_run = enemy_data.get("speed_run")
        self.__gravity = enemy_data.get("gravity")
        self.__frame_rate = enemy_data.get("frame_rate")
        self.__is_jumping = False

        # Atributos de control de animaciones
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.image = self.__actual_animation[self.__initial_frame]
        self.rect = self.image.get_rect(center = self.__location)
        self.__is_looking_right = True

    ################ ANIMACIONES ################
    #   Funciones de control de animaciones del enemigo
    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        # self.__move_y = -self.__jump
        self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        # self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        # self.__is_jumping = True
    
    #   Animacion caminando/corriendo
    def run(self, direction: str = 'Right'):
        self.__initial_frame = 0
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    
    #   Animacion estando quieto
    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    #   Animacion de salto
    def jump(self, jumping=True):
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()
    
    #   Seteo de limites de pantalla
    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.x < SCREEN_WIDTH - self.image.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move

    ################ ACCIONES / MOVIMIENTOS GENERALES ################
    #   Controles de movimiento y disparo generales del jugador
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.rect.x += self.__set_borders_limits()
            self.rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y += self.__gravity
            if self.rect.y < SCREEN_HEIGHT - self.image.get_height():
                self.rect.y += self.__gravity

    #   Limitacion de FPS 
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    
    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
    
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            # pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.image = self.__actual_animation[self.__initial_frame]
        screen.blit(self.image, self.rect)