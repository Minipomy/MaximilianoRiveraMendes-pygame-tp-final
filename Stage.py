import pygame as pg
from Menu import Menu
from Player import Player
from Enemy import Enemy
from Fruit import Fruit
from Tile import Tile
from functions import draw_text
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class Stage(Menu):
    def __init__(self, stage_data):
        super().__init__(self)
        #   Decoradores generales
        self.stage = stage_data
        # self.screen = screen
        # self.size = size
        # self.font = font
#        pg.font.init()
        self.background = self.stage.get("BG_img")
        self.image = pg.transform.scale(pg.image.load(self.background), self.size)
        self.clock = pg.time.Clock()
        self.delta_ms = self.clock.tick(FPS)
        self.isPlaying = True

        #   Atributos de clase Enemigos, Jugador, Tiles y Frutas
        self.player =  Player(self.stage.get("player")) 
        
        self.sprites = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.tile = pg.sprite.Group()
        self.fruit = pg.sprite.Group()

        self.enemy_counter = self.stage.get("enemy_count")
        self.tile_counter = self.stage.get("tile_count")
        self.fruit_counter = self.stage.get("fruit_count")
        self.add_sprite(self.player)        
        
    def add_sprite(self, sprite):
        self.sprites.add(sprite) 

    def add_enemy(self, enemy):
        self.enemy.add(enemy) 
        
    def add_tile(self, tile):
        self.tile.add(tile)
    
    def add_fruit(self, fruit):
        self.fruit.add(fruit)

    def generate_fruits(self, counter):
        if len(self.fruit) == 0:
            for index in range(0,counter-1):
                fruit = Fruit(self.stage.get("fruit"), self.stage.get("fruit_pos")[index])
                self.add_sprite(fruit)
                self.add_fruit(fruit)

    def generate_enemies(self, counter):
        if len(self.enemy) == 0:
            for index in range(0,counter-1):
                enemy = Enemy(self.stage.get("enemy"), self.stage.get("enemy_pos")[index])
                self.add_sprite(enemy)
                self.add_enemy(enemy)

    def generate_tiles(self, counter):
        if len(self.tile) == 0:
            for index in range(0,counter-1):
                tile = Tile(self.stage.get("tile"), self.stage.get("tiles_pos")[index])
                self.add_sprite(tile)
                self.add_tile(tile)

    def event_handler(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.isPause = True
                        self.isPlaying = False
                        self.set_pause()

        #   Comprobamos si los enemigos colisionan con las balas de jugador
        for bullet in self.player.bullet_group:
            for enemy in self.enemy:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.get_damage(self.player)
                    if enemy.is_dead:
                        enemy.kill()
        
        #   Comprobamos si el jugador colisiona con la fruta
        for fruit in self.fruit:
            if fruit.rect.colliderect(self.player):
                fruit.kill()
                self.player.extra_life() 

        #   Comprobamos si el jugador colisiona con el enemigo
        for enemy in self.enemy:
            if enemy.rect.colliderect(self.player):
                # now = pg.time.get_ticks()
                self.player.get_damage(enemy)

    def render_handler(self, ticks):
            #   Generamos el fondo de pantalla
            self.screen.blit(self.image, (0, 0))            
            
            #   Generamos contador de tiempo en stage
            seconds = int((pg.time.get_ticks() - ticks)/1000)
            draw_text(self.font, "Time: ", (255, 255, 255), self.screen, 20, 20)
            draw_text(self.font, str(seconds),(255, 255, 255), self.screen, 200, 20)
            self.sprites.update(self.delta_ms)
            self.player.update(self.delta_ms)

    def elements_handler(self):
        self.generate_enemies(self.enemy_counter)
        self.generate_fruits(self.fruit_counter)
        self.generate_tiles(self.tile_counter)
        #   Agregamos los sprites al stage
        self.sprites.draw(self.screen)
        self.player.draw(self.screen)

    def stage_run(self):
        start_ticks = int(pg.time.get_ticks())
        while self.isPlaying:
            self.event_handler()
            self.render_handler(start_ticks)
            self.elements_handler()
            #   Actualizacion de pantalla
            pg.display.flip()
            self.clock.tick(60)