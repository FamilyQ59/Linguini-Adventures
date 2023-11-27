import pygame
from CSV_TileAmountBlocks import CountTiles
import os


def import_images(image_folder, image_list):
    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):  # You can change the file extension as needed
            # Load the image and add it to the list
            image_path = os.path.join(image_folder, filename)
            image = pygame.image.load(image_path)
            image_list.append(image)
    return image_list


class Level_Selection:
    def __init__(self):
        # Tiles
        self.black = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Black.png"
        )
        self.blue = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Blue.png"
        )
        self.brown = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Brown.png"
        )
        self.gray = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Gray.png"
        )
        self.green = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Green.png"
        )
        self.lefttop_corner = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Left-top_corner.png"
        )
        self.leftwall = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Left_wall.png"
        )
        self.light_blue = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Light_Blue.png"
        )
        self.orange = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Orange.png"
        )
        self.pink = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Pink.png"
        )
        self.purple = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Purple.png"
        )
        self.red = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Red.png"
        )
        self.rightTop_corner = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Right-Top_corner.png"
        )
        self.rightwall = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Right_wall.png"
        )
        self.whiteFloor = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/White floor.png"
        )
        self.wine = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Wine.png"
        )
        self.yellow = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Colors/Yellow.png"
        )
        self.blocks = [self.black, self.blue, self.brown, self.gray, self.green, self.lefttop_corner, self.leftwall
                       , self.light_blue, self.orange, self.pink, self.purple, self.red, self.rightTop_corner,
                       self.rightwall, self.whiteFloor, self.wine, self.yellow]
        self.block_amount = len(self.blocks)
        self.csv = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Files/CSV_files/Level-Selection.csv'
        self.blockNum = CountTiles(self.csv)

        # Doors
        self.black_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Black_door.png"
        )
        self.blue_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Blue_door.png"
        )
        self.green_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Green_door.png"
        )
        self.orange_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Orange_door.png"
        )
        self.pink_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Pink_door.png"
        )
        self.purple_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Purple_door.png"
        )
        self.red_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/red_door.png"
        )
        self.wine_door = pygame.image.load(
            "C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/level-selection/Color_Doors/Wine_door.png"
        )
        self.doors = [self.black_door, self.red_door, self.blue_door, self.green_door, self.purple_door, self.pink_door,
                      self.orange_door, self.wine_door]
        self.door_size = pygame.math.Vector2(128, 128)
        self.door_position_x = [64, 256, 448, 640, 832, 1024, 1218, 1410]
        self.door_position_y = 352
        self.door_hitbox = ["", "", "", "", ""]

        # Enemy Test
        self.enemy_testCSV = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Files/CSV_files/Enemy_test.csv'
        self.Level_1 = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Files/CSV_files/Level1.csv'
        self.Level_1_tileNum = CountTiles(self.Level_1)


SelectLvl = Level_Selection()
