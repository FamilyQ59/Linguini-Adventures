from Map import *
from Player import *
import pygame

pygame.init()
Clock = pygame.time.Clock()
TargetFPS = 60


class MainGame:
    def __init__(self, file, blocks, numLimit):
        self.canvas_size = pygame.Vector2(640, 426)
        self.size = pygame.math.Vector2(640, 426)
        self.canvas = pygame.Surface(self.canvas_size)
        self.screen = pygame.display.set_mode(self.size)
        self.dt = Clock.tick(60) * .001 * TargetFPS
        self.run = True
        self.scroll = [0, 0]
        self.level, self.blocks, self.Amount_of_Blocks = file, blocks, numLimit
        self.true_scroll = [0, 0]
        self.map = Map()
        self.window = ""
        self.run_once = [0, 0, 0]

        # Doors
        self.door_hitbox = []
        self.doors_open = {i: False for i in range(0, 8)}

    def draw(self, Input):
        self.canvas.fill((119, 136, 153))
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)
        player.draw(self.canvas, self.scroll[0], self.scroll[1])
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.draw.rect(self.window, (255, 0, 0), (100, 50, player.life * 5, 10))
        pygame.display.update()

    def gameloop(self):
        while self.run:

            # Def screen scroll
            self.true_scroll[0] += (player.rect.x - self.true_scroll[0] - self.canvas_size .x / 2) / 20
            self.true_scroll[1] += (player.rect.y - self.true_scroll[1] - self.canvas_size.y / 2) / 20
            self.scroll = self.true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])

            # Quit Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        player.position = pygame.math.Vector2(100, 300)
                        self.run = False

            # Call variables and functions that must be in the loop
            self.dt = Clock.tick(60) * .001 * TargetFPS
            Input = pygame.key.get_pressed()
            player.begin_jump(Input)
            player.update(self.dt, self.map.tile_rects, Input)
            self.draw(Input)


player = Player()
