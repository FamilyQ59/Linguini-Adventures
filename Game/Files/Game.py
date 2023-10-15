from Tiles import *
from Player import Player
import pygame

pygame.init()
clock = pygame.time.Clock()
TargetFPS = 60
mapa = "Selva"


class Main:
    def __init__(self):
        self.size = pygame.Vector2(960, 640)
        self.canvas = pygame.Surface(self.size)
        self.window = pygame.display.set_mode(self.size)
        self.dt = clock.tick(60) * .001 * TargetFPS
        self.map = TileMap('Selva.csv')
        self.run = True

    def draw(self):
        self.canvas.fill((0, 144, 160))
        self.map.draw_map(self.canvas)
        player.draw(self.canvas)
        self.window.blit(self.canvas, (0, 0))
        pygame.display.update()

    def boundaries(self):
        if player.rect.x < 0:
            player.rect.x = 0
            player.position.x = 0
            player.acceleration.x = 0
            player.velocity.x = 0

        if player.rect.x > self.size.x - player.rect.w:
            player.rect.x = self.size.x - player.rect.w
            player.position.x = self.size.x - player.rect.w
            player.acceleration.x = 0
            player.velocity.x = 0

    def lose(self):
        if player.position.y > self.size.y:
            self.run = False

    def gameloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        self.run = False

            self.dt = clock.tick(60) * .001 * TargetFPS
            Input = pygame.key.get_pressed()
            player.begin_jump(Input)
            self.boundaries()
            player.update(self.dt, self.map.tiles, Input)
            self.lose()
            self.draw()


main = Main()
player = Player()
player.position.x, player.position.y = main.map.start_pos
main.gameloop()
