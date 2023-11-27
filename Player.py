import pygame as pg
from auxiliar import SurfaceManager as sf
from constants import SCREEN_WIDTH, DEBUG

class Player(pg.sprite.Sprite):
    def __init__(self, player_data, frame_rate = 60, speed_run = 12, gravity = 16, jump = 32):
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet(player_data.get("idle"), 11, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(player_data.get("idle"), 11, 1, flip=True)
        self.__run_r = sf.get_surface_from_spritesheet(player_data.get("run"), 12, 1)
        self.__run_l = sf.get_surface_from_spritesheet(player_data.get("run"), 12, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet(player_data.get("jump"), 1, 1)
        self.__jump_l = sf.get_surface_from_spritesheet(player_data.get("jump"), 1, 1, flip=True)
        self.__move_x = player_data.get("coord_x")
        self.__move_y = player_data.get("coord_y")
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

    
    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True
    
    def run(self, direction: str = 'Right'):
        self.__initial_frame = 0
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    
    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    def jump(self, jumping=True):
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()
    
    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < SCREEN_WIDTH - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move


    def do_movement(self, delta_ms):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.run('Right')
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.run('Left')
        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.stay()

        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.__rect.y < 300:
                self.__rect.y += self.__gravity
        print(self.__rect.x)
        # print(self.__move_x)

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0
    
    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        
    
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            # pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)