import pygame as pg
import json as js
from Enemy import Enemy
from Player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAPTION, BACKGROUND_COLOR, FONT

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

    def main_menu(self, screen):
        while True:
            screen.fill((0,0,0))
            self.draw_text('main menu', self.font, (255, 255, 255), screen, 20, 20)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.update()

    def pause(self, screen):
        while True:
            screen.fill((0,0,0))
            self.draw_text('pause menu', self.font, (255, 255, 255), screen, 20, 20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.update()

    def play(self):
        self.run()    
    def options(self, screen):
        while True:
            screen.fill((0,0,0))
            self.draw_text('option menu', self.font, (255, 255, 255), screen, 20, 20)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.update()

    def draw_text(self, text, font, color, screen, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        screen.blit(textobj, textrect)
        
    def run(self):
        while True:
            self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            
            self.screen.fill(BACKGROUND_COLOR)
            player = self.player
            enemy = self.enemy
            player.update(self.delta_ms)
            player.draw(self.screen)
            enemy.update(self.delta_ms)
            enemy.draw(self.screen)
            pg.display.flip()

            self.clock.tick(60)  # Limita el juego a 60 FPS