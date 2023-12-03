import pygame as pg
from constants import SPRITE_SIZE
class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = pg.transform.scale(surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                ), SPRITE_SIZE)

                if flip:
                    frame_surface = pg.transform.scale(pg.transform.flip(frame_surface, True, False), SPRITE_SIZE)
                sprites_list.append(frame_surface)
        return sprites_list