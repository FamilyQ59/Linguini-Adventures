import csv
import os


def CountTiles(file):
    Tiles = []
    Tile_amount = 0
    with open(os.path.join(file)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            Tiles.append(list(row))

    y = 0
    for layer in Tiles:
        x = 0
        for tile in layer:
            if tile != "-1":
                Tile_amount += 1
            x += 1
        y += 1

    return Tile_amount

