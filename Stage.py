import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Stage:
    def __init__(self, stage_data):
        self.background = stage_data.get("BG_img")

        #   Atributos de clase Enemigos, Jugador, Tiles y Frutas
        self.player =  Player(self.json.get("player")) 
        self.enemy = pg.sprite.Group()
        self.tile = pg.sprite.Group()
        self.fruit = pg.sprite.Group()

        #   Agregamos los enemigos, tiles y jugador
        self.enemy.add(Enemy(self.json.get("enemy")))
        self.tile.add(Tile(self.json.get("tile")))
        self.fruit.add(Fruit(self.json.get("fruit")))

    # Loop over both and blit accordingly
    def set_background(self, screen):
        tilesX, tilesY = self.background.get_size()
        for x in range(tilesX):
            for y in range(tilesY):
                screen.blit(self.background, (x * SCREEN_WIDTH, y * SCREEN_HEIGHT))

    def stage_run(self, screen):
        start_ticks = int(pg.time.get_ticks())
        while self.isPlaying:
            seconds = int((pg.time.get_ticks()-start_ticks)/1000)

            #   Control de eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.isPause = True
                        self.set_pause()

            self.draw(screen)

            #   Generamos contador de tiempo en stage
            self.draw_text("Time: ", (255, 255, 255), self.screen, 20, 20)
            self.draw_text(str(seconds),(255, 255, 255), self.screen, 200, 20)
            
            #   Actualizacion de pantalla
            pg.display.flip()
            self.clock.tick(100)  # Limita el juego a 60 FPS
