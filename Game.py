import pygame as pg
import json as js
from Enemy import Enemy
from constants import *
from Player import Player

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
        pass
    def pause(self):
        pass
    def play(self):
        pass    
    def options(self):
        pass

    def run(self):
        while True:
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