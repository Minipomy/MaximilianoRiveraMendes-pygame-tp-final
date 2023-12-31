import sys
import pygame as pg
import json as js
from Stage import Stage
from Buttons import Buttons
from functions import *
from constants import *

class Menu:
    def __init__(self, json_file):
        
        #   Archivo de configuracion
        data = open(json_file)
        self.json = js.load(data)

        #   Atributos de control de pygame
        pg.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.stages = self.json.get("stages")
        self.stage_selected = self.stages.get("stage_1")
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)
        self.caption = pg.display.set_caption(CAPTION)
        self.font = pg.font.Font(FONT, 36)
        self.volume = 1.0
        pg.font.init()

        self.highscore = 0
        #   Atributos de control de juego
        # self.is_game_select = False
        # self.is_in_option = False

    def main_menu(self, main_menu=True):
        createTable()
        while main_menu:
            MOUSE = pg.mouse.get_pos()
            MENU_TEXT = self.font.render(MAIN_MENU_TEXT, True, PRIMARY_ACCENT)
            MENU_RECT = MENU_TEXT.get_rect(center=(340, 100))
            PLAY_BUTTON = Buttons(pos=(340, 250), text_input=PLAY_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            OPTIONS_BUTTON = Buttons(pos=(340, 400), text_input=OPTIONS_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            QUIT_BUTTON = Buttons(pos=(340, 550), text_input=CLOSE_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.highscore = load_score()

            y_pos = 250
            draw_text(self.font, f"Highscore", PRIMARY_ACCENT, self.screen, SCREEN_WIDTH//2, 210)
            for score in self.highscore:
                # highscore.get("highscore")
                nombre = score.get("nombre")
                puntaje = score.get("puntaje")
                mensaje = f"{nombre} {puntaje}"
                y_pos += 40
                draw_text(self.font, f"{mensaje}", TEXT_COLOR, self.screen, SCREEN_WIDTH//2, y_pos)
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(MOUSE):
                            self.game_select(True)
                        if OPTIONS_BUTTON.checkForInput(MOUSE):
                            self.options(True)
                        if QUIT_BUTTON.checkForInput(MOUSE):
                            pg.quit()
                            sys.exit()
            pg.display.flip()

    def game_select(self, game_select=True):
        while game_select:
            MOUSE = pg.mouse.get_pos()
            SELECT_GAME_TEXT = self.font.render(SELECT_STAGE_TEXT, True, PRIMARY_ACCENT)
            SELECT_STAGE_MENU = SELECT_GAME_TEXT.get_rect(topleft=(20, 20))
            STAGE_1 = Buttons(pos=(640, 250), text_input=STAGE_1_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            STAGE_2 = Buttons(pos=(640, 400), text_input=STAGE_2_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            STAGE_3 = Buttons(pos=(640, 550), text_input=STAGE_3_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            CLOSE = Buttons(pos=(640, 700), text_input=CLOSE_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0, 0, 0))
            self.screen.blit(SELECT_GAME_TEXT, SELECT_STAGE_MENU)
            for button in [STAGE_1, STAGE_2, STAGE_3, CLOSE]:
                button.changeColor(MOUSE)
                button.update(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if STAGE_1.checkForInput(MOUSE):
                        self.stage_selected = self.stages.get("stage_1")
                        Stage(self.stage_selected, self.font, self.screen, self.size, self.volume).stage_run()
                    if STAGE_2.checkForInput(MOUSE):
                        self.stage_selected = self.stages.get("stage_2")
                        Stage(self.stage_selected, self.font, self.screen, self.size, self.volume).stage_run()
                    if STAGE_3.checkForInput(MOUSE):
                        self.stage_selected = self.stages.get("stage_3")
                        Stage(self.stage_selected, self.font, self.screen, self.size, self.volume).stage_run()
                    if CLOSE.checkForInput(MOUSE):
                        game_select = False
            pg.display.update()            

    def options(self, option_menu=True):
        while option_menu:
            MOUSE = pg.mouse.get_pos()
            CLOSE = Buttons(pos=(640, 700), text_input=CLOSE_TEXT, font=self.font, base_color=BUTTON_BASE_COLOR, hovering_color=HOVER_COLOR)
            self.screen.fill((0,0,0))
            draw_text(self.font, OPTION_MENU_TEXT, PRIMARY_ACCENT, self.screen, 20, 20)
            draw_text(self.font, f"Press - for Lower values", TEXT_COLOR, self.screen, SCREEN_WIDTH//2-450, SCREEN_HEIGHT//2-60)
            draw_text(self.font, f"Volume value [{(self.volume * 100):.0F}]", TEXT_COLOR, self.screen, SCREEN_WIDTH//2-450, SCREEN_HEIGHT//2)
            draw_text(self.font, f"Press = for Higher values", TEXT_COLOR, self.screen, SCREEN_WIDTH//2-450, SCREEN_HEIGHT//2+60)
            keys = pg.key.get_pressed()
            for button in [CLOSE]:
                button.changeColor(MOUSE)
                button.update(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if CLOSE.checkForInput(MOUSE):
                        option_menu=False
            if keys[pg.K_MINUS]:
                pg.time.delay(50)
                self.volume -= 0.1
                if self.volume <= 0.0:
                    self.volume = 0.0
            if keys[pg.K_EQUALS]:
                pg.time.delay(50)
                self.volume += 0.1
                if self.volume >= 1.0:
                    self.volume = 1.0
            pg.display.update()