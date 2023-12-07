from Main import *
from Enemies import *
from Load import *


class Level_Selection(MainGame):

    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        player.position = pygame.math.Vector2(100, 300)

    def draw(self, Input):
        self.canvas.fill((0, 0, 0))

        # Draw
        #   Draw Tiles
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1], self.Amount_of_Blocks
                      , player.position.x, player.position.y)

        #   Draw Doors
        for i in range(0, 8):
            if self.doors_open[i]:
                self.canvas.blit(SelectLvl.doors[i], (SelectLvl.door_position_x[i] - self.scroll[0],
                                                      352 - self.scroll[1]))
        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])
        self.collisions(pygame.key.get_pressed())

        # Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

    def lose(self):
        if player.position.y > 1000:
            self.run = False

    def collisions(self, key):
        for i in range(0, 8):
            self.doors_open[i] = True
        for i in range(0, 8):
            if self.doors_open[i] is True:
                self.door_hitbox.append(pygame.Rect(SelectLvl.door_position_x[i], SelectLvl.door_position_y
                                                    , SelectLvl.door_size.x, SelectLvl.door_size.y))
        for i in range(0, 8):
            # Door Interactions
            if self.doors_open[i]:
                if (player.rect.colliderect(self.door_hitbox[i]) and key[pygame.K_p] and self.run_once[0] == 0 or
                        player.rect.colliderect(self.door_hitbox[i]) and pygame.mouse.get_pressed()[2] and
                        self.run_once[0] == 0):
                    self.run_once[0] = 1
                    player.position = Spawn_Positions[i]
                    self.run = False
                    player.life -= 10
                    Levels[i].gameloop()

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
                        Title_Screen().gameloop()
                        self.run = False

            # Call variables and functions that must be in the loop
            self.dt = Clock.tick(60) * .001 * TargetFPS
            Input = pygame.key.get_pressed()
            player.begin_jump(Input)
            player.update(self.dt, self.map.tile_rects, Input)
            self.draw(Input)


