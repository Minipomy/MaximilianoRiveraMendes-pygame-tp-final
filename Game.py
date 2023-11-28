import sys
import pygame as pg
import json as js
from Enemy import Enemy
from Player import Player
from Projectile import Projectile
from Buttons import Buttons
from constants import *

class Game():
    def __init__(self, json_file):
        data = open(json_file)
        json = js.load(data)
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
        self.sprites = pg.sprite.Group()
        self.player = Player(json.get("player"))
        self.enemy = Enemy(json.get("enemy"))
        

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    # def counter(self):
    #     self.time_start -= 1
    #     if self.time_start <= 0:
    #         self.finished = True

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
                            self.run()
                        if OPTIONS_BUTTON.checkForInput(MOUSE):
                            self.options()
                        if QUIT_BUTTON.checkForInput(MOUSE):
                            pg.quit()
                            sys.exit()
            pg.display.flip()

    def set_pause(self):
        while self.isPause:
            MOUSE = pg.mouse.get_pos()
            RESUME_BUTTON = Buttons(pos=(640, 250), text_input=RESUME_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            OPTIONS_BUTTON = Buttons(pos=(640, 400), text_input=OPTIONS_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            MAIN_MENU_BUTTON = Buttons(pos=(640, 550), text_input=MAIN_MENU_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            # self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [RESUME_BUTTON, OPTIONS_BUTTON, MAIN_MENU_BUTTON]:
                button.changeColor(MOUSE)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if RESUME_BUTTON.checkForInput(MOUSE):
                            self.isPause = False
                        if OPTIONS_BUTTON.checkForInput(MOUSE):
                            self.options()
                        if MAIN_MENU_BUTTON.checkForInput(MOUSE):
                            self.main_menu()
            pg.display.flip()
            

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
        while True:
            bullets = []
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.isPause = True
                        self.set_pause()
                    if event.key == pg.K_s:
                        bullets.append(Projectile(self.player.__rect.x, self.player.__rect.y))
                        for bullet in bullets:
                            bullet.update()
                

                
            self.screen.fill(BACKGROUND_COLOR)
            player = self.player
            enemy = self.enemy
            player.update(self.delta_ms)
            player.draw(self.screen)
            for bullet in bullets:
                bullet.draw(self.screen)
            enemy.update(self.delta_ms)
            enemy.draw(self.screen)
            pg.display.flip()
            self.clock.tick(100)  # Limita el juego a 60 FPS