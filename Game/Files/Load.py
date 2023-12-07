import pygame
from CSV_TileAmountBlocks import CountTiles
import os


class Level_Selection:
    def __init__(self):
        # Screen
        self.TitleScreen = [pygame.image.load(os.path.join('../Images/Title_1.png')),
                            pygame.image.load(os.path.join('../Images/Title_2.png')),
                            pygame.image.load(os.path.join('../Images/Title_3.png')),
                            pygame.image.load(os.path.join('../Images/Title_4.png'))]

        self.Controls_Screen = os.path.join("../Images/Controls.png")

        self.N = [pygame.image.load(os.path.join("../Images/N_1.png")),
                  pygame.image.load(os.path.join("../Images/N_2.png")),
                  pygame.image.load(os.path.join("../Images/N_3.png")),
                  pygame.image.load(os.path.join("../Images/N_4.png"))]
        # Tiles
        self.black = pygame.image.load(
            os.path.join("../Images/Black.png")
        )
        self.blue = pygame.image.load(
            os.path.join("../Images/Blue.png")
        )
        self.brown = pygame.image.load(
            os.path.join("../Images/Brown.png")
        )
        self.gray = pygame.image.load(
            os.path.join("../Images/Gray.png")
        )
        self.green = pygame.image.load(
            os.path.join("../Images/Green.png")
        )
        self.lefttop_corner = pygame.image.load(
            os.path.join("../Images/Left-top_corner.png")
        )
        self.leftwall = pygame.image.load(
            os.path.join("../Images/Left_wall.png")
        )
        self.light_blue = pygame.image.load(
            os.path.join("../Images/Light_Blue.png")
        )
        self.orange = pygame.image.load(
            os.path.join("../Images/Orange.png")
        )
        self.pink = pygame.image.load(
            os.path.join("../Images/Pink.png")
        )
        self.purple = pygame.image.load(
            os.path.join("../Images/Purple.png")
        )
        self.red = pygame.image.load(
            os.path.join("../Images/Red.png")
        )
        self.rightTop_corner = pygame.image.load(
            os.path.join("../Images/Right-Top_corner.png")
        )
        self.right_wall = pygame.image.load(
            os.path.join("../Images/Right_wall.png")
        )
        self.whiteFloor = pygame.image.load(
            os.path.join("../Images/White floor.png")
        )
        self.wine = pygame.image.load(
            os.path.join("../Images/Wine.png")
        )
        self.yellow = pygame.image.load(
            os.path.join("../Images/Yellow.png")
        )
        self.blocks = [self.black, self.blue, self.brown, self.gray, self.green, self.lefttop_corner, self.leftwall
                       , self.light_blue, self.orange, self.pink, self.purple, self.red, self.rightTop_corner,
                       self.right_wall, self.whiteFloor, self.wine, self.yellow]
        self.block_amount = len(self.blocks)
        self.csv = os.path.join("../Files/Level-Selection.csv")
        self.blockNum = CountTiles(self.csv)

        # Doors
        self.black_door = pygame.image.load(
            os.path.join("../Images/Black_door.png")
        )
        self.blue_door = pygame.image.load(
            os.path.join("../Images/Blue_door.png")
        )
        self.green_door = pygame.image.load(
            os.path.join("../Images/Green_door.png")
        )
        self.pink_door = pygame.image.load(
            os.path.join("../Images/Pink_door.png")
        )
        self.orange_door = pygame.image.load(
            os.path.join("../Images/Orange_door.png")
        )
        self.purple_door = pygame.image.load(
            os.path.join("../Images/Purple_door.png")
        )
        self.red_door = pygame.image.load(
            os.path.join("../Images/red_door.png")
        )
        self.wine_door = pygame.image.load(
            os.path.join("../Images/Wine_door.png")
        )
        self.doors = [self.black_door, self.red_door, self.blue_door, self.green_door, self.purple_door, self.pink_door,
                      self.orange_door, self.wine_door]
        self.door_size = pygame.math.Vector2(128, 128)
        self.door_position_x = [64, 256, 448, 640, 832, 1024, 1218, 1410]
        self.door_position_y = 352
        self.door_hitbox = ["", "", "", "", ""]

        # Enemy Test
        self.enemy_testCSV = os.path.join("../Files/Enemy_test.csv")
        self.Level_1 = os.path.join("../Files/Level1.csv")
        self.Level_1_tileNum = CountTiles(self.Level_1)
        self.Level_2 = os.path.join("../Files/Level2.csv")
        self.Level_2_tileNum = CountTiles(self.Level_2)
        self.Level_3 = os.path.join("../Files/Level3.csv")
        self.Level_3_tileNum = CountTiles(self.Level_3)
        self.Level_4 = os.path.join("../Files/Level4.csv")
        self.Level_4_tileNum = CountTiles(self.Level_4)
        self.Level_5 = os.path.join("../Files/Level5.csv")
        self.Level_5_tileNum = CountTiles(self.Level_5)
        self.Level_6 = os.path.join("../Files/Level6.csv")
        self.Level_6_tileNum = CountTiles(self.Level_6)
        self.Level_7 = os.path.join("../Files/Level7.csv")
        self.Level_7_tileNum = CountTiles(self.Level_7)
        self.Level_8 = os.path.join("../Files/Level8.csv")
        self.Level_8_tileNum = CountTiles(self.Level_8)

        # Level Doors
        self.Level_doors = [pygame.image.load(os.path.join("../Images//1_RedDoor.png")),
                            pygame.image.load(os.path.join("../Images/2_BlueDoor.png")),
                            pygame.image.load(os.path.join("../Images/3_GreenDoor.png.")),
                            pygame.image.load(os.path.join("../Images/4_PurpleDoor.png.")),
                            pygame.image.load(os.path.join("../Images/5_PinkDoor.png.")),
                            pygame.image.load(os.path.join("../Images/6_OrangeDoor.png.")),
                            pygame.image.load(os.path.join("../Images/7_WineDoor.png.")),
                            pygame.image.load(os.path.join("../Images/8_YellowDoor.png."))]


SelectLvl = Level_Selection()