class Enemy_test(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.soldier = Soldier((400, 392), "Left")
        self.phantom = Phantom((600, 350))
        self.ninja = Ninja((800, 388), 100, 3)
        self.vulture = Vulture((400, 250), 300)
        self.vulture2 = Vulture((300, 270), 150)
        self.vulture3 = Vulture((500, 290), 170)
        self.spikes = [Spike((600, 416)), Spike((632, 416)), Spike((664, 416))]
        self.hit_list = [0, 0, 0]
        self.phantoms = []
        player.position = pygame.math.Vector2(300, 300)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Draw Enemies
        self.soldier.draw(self.canvas, self.scroll[0], self.scroll[1])
        # self.phantom.draw(self.canvas, self.scroll[0], self.scroll[1])
        # self.ninja.draw(self.canvas, self.scroll[0], self.scroll[1])
        # self.vulture.draw(self.canvas, self.scroll[0], self.scroll[1])
        # self.vulture2.draw(self.canvas, self.scroll[0], self.scroll[1])
        # self.vulture3.draw(self.canvas, self.scroll[0], self.scroll[1])
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions()

    def Interactions(self):
        # Enemy Movement
        self.soldier.movement(300, 2, self.map.tile_rects)
        # self.phantom.loop(self.map.tile_rects)
        # self.ninja.Interactions(2, 300)
        # self.vulture.Interactions(300, self.map.tile_rects)
        # self.vulture2.Interactions(150, self.map.tile_rects)
        # self.vulture3.Interactions(170, self.map.tile_rects)

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.life <= 0:
            self.run = False


class Level1(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.phantoms = []
        self.spikes = [Spike((256, 864)), Spike((288, 864)), Spike((416, 864)), Spike((448, 864)), Spike((576, 864)),
                       Spike((608, 864)), Spike((352, 96)), Spike((512, 160)), Spike((704, 192)), Spike((1376, 544)),
                       Spike((1344, 544)), Spike((1312, 544)), Spike((1280, 544)), Spike((1248, 544))]
        self.ninja = Ninja((950, 516), 100, 2)
        self.ninja_2 = Ninja((950, 164), 100, 2)
        player.position = pygame.math.Vector2(100, 896)
        self.door = Level_doors((96, 32), 0)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Draw Spikes
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Ninja
        self.ninja.draw(self.canvas, self.scroll[0], self.scroll[1])
        self.ninja_2.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Doors
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Ninja
        self.ninja.Interactions(3)
        self.ninja_2.Interactions(3)

        # Door
        if (self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 or
                self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0):
            self.run_once[0] = 1
            player.position = Spawn_Positions[1]
            player.life -= 10
            Levels[1].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.life <= 0:
            player.life = 5
            self.ninja.life = 2
            self.ninja_2.life = 2
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(75, 896)


class Level2(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.phantoms = [Phantom((990, 730)), Phantom((430, 500)), Phantom((950, 308)), Phantom((472, 116))]
        self.spikes = [Spike((896, 832)), Spike((448, 704)), Spike((416, 576)), Spike((736, 608)), Spike((544, 448)),
                       Spike((576, 448)), Spike((608, 448)), Spike((544, 256)), Spike((512, 224)), Spike((896, 64))]
        player.position = pygame.math.Vector2(700, 928)
        self.door = Level_doors((704, -32), 1)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Spikes
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Phantom
        for phantom in self.phantoms:
            phantom.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Phantom
        for phantom in self.phantoms:
            phantom.loop(self.map.tile_rects)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0\
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[2]
            player.life -= 10
            Levels[2].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            for phantom in self.phantoms:
                phantom.life = 3
            player.life = 5
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(690, 928)


class Level3(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.spikes = [Spike((256, 736)), Spike((352, 736)), Spike((448, 704)),
                       Spike((544, 704)), Spike((1344, 576)), Spike((1088, 448)), Spike((896, 352)), Spike((800, 352)),
                       Spike((704, 352)), Spike((608, 352)), Spike((480, 320)), Spike((384, 288)), Spike((288, 256)),
                       Spike((96, 160)), Spike((160, 96)), Spike((512, 96)), Spike((768, 96)), Spike((1024, 96))]
        # Subir mas
        self.stationary_soldier = Soldier((1409, -27), "Left")
        self.moving_soldiers = [Soldier((896, 550), "Left"), Soldier((160, 166), "Left")]
        player.position = pygame.math.Vector2(700, 928)
        self.door = Level_doors((1280, 64), 2)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Spikes
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Soldier
        self.stationary_soldier.draw(self.canvas, self.scroll[0], self.scroll[1])
        for soldier in self.moving_soldiers:
            soldier.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Soldier
        self.stationary_soldier.movement(0, 0, self.map.tile_rects, False)
        self.moving_soldiers[0].movement(32, 3, self.map.tile_rects, True)
        self.moving_soldiers[1].movement(32, 3, self.map.tile_rects, True)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[3]
            player.life -= 10
            Levels[3].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            self.stationary_soldier.life = 3
            for soldier in self.moving_soldiers:
                soldier.life = 3
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(112, 800)


class Level4(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        player.position = pygame.math.Vector2(700, 928)
        self.Vultures = []
        self.door = Level_doors((1020, -64), 3)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Vultures
        for vulture in self.Vultures:
            vulture.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        if len(self.Vultures) <= 10:
            self.Vultures.append(Vulture((random.randint(300, 700), random.randint(600, 700)),
                                         random.randint(100, 400)))

        # Vulture
        for vulture in self.Vultures:
            vulture.Interactions(self.map.tile_rects, 500, 1376, 832)

            if vulture.life <= 0:
                self.Vultures.remove(vulture)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[4]
            player.life -= 10
            Levels[4].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(50, 408)


class Level5(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.phantoms = [Phantom((420, 80)), Phantom((575, 80)), Phantom((802, 96))]
        self.ninjas = [Ninja((116, 196), 75, 2), Ninja((176, 324), 75, 2),
                       Ninja((106, 452), 75, 2)]
        self.soldier = Soldier((800, 806), "Left")
        player.position = pygame.math.Vector2(700, 928)
        self.door = Level_doors((1344, 0), 4)

    def draw(self, Input):

        self.canvas.fill((47, 34, 82))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Phantoms
        for phantom in self.phantoms:
            phantom.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Ninjas
        for ninja in self.ninjas:
            ninja.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Soldier
        self.soldier.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Phantoms
        for phantom in self.phantoms:
            phantom.loop(self.map.tile_rects)

        # Ninja
        for ninja in self.ninjas:
            ninja.Interactions(2)

        # Soldier
        self.soldier.movement(0, 0, self.map.tile_rects, False)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[5]
            player.life -= 10
            Levels[5].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            for ninja in self.ninjas:
                ninja.life = 2
            for phantom in self.phantoms:
                phantom.life = 3
            self.run_once[0] = 0

            player.position = pygame.math.Vector2(256, 100)


class Level6(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.spikes = [Spike((128, 832)), Spike((256, 768)), Spike((160, 608)),
                       Spike((192, 608)), Spike((512, 704)), Spike((608, 704)), Spike((704, 640)), Spike((800, 640)),
                       Spike((864, 768)), Spike((960, 768)), Spike((1056, 704)), Spike((1152, 704)), Spike((1216, 608)),
                       Spike((1312, 608)),  Spike((896, 192)), Spike((1024, 192))]
        self.soldiers = [Soldier((224, 580), "Right"), Soldier((128, 580), "Left"),
                         Soldier((992, 4), "Right"), Soldier((896, 452), "Left"),
                         Soldier((992, 452), "Right")]
        self.ninjas = [Ninja((288, 68), 64, 2), Ninja((160, 260), 64, 2)]
        player.position = pygame.math.Vector2(700, 928)
        self.door = Level_doors((224, 448), 5)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Spikes
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Soldiers
        for soldier in self.soldiers:
            soldier.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Ninjas
        for ninja in self.ninjas:
            ninja.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Soldier
        for soldier in self.soldiers:
            soldier.movement(0, 0, self.map.tile_rects, False)

        # Ninja
        for ninja in self.ninjas:
            ninja.Interactions(3)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[6]
            player.life -= 10
            Levels[6].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            for soldier in self.soldiers:
                soldier.life = 3
            for ninja in self.ninjas:
                ninja.life = 2
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(192, 800)


class Level7(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.hit_list = [0, 0, 0]
        self.spikes = [Spike((352, 1056)), Spike((384, 1056)), Spike((704, 864))]
        self.soldier = Soldier((96, 772), "Right")
        self.phantom = Phantom((544, 896))
        self.ninjas = [Ninja((640, 676), 64, 2), Ninja((192, 196), 32, 2)]
        self.vultures = [Vulture((580, 192), 112), Vulture((560, 200), 112),
                         Vulture((576, 185), 112)]
        player.position = pygame.math.Vector2(700, 928)
        self.door = Level_doors((64, 96), 6)

    def draw(self, Input):

        self.canvas.fill((255, 255, 255))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Doors
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Spikes
        for spike in self.spikes:
            spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Soldier
        self.soldier.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Phantom
        self.phantom.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Ninjas
        for ninja in self.ninjas:
            ninja.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Vultures
        for vulture in self.vultures:
            vulture.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Soldier
        self.soldier.movement(0, 0, self.map.tile_rects, False)

        # Phantom
        self.phantom.loop(self.map.tile_rects)

        # Ninja
        for ninja in self.ninjas:
            ninja.Interactions(3)

        # Vulture
        for vulture in self.vultures:
            vulture.Interactions(self.map.tile_rects, 480, 704, 320)

            if vulture.life <= 0:
                self.vultures.remove(vulture)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            player.position = Spawn_Positions[7]
            player.life -= 10
            Levels[7].gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            self.soldier.life = 3
            self.phantom.life = 3
            for ninja in self.ninjas:
                ninja.life = 3
            self.run_once[0] = 0
            self.vultures = []
            self.vultures.append(Vulture((random.randint(560, 590), random.randint(180, 200)), 112))
            self.vultures.append(Vulture((random.randint(560, 590), random.randint(180, 200)), 112))
            self.vultures.append(Vulture((random.randint(560, 590), random.randint(180, 200)), 112))
            player.position = pygame.math.Vector2(288, 1376)


class Level8(MainGame):
    def __init__(self, file, blocks, blockNum):
        super().__init__(file, blocks, blockNum)
        self.map = DarkMap()
        self.hit_list = [0, 0, 0]
        self.spikes = [Spike((320, 64)), Spike((256, 288)), Spike((448, 256)), Spike((416, 256)), Spike((480, 256)),
                       Spike((512, 256)), Spike((736, 384)), Spike((608, 544)), Spike((384, 544)), Spike((256, 448)),
                       Spike((224, 640)), Spike((384, 672)), Spike((288, 928)), Spike((96, 1184)), Spike((576, 1216)),
                       Spike((544, 1216)), Spike((800, 1152))]
        self.phantoms = [Phantom((417, 996)), Phantom((704, 832))]
        player.position = pygame.math.Vector2(100, 896)
        self.door = Level_doors((320, 1248), 7)

    def draw(self, Input):

        self.canvas.fill((0, 0, 0))
        # Draw Map
        self.map.draw(self.level, self.blocks, self.canvas, self.scroll[0], self.scroll[1],
                      self.Amount_of_Blocks, player.position.x, player.position.y)

        # Door
        self.door.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Draw Player
        player.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Spikes
        for spike in self.spikes:
            if LittleLight(spike.position.x, spike.position.y, player.position.x, player.position.y):
                spike.draw(self.canvas, self.scroll[0], self.scroll[1])

        # Phantom
        for phantom in self.phantoms:
            phantom.draw(self.canvas, self.scroll[0], self.scroll[1])

        # UI
        pygame.draw.rect(self.canvas, (255, 0, 0), (10, 10, player.life * 25, 30))

        # Draw Canvas onto Window
        self.window = pygame.transform.scale(self.canvas, self.size)
        self.screen.blit(self.window, (0, 0))
        pygame.display.update()

        # Call onto loop
        self.Interactions(Input)

    def Interactions(self, Input):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
                    self.run = False

        # Phantom
        for phantom in self.phantoms:
            phantom.loop(self.map.tile_rects)

        # Door
        if self.door.Collisions() and Input[pygame.K_p] and self.run_once[0] == 0 \
                or self.door.Collisions() and pygame.mouse.get_pressed()[2] and self.run_once[0] == 0:
            self.run_once[0] = 1
            Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
            self.run = False

        # Reset player attacks
        if player.attacking is False:
            self.hit_list = [0, 0, 0]

        if player.position.y >= 1500:
            player.life -= 10

        if player.life <= 0:
            player.life = 5
            self.run_once[0] = 0
            player.position = pygame.math.Vector2(100, 0)


class Title_Screen:
    def __init__(self):
        self.screen_size = pygame.Vector2(640, 426)
        self.canvas = pygame.display.set_mode(self.screen_size)
        self.animation_index = 0
        self.mouse = pygame.mouse.get_pos()
        self.mouse_hitbox = pygame.Rect(self.mouse[0], self.mouse[1], 5, 5)
        self.button_hitbox = [
            pygame.Rect(277, 267, 75, 30), pygame.Rect(245, 304, 148, 30)
        ]
        self.run = True
        self.once = [0, 0, 0]
        self.N_animation = 0

    def draw(self):
        self.canvas.fill((255, 255, 255))

        self.canvas.blit(SelectLvl.TitleScreen[int(self.animation_index)], (0, 0))
        # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
        self.animation_index += 0.05
        if self.animation_index >= 4:
            self.animation_index = 0

        self.canvas.blit(SelectLvl.N[int(self.animation_index)], (563, 158))
        self.N_animation += 0.05
        if self.N_animation >= 4:
            self.N_animation = 0

        pygame.draw.rect(self.canvas, (255, 255,255), pygame.Rect(259, 348, 120, 30))

        pygame.display.update()

    def Interactions(self):
        self.mouse = pygame.mouse.get_pos()
        print(self.mouse)
        self.mouse_hitbox = pygame.Rect(self.mouse[0], self.mouse[1], 5, 5)

        if pygame.mouse.get_pressed()[0] is False:
            self.once = [0, 0, 0]

        if (check_collision(self.button_hitbox[0], self.mouse_hitbox) and pygame.mouse.get_pressed()[0]
                and self.once[0] == 0):
            self.once[0] = 1
            Level_Selection(SelectLvl.csv, SelectLvl.blocks, SelectLvl.blockNum).gameloop()
            self.run = False

        if (check_collision(self.button_hitbox[1], self.mouse_hitbox) and pygame.mouse.get_pressed()[0]
                and self.once[1] == 0):
            self.once[1] = 1
            Info(SelectLvl.Controls_Screen).gameloop()

    def gameloop(self):
        while self.run:
            # Quit Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        player.position = pygame.math.Vector2(100, 300)
                        self.run = False

            self.draw()
            self.Interactions()


class Info:
    def __init__(self, img_path):
        self.screen_size = pygame.Vector2(640, 426)
        self.canvas = pygame.display.set_mode(self.screen_size)
        self.run = True
        self.image = pygame.image.load(img_path)

    def draw(self):
        self.canvas.fill((255, 255, 255))
        self.canvas.blit(self.image, (0, 0))
        pygame.display.update()

    def gameloop(self):
        while self.run:
            # Quit Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        player.position = pygame.math.Vector2(100, 300)
                        self.run = False

            self.draw()


Levels = [Level1(SelectLvl.Level_1, SelectLvl.blocks, SelectLvl.Level_1_tileNum),
          Level2(SelectLvl.Level_2, SelectLvl.blocks, SelectLvl.Level_2_tileNum),
          Level3(SelectLvl.Level_3, SelectLvl.blocks, SelectLvl.Level_3_tileNum),
          Level4(SelectLvl.Level_4, SelectLvl.blocks, SelectLvl.Level_4_tileNum),
          Level5(SelectLvl.Level_5, SelectLvl.blocks, SelectLvl.Level_5_tileNum),
          Level6(SelectLvl.Level_6, SelectLvl.blocks, SelectLvl.Level_6_tileNum),
          Level7(SelectLvl.Level_7, SelectLvl.blocks, SelectLvl.Level_7_tileNum),
          Level8(SelectLvl.Level_8, SelectLvl.blocks, SelectLvl.Level_8_tileNum)]

Spawn_Positions = [pygame.math.Vector2(100, 896), pygame.math.Vector2(700, 928), pygame.math.Vector2(112, 800),
                   pygame.math.Vector2(50, 408), pygame.math.Vector2(256, 100), pygame.math.Vector2(192, 800),
                   pygame.math.Vector2(288, 1376), pygame.math.Vector2(100, 0)]

Title_Screen().gameloop()
