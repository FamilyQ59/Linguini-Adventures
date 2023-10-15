import pygame, csv, os

Dirt = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Dirt.png'
Grass1 = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Grass_1.png'
Grass2 = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Grass_2.png'
Grass3 = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Grass_3.png'
Platform = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Platform.png'
blocks = [Grass1, Grass2, Grass3, Dirt, Platform]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    def __init__(self, filename):
        self.tile_size = 32
        self.start_pos = pygame.math.Vector2(0, 0)
        self.map_size = pygame.math.Vector2(0, 0)
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface(self.map_size)
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    @staticmethod
    def read_csv(filename):
        Map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                Map.append(list(row))
        return Map

    def load_tiles(self, filename):
        tiles = []
        Map = self.read_csv(filename)
        x, y = 0, 0
        for row in Map:
            x = 0
            for tile in row:
                for i in range(0, 5):
                    if tile == "0":
                        self.start_pos = (x * self.tile_size, y * self.tile_size)
                    elif tile == str(i + 1):
                        tiles.append(Tile(blocks[i],  x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1

        self.map_size = (x * self.tile_size, y * self.tile_size)
        return tiles
