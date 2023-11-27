import sys
from tkinter import font
import pygame as pg
import json as js
from Enemy import Enemy
from Player import Player
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
        self.player = Player(json.get("player"))
        self.enemy = Enemy(json.get("enemy"))
        self.font = pg.font.Font(FONT, 36)
        pg.font.init()
        # self.finished = False
        # self.time_start = 240000 / 1000

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
            self.screen.fill((0,0,0))
            MENU_MOUSE_POS = pg.mouse.get_pos()
            MENU_TEXT = self.font.render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            PLAY_BUTTON = Buttons(pos=(640, 250), text_input=PLAY_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            OPTIONS_BUTTON = Buttons(pos=(640, 400), text_input=OPTIONS_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            QUIT_BUTTON = Buttons(pos=(640, 550), text_input=CLOSE_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.run()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pg.quit()
                        sys.exit()
            pg.display.update()

    def set_pause(self, pause):
        while pause:
            self.screen.fill((0,0,0))
            self.draw_text('pause menu',(255, 255, 255), self.screen, 20, 20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        pause = False
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
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.set_pause(True)
                
            self.screen.fill(BACKGROUND_COLOR)
            player = self.player
            enemy = self.enemy
            player.update(self.delta_ms)
            player.draw(self.screen)
            enemy.update(self.delta_ms)
            enemy.draw(self.screen)
            pg.display.flip()
            self.clock.tick(100)  # Limita el juego a 60 FPS