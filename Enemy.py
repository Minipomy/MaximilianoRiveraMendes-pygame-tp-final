import random
import pygame as pg
from Projectile import Projectile
from auxiliar import SurfaceManager as sf
from constants import SCREEN_WIDTH, DEBUG, SCREEN_HEIGHT, BOSS_RUN, BOSS_IDLE

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_data, location, minion:bool=False):
        super().__init__()
        
        # Imagenes del enemigo segun estado
        self.iddle_r = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1)
        self.iddle_l = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1, flip=True)
        self.run_r = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1)
        self.run_l = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1, flip=True)
        
        #   Flag de Jefe 
        self.is_boss = enemy_data.get("is_boss")
        self.is_minion = minion

        self.enemy_data = enemy_data

        # Valores del enemigo 
        self.move_x = 0
        self.move_y = 0
        self.base_score_value = 155
        self.life = enemy_data.get("life")
        self.location = (location)
        self.speed_run = enemy_data.get("speed_run")
        self.gravity = enemy_data.get("gravity")
        self.frame_rate = enemy_data.get("frame_rate")
        # self.is_jumping = False
        self.is_alive = True

        # Atributos de control de animaciones
        self.player_move_time = 0
        self.player_animation_time = 0
        self.initial_frame = 0
        self.actual_animation = self.iddle_r
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect(center = self.location)
        self.is_looking_right = True
        self.direction = 1

        if self.is_boss:
            self.life *= 2
            self.speed_run *= 2
            self.base_score_value *= 15
            self.iddle_r = sf.get_surface_from_spritesheet(BOSS_IDLE, 11, 1)
            self.iddle_l = sf.get_surface_from_spritesheet(BOSS_IDLE, 11, 1, flip=True)
            self.run_r = sf.get_surface_from_spritesheet(BOSS_RUN, 6, 1)
            self.run_l = sf.get_surface_from_spritesheet(BOSS_RUN, 6, 1, flip=True)

        if self.is_minion:
            self.is_boss = False
            self.life = 1
            self.speed_run = 6 
            self.base_score_value = 20
    
            # Imagenes del enemigo segun estado
            self.iddle_r = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1)
            self.iddle_l = sf.get_surface_from_spritesheet(enemy_data.get("idle"), 9, 1, flip=True)
            self.run_r = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1)
            self.run_l = sf.get_surface_from_spritesheet(enemy_data.get("run"), 16, 1, flip=True)

    ################ ANIMACIONES ################
    #   Animaciones eje x
    def set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.move_x = move_x
        self.actual_animation = animation_list
        self.is_looking_right = look_r
    
    #   Animaciones eje Y
    def set_y_animations_preset(self):
        # self.move_y = -self.jump
        self.move_x = self.speed_run if self.is_looking_right else -self.speed_run
        # self.actual_animation = self.jump_r if self.is_looking_right else self.jump_l
        self.initial_frame = 0
        # self.is_jumping = True
    
    #   Seteo de limites de pantalla
    def set_borders_limits(self):
        pixels_move = 0
        if self.move_x > 0:
            pixels_move = self.move_x if self.rect.x < SCREEN_WIDTH - self.image.get_width() else 0
        elif self.move_x < 0:
            pixels_move = self.move_x if self.rect.x > 0 else 0
        return pixels_move

    #   Animacion caminando/corriendo
    def run(self, direction: str = 'Right'):
        self.initial_frame = 0
        match direction:
            case 'Right':
                look_right = True
                self.set_x_animations_preset(self.speed_run, self.run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.set_x_animations_preset(-self.speed_run, self.run_l, look_r=look_right)
    
    #   Animacion estando quieto
    def stay(self):
        if self.actual_animation != self.iddle_l and self.actual_animation != self.iddle_r:
            self.actual_animation = self.iddle_r if self.is_looking_right else self.iddle_l
            self.initial_frame = 0
            self.move_x = 0
            self.move_y = 0
    
    #   Animacion de salto
    def jump(self, jumping=True):
        if jumping and not self.is_jumping:
            self.set_y_animations_preset()
        else:
            self.is_jumping = False
            self.stay()

    ################ ACCIONES / MOVIMIENTOS GENERALES ################

    #   Enemigo recibe danio
    def get_damage(self, entity):
        if entity.rect.colliderect(self.rect):
            self.life -= 1
            self.invensible = True
            if self.life <= 0:
                self.is_alive = False

    def do_movement(self, delta_ms):
        self.player_move_time += delta_ms
        if self.player_move_time >= self.frame_rate:
            self.player_move_time = 0
            left_limit = 0
            right_limits = SCREEN_WIDTH - self.rect.width
            if self.rect.x <= left_limit:
                self.direction = 1
            elif self.rect.x >= right_limits:
                self.direction = -1
            self.rect.x += self.direction * self.speed_run
            # Parte relacionado a saltar
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y += self.gravity
            if self.rect.y < SCREEN_HEIGHT - self.image.get_height():
                self.rect.y += self.gravity   
        if self.direction == -1:
            self.actual_animation = self.run_r
        else:
            self.actual_animation = self.run_l

    #   Limitacion de FPS 
    def do_animation(self, delta_ms):
        self.player_animation_time += delta_ms
        if self.player_animation_time >= self.frame_rate:
            self.player_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0
    
    def update(self, delta_ms):
        if self.is_alive:
            self.do_movement(delta_ms)
            self.do_animation(delta_ms)
            self.image = self.actual_animation[self.initial_frame]
    
    # def draw(self, screen: pg.surface.Surface):
    #     if DEBUG:
    #         pg.draw.rect(screen, 'red', self.rect)
    #         # pg.draw.rect(screen, 'green', self.__rect.bottom)
    #     self.image = self.actual_animation[self.initial_frame]
    #     screen.blit(self.image, self.rect)