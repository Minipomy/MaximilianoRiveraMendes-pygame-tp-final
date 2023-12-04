import pygame as pg
import sys
from Player import Player
from Enemy import Enemy
from Fruit import Fruit
from Tile import Tile
from Buttons import Buttons
from functions import draw_text
from constants import *

class Stage:
    def __init__(self, stage_data, font, screen, size):
        #   Decoradores generales
        self.stage = stage_data
        self.screen = screen
        self.size = size
        self.font = font
        #pg.font.init()
        self.background = self.stage.get("BG_img")
        self.image = pg.transform.scale(pg.image.load(self.background), self.size)
        self.clock = pg.time.Clock()
        self.delta_ms = self.clock.tick(FPS)
        self.is_playing = True
        self.is_paused = False
        self.win = False

        #   Control de audio
        self.bg_sfx = pg.mixer.Sound(BG_SFX)
        self.collected_sfx = pg.mixer.Sound(COLLECT_SFX)
        self.damage_sfx = pg.mixer.Sound(DAMAGE_SFX)
        self.enemy_k_sfx = pg.mixer.Sound(ENEMY_DF_SFX)
        self.death_sfx = pg.mixer.Sound(DEATH_SFX)
        self.win_sfx = pg.mixer.Sound(WIN_SFX)
        self.win_vocal_sfx = pg.mixer.Sound(WIN_VOCAL_SFX)

        #   Atributos de clase Enemigos, Jugador, Tiles y Frutas
        self.player =  Player(self.stage.get("player")) 
        self.score = 0
        
        self.sprites = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.tile = pg.sprite.Group()
        self.fruit = pg.sprite.Group()

        self.enemy_counter = self.stage.get("enemy_count")
        self.tile_counter = self.stage.get("tile_count")
        self.fruit_counter = self.stage.get("fruit_count")
        self.add_sprite(self.player)        

        if self.is_playing:
            self.bg_sfx.play(-1)
            self.generate_enemies(self.enemy_counter)
            self.generate_fruits(self.fruit_counter)
            self.generate_tiles(self.tile_counter)

    def add_sprite(self, sprite):
        self.sprites.add(sprite) 

    def add_enemy(self, enemy):
        self.enemy.add(enemy) 
        
    def add_tile(self, tile):
        self.tile.add(tile)
    
    def add_fruit(self, fruit):
        self.fruit.add(fruit)

    def draw_grid(self):
        if DEBUG:
            tile_size = 47
            WHITE = (255, 255, 255)
            for line in range(0,29):
                pg.draw.line(self.screen, WHITE, (0, line * tile_size), (SCREEN_WIDTH, line * tile_size))
                pg.draw.line(self.screen, WHITE, (line * tile_size, 0), (line * tile_size, SCREEN_HEIGHT))

    def generate_fruits(self, counter):
        if len(self.fruit) == 0 and not self.win:
            for index in range(counter):
                fruit = Fruit(self.stage.get("fruit"), self.stage.get("fruit_pos")[index])
                self.add_sprite(fruit)
                self.add_fruit(fruit)

    def generate_enemies(self, counter):
        if len(self.enemy) == 0 and not self.win:
            for index in range(counter):
                enemy = Enemy(self.stage.get("enemy"), self.stage.get("enemy_pos")[index])
                self.add_sprite(enemy)
                self.add_enemy(enemy)

    def generate_tiles(self, counter):
        if len(self.tile) == 0 and not self.win:
            for index in range(counter):
                tile = Tile(self.stage.get("tile"), self.stage.get("tiles_pos")[index])
                self.add_sprite(tile)
                self.add_tile(tile)

    def set_pause(self):
        while self.isPause:
            MOUSE = pg.mouse.get_pos()
            MENU_TEXT = self.font.render(GAME_PAUSE_TEXT, True, PRIMARY_ACCENT)
            MENU_RECT = MENU_TEXT.get_rect(topleft=(20, 20))
            RESUME_BUTTON = Buttons(pos=(640, 250), text_input=RESUME_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            MAIN_MENU_BUTTON = Buttons(pos=(640, 550), text_input=MAIN_MENU_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [RESUME_BUTTON, MAIN_MENU_BUTTON]:
                button.changeColor(MOUSE)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_p:
                            self.is_pause = False
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if RESUME_BUTTON.checkForInput(MOUSE):
                            self.is_paused = False
                        if MAIN_MENU_BUTTON.checkForInput(MOUSE):
                            self.is_playing = False
            pg.display.flip()

    def are_ya_winning_son(self):
        while self.win:
            self.screen.fill((0,0,0))
            draw_text(self.font, YOU_WIN, TEXT_COLOR, self.screen, SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2 - 300)
            draw_text(self.font, f"Score: {self.score}", TEXT_COLOR, self.screen, SCREEN_WIDTH//2-180, SCREEN_HEIGHT//2)
            draw_text(self.font, f"Press SPACE to return to menu", TEXT_COLOR, self.screen, SCREEN_WIDTH//2-600, SCREEN_HEIGHT//2 + 100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    pg.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.bg_sfx.stop()
                        self.is_playing = False
                        self.win = False
            pg.display.update()

    def event_handler(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.is_paused = not self.is_paused
        
        #   Comprobamos si los enemigos colisionan con las balas de jugador
        for bullet in self.player.bullet_group:
            for enemy in self.enemy:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.get_damage(bullet)
                    bullet.kill()
                    if not enemy.is_alive:
                        enemy.kill()
                        self.score += enemy.base_score_value
                        self.enemy_counter -= 1
                        self.enemy_k_sfx.play()
            for tile in self.tile:
                if bullet.rect.colliderect(tile.rect):
                    bullet.kill()

        #   Comprobamos si el jugador colisiona con la fruta
        for fruit in self.fruit:
            if fruit.rect.colliderect(self.player):
                fruit.kill()
                self.player.extra_life()
                self.collected_sfx.play()

        #   Comprobamos si el jugador colisiona con el enemigo
        for enemy in self.enemy:
            if enemy.rect.colliderect(self.player):
                # now = pg.time.get_ticks()
                self.player.get_damage(enemy, self.damage_sfx)
                if not self.player.is_alive:
                    self.player.kill()

        #   Comprobamos las colisiones del jugador con respecto a las plataformas
        for tile in self.tile:
            if self.player.rect.colliderect(tile):
                #   Colision Pies y base
                if tile.rect.top - self.player.rect.bottom < 0:
                    self.player.rect.x, self.player.rect.y = self.player.rect.x, tile.rect.top
                    self.player.is_jumping = False  
                #   Colision Cabeza y base
                if tile.rect.bottom - self.player.rect.top < 0:
                    self.player.rect.x, self.player.rect.y = self.player.rect.x, tile.rect.bottom  
                #   Colision del lado de la izquierda de la plataforma
                if tile.rect.left - self.player.rect.right < 0:
                    self.player.rect.x, self.player.rect.y = self.player.rect.x, tile.rect.left  
                #   Colision del lado de la derecha de la plataforma
                if tile.rect.right - self.player.rect.left < 0:
                    self.player.rect.x, self.player.rect.y = self.player.rect.x, tile.rect.right 

        #   Comprobamos si se completo el juego
        if len(self.enemy) == 0 and not self.win:
            self.win = True
            self.win_sfx.play()
            pg.time.delay(200)
            self.win_vocal_sfx.play()
            self.are_ya_winning_son()

    def render_handler(self, ticks):
            #   Generamos el fondo de pantalla
            self.screen.blit(self.image, (0, 0))            
            #   Generamos contador de tiempo en stage
            seconds = int((pg.time.get_ticks() - ticks)/1000)
            draw_text(self.font, f"Time: {str(seconds)} ", PRIMARY_ACCENT, self.screen, 20, 20)
            # draw_text(self.font, str(seconds),PRIMARY_ACCENT, self.screen, 200, 20)
            draw_text(self.font, f"Score: {self.score}", PRIMARY_ACCENT, self.screen, 20, 60)
            self.sprites.update(self.delta_ms)

    def elements_handler(self):
        #   Agregamos los sprites al stage
        self.sprites.draw(self.screen)
        self.player.bullet_group.draw(self.screen)

    def stage_run(self):
            start_ticks = pg.time.get_ticks()
            while self.is_playing:
                self.event_handler()
                self.render_handler(start_ticks)
                self.elements_handler()
                #   Actualizacion de pantalla
                self.draw_grid()
                pg.display.flip()
                self.clock.tick(FPS)