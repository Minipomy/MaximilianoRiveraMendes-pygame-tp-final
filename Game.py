import sys
import pygame as pg
import json as js
import time
from Enemy import Enemy
from Player import Player
from Projectile import Projectile
from Tile import Tile
from Buttons import Buttons
from constants import *

class Game():
    def __init__(self, json_file):
        data = open(json_file)
        self.json = js.load(data)
        pg.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)
        self.caption = pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()
        self.delta_ms = self.clock.tick(FPS)
        self.font = pg.font.Font(FONT, 36)
        pg.font.init()

        self.isPause = False
        self.isPlaying = False
        self.sprites = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.tile = pg.sprite.Group()
        self.player = Player(self.json.get("player"))

        #   Agregamos los enemigos y tiles al grupo
        self.enemy.add(Enemy(self.json.get("enemy")))
        self.tile.add(Tile(self.json.get("tile")))

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def main_menu(self):
        while True:
            MOUSE = pg.mouse.get_pos()
            MENU_TEXT = self.font.render(MAIN_MENU_TEXT, True, PRIMARY_ACCENT)
            MENU_RECT = MENU_TEXT.get_rect(center=(340, 100))
            PLAY_BUTTON = Buttons(pos=(340, 250), text_input=PLAY_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            OPTIONS_BUTTON = Buttons(pos=(340, 400), text_input=OPTIONS_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            QUIT_BUTTON = Buttons(pos=(340, 550), text_input=CLOSE_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(MOUSE):
                            # self.isPlaying = True
                            self.game_select()
                        if OPTIONS_BUTTON.checkForInput(MOUSE):
                            self.options()
                        if QUIT_BUTTON.checkForInput(MOUSE):
                            pg.quit()
                            sys.exit()
            pg.display.flip()

    def set_pause(self):
        while self.isPause:
            MOUSE = pg.mouse.get_pos()
            MENU_TEXT = self.font.render("Game Paused", True, PRIMARY_ACCENT)
            MENU_RECT = MENU_TEXT.get_rect(topleft=(20, 20))
            RESUME_BUTTON = Buttons(pos=(640, 250), text_input=RESUME_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            OPTIONS_BUTTON = Buttons(pos=(640, 400), text_input=OPTIONS_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            MAIN_MENU_BUTTON = Buttons(pos=(640, 550), text_input=MAIN_MENU_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [RESUME_BUTTON, OPTIONS_BUTTON, MAIN_MENU_BUTTON]:
                button.changeColor(MOUSE)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_p:
                            self.isPause = False
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if RESUME_BUTTON.checkForInput(MOUSE):
                            self.isPause = False
                        if OPTIONS_BUTTON.checkForInput(MOUSE):
                            self.options()
                        if MAIN_MENU_BUTTON.checkForInput(MOUSE):
                            self.isPlaying = False
                            self.main_menu()
            pg.display.flip()

    def game_select(self):
        while True:
            MOUSE = pg.mouse.get_pos()
            SELECT_GAME_TEXT = self.font.render("Select Stage", True, PRIMARY_ACCENT)
            SELECT_STAGE_MENU = SELECT_GAME_TEXT.get_rect(topleft=(20, 20))
            STAGE_1 = Buttons(pos=(140, 150), text_input="STAGE 1", font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            STAGE_2 = Buttons(pos=(440, 350), text_input="STAGE 2", font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            STAGE_3 = Buttons(pos=(140, 440), text_input="STAGE 3", font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(SELECT_GAME_TEXT, SELECT_STAGE_MENU)
            for button in [STAGE_1, STAGE_2, STAGE_3]:
                button.changeColor(MOUSE)
                button.update(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if STAGE_1.checkForInput(MOUSE):
                        self.isPlaying = True
                        self.run()
                    if STAGE_2.checkForInput(MOUSE):
                        self.isPlaying = True
                    if STAGE_3.checkForInput(MOUSE):
                        self.isPlaying = True

                
            pg.display.update()            

    def options(self):
        while True:
            self.screen.fill((0,0,0))
            self.draw_text('option menu',(255, 255, 255), self.screen, 20, 20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.update()

    def draw_text(self, text, color, screen, x, y):
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        screen.blit(textobj, textrect)
    
    def run(self):
        start_ticks = int(pg.time.get_ticks())
        while self.isPlaying:
            seconds = int((pg.time.get_ticks()-start_ticks)/1000)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.isPause = True
                        self.set_pause()

            self.screen.fill(BACKGROUND_COLOR)

            #   Generamos contador de tiempo en stage
            self.draw_text("Time: ", (255, 255, 255), self.screen, 20, 20)
            self.draw_text(str(seconds),(255, 255, 255), self.screen, 200, 20)
            
            for bullet in self.player.bullet_group:
                for enemy in self.enemy:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.kill()

            #   Agregamos los enemigos al Stage
            self.enemy.draw(self.screen)
            self.enemy.update(self.delta_ms)

            # #   Agregamos los Tiles al Stage
            self.tile.draw(self.screen)
            
            #   Agregamos el jugador al Stage
            for tile in self.tile:
                self.player.is_on_platform(tile)

            self.player.update(self.delta_ms, self.screen)

            #   Actualizacion de pantalla
            pg.display.flip()
            self.clock.tick(100)  # Limita el juego a 60 FPS