import pygame as pg
from constants import CAPTION, SCREEN_HEIGHT, SCREEN_WIDTH
from Player import Player

class Game():
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        pg.init()
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)
        self.caption = pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()
        self.finished = False
        self.time_start = 240000 / 1000

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def counter(self):
        self.time_start -= 1
        if self.time_start <= 0:
            self.finished = True

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            player = Player()
            player.draw(self.screen)

            pg.display.flip()  # Actualiza la pantalla
            self.clock.tick(60)  # Limita el juego a 60 FPS