import pygame
import csv
import os


def WithinCharacterView(x, y, player_pos_x, player_pos_y):
    if (player_pos_x - x)**2 <= 252400:
        if -1000 <= (player_pos_y - y) <= 1000 and (player_pos_y - y)**2 <= 120076:
            return True
    return False


class Map:
    def __init__(self):
        self.map = []
        self.tile_rects = []
        self.once = True

    def draw(self, file, blocks, surface, Scroll_x, Scroll_y, Number_of_Blocks, player_pos_x, player_pos_y):
        if self.once:
            with open(os.path.join(file)) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    self.map.append(list(row))
                self.once = False

        self.tile_rects = []
        y = 0
        for layer in self.map:
            x = 0
            for tile in layer:
                for i in range(0, len(blocks)):
                    if tile == str(i) and WithinCharacterView(x*32, y*32, player_pos_x, player_pos_y):
                        surface.blit(blocks[i], (x * 32 - Scroll_x, y * 32 - Scroll_y))
                if tile != '-1' and len(self.tile_rects) < Number_of_Blocks:
                    self.tile_rects.append(pygame.Rect(x * 32, y * 32, 32, 32))
                x += 1
            y += 1
