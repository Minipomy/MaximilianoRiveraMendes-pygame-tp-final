import pygame as pg
from Projectile import Projectile
from auxiliar import SurfaceManager as sf
from functions import draw_text
from constants import SCREEN_WIDTH, DEBUG, SCREEN_HEIGHT, DAMAGE_SFX, PG_LASER_SFX, PRIMARY_ACCENT

class Player(pg.sprite.Sprite):
    def __init__(self, player_data, volume):
        super().__init__()

        #   Imagenes del jugador
        self.iddle_r = sf.get_surface_from_spritesheet(player_data.get("idle_img"), 11, 1)
        self.iddle_l = sf.get_surface_from_spritesheet(player_data.get("idle_img"), 11, 1, flip=True)
        self.run_r = sf.get_surface_from_spritesheet(player_data.get("run_img"), 12, 1)
        self.run_l = sf.get_surface_from_spritesheet(player_data.get("run_img"), 12, 1, flip=True)
        self.jump_r = sf.get_surface_from_spritesheet(player_data.get("jump_img"), 1, 1)
        self.jump_l = sf.get_surface_from_spritesheet(player_data.get("jump_img"), 1, 1, flip=True)

        #   Control de animaciones
        # self.pos_x, self.pos_y = player_data.get("player_pos")[0], player_data.get("player_pos")[1] 
        self.location = (player_data.get("player_pos"))
        self.initial_frame = 0
        self.player_move_time = 0
        self.player_animation_time = 0
        self.actual_animation = self.iddle_r
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect(center = self.location)
        self.is_looking_right = True

        #   Control de audio
        self.laser_sfx = pg.mixer.Sound(PG_LASER_SFX)
        self.volume = volume

        #   Valores del jugador
        self.move_x = player_data.get("coord_x")
        self.move_y = player_data.get("coord_y")
        self.speed_run = player_data.get("speed_run")
        self.frame_rate = player_data.get("frame_rate")
        self.bullet_data = player_data.get("bullet")
        self.gravity = player_data.get("gravity")
        self.jump_strenght = player_data.get("jump")
        self.life = player_data.get("life")
        self.life_counter = 3
        self.is_alive = True
        self.isOnFloor = False
        self.is_jumping = False

        #   Valores balas del jugador
        self.laser_time = self.bullet_data.get("laser_time")
        self.laser_cooldown = self.bullet_data.get("laser_cooldown")
        self.ready = True
        self.bullet_group = pg.sprite.Group()

    ################ ANIMACIONES ################

    #   Animaciones eje X
    def set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.move_x = move_x
        self.actual_animation = animation_list
        self.is_looking_right = look_r
    #   Animaciones eje Y
    def set_y_animations_preset(self):
        self.move_y = -self.jump_strenght
        self.move_x = self.speed_run if self.is_looking_right else -self.speed_run
        self.actual_animation = self.jump_r if self.is_looking_right else self.jump_l
        self.initial_frame = 0
        self.is_jumping = True
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

    #   Jugador recibe vida
    def extra_life(self):
        self.life += 50
        self.life_counter += 1
    #   Jugador recibe danio
    def get_damage(self, entity, sound, screen, font):
        if entity.rect.colliderect(self.rect):
            self.life -= 2
            if self.life == 350:
                self.life_counter -= 1
                draw_text(font, "2 HP", PRIMARY_ACCENT, screen, self.rect.top - 20, self.rect.y)
                sound.play(0).set_volume(self.volume)
            elif self.life == 250:
                self.life_counter -= 1
                draw_text(font, "1 HP", PRIMARY_ACCENT, screen, self.rect.top - 20, self.rect.y)
                sound.play(0).set_volume(self.volume)
            elif self.life == 150:
                self.life_counter -= 1
                draw_text(font, "0 HP", PRIMARY_ACCENT, screen, self.rect.top - 20, self.rect.y)
                sound.play(0).set_volume(self.volume)
            elif self.life == 0:
                self.is_alive = False
        print(self.life)
    #   El jugador dispara
    def attack(self):
        self.laser_sfx.play().set_volume(self.volume)
        self.bullet_group.add(self.create_bullet())
    #   Crea una bala con el consturctor de Projectile
    def create_bullet(self):
        return Projectile(self.bullet_data, self.rect.centerx, self.rect.centery, self.is_looking_right)
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

        self.player_move_time += delta_ms
        if self.player_move_time >= self.frame_rate:
            self.player_move_time = 0
            self.rect.x += self.set_borders_limits()
            self.rect.y += self.move_y
            
            # Parte relacionado a saltar
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y += self.gravity
            if self.rect.y < SCREEN_HEIGHT - self.image.get_height():
                self.rect.y += self.gravity

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
        if self.is_alive:
            self.do_movement(delta_ms)
            self.do_animation(delta_ms)
            self.recharge()
            self.bullet_group.update()
            self.image = self.actual_animation[self.initial_frame]


    #   Dibujar jugador
    # def draw(self, screen: pg.surface.Surface):
    #     if DEBUG:
    #         pg.draw.rect(screen, 'red', self.rect)
    #     self.image = self.actual_animation[self.initial_frame]
    #     self.bullet_group.draw(screen)
    #     screen.blit(self.image, self.rect)