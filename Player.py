import pygame as pg
from Projectile import Projectile
from auxiliar import SurfaceManager as sf
from constants import SCREEN_WIDTH, DEBUG, SCREEN_HEIGHT

class Player(pg.sprite.Sprite):
    def __init__(self, player_data):
        super().__init__()

        #   Imagenes del jugador
        self.__iddle_r = sf.get_surface_from_spritesheet(player_data.get("idle_img"), 11, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(player_data.get("idle_img"), 11, 1, flip=True)
        self.__run_r = sf.get_surface_from_spritesheet(player_data.get("run_img"), 12, 1)
        self.__run_l = sf.get_surface_from_spritesheet(player_data.get("run_img"), 12, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet(player_data.get("jump_img"), 1, 1)
        self.__jump_l = sf.get_surface_from_spritesheet(player_data.get("jump_img"), 1, 1, flip=True)

        #   Control de animaciones
        self.pos_x = player_data.get("pos_x") 
        self.pos_y = player_data.get("pos_y")
        self.location = (self.pos_x, self.pos_y)
        self.__initial_frame = 0
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__actual_animation = self.__iddle_r
        self.image = self.__actual_animation[self.__initial_frame]
        self.rect = self.image.get_rect(center = self.location)
        self.__is_looking_right = True

        #   Valores del jugador
        self.__move_x = player_data.get("coord_x")
        self.__move_y = player_data.get("coord_y")
        self.__speed_run = player_data.get("speed_run")
        self.__frame_rate = player_data.get("frame_rate")
        self.__bullet_data = player_data.get("bullet")
        self.__gravity = player_data.get("gravity")
        self.__jump = player_data.get("jump")
        self.life = player_data.get("life")
        self.last_damage = pg.time.get_ticks()
        self.damage_cooldown = 3000 
        self.invensible = False
        self.isOnFloor = False
        self.__is_jumping = False

        #   Valores balas del jugador
        self.laser_time = self.__bullet_data.get("laser_time")
        self.laser_cooldown = self.__bullet_data.get("laser_cooldown")
        self.ready = True
        self.bullet_group = pg.sprite.Group()

    ################ ANIMACIONES ################
    #   Funciones de control de animaciones del jugador
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
    
    #   Animacion caminando/corriendo
    def run(self, direction: str = 'Right'):
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

    def extra_life(self):
        self.life += 1

    def get_damage(self, entity):
        if entity.rect.colliderect(self.rect):
            self.life -= 1
            self.invensible = True

    #   El jugador dispara
    def attack(self):
        self.bullet_group.add(self.create_bullet())

    #   Crea una bala con el consturctor de Projectile
    def create_bullet(self):
        return Projectile(self.__bullet_data, self.rect.centerx, self.rect.centery, self.__is_looking_right)
    
    #   Tiempo de recarga y delay de disparo
    def recharge(self):
        if not self.ready:
            curent_time = pg.time.get_ticks()
            if curent_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    #   Controles de movimiento y disparo generales del jugador
    def do_movement(self, delta_ms):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.run('Right')
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.run('Left')
        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.stay()
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_s] and self.ready:
            self.attack()
            self.ready = False
            self.laser_time = pg.time.get_ticks()

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
            
    def is_on_platform(self, tile):
        self.isOnFloor = False
        if self.rect.top == tile.rect.bottom:
            self.rect.y += 0
        elif self.rect.bottom == tile.rect.top:
            self.rect.y += tile.rect.x
            self.isOnFloor = True
            print(self.isOnFloor)

    #   Limitacion de FPS 
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    
    def update(self, delta_ms, screen):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.draw(screen)
        self.recharge()
        self.bullet_group.draw(screen)
        self.bullet_group.update()
        
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            # pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.image = self.__actual_animation[self.__initial_frame]
        screen.blit(self.image, self.rect)