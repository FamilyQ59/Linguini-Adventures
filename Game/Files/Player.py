import pygame
from Load import import_images

linguini = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Assets/Linguini.png'
Linguini_Folder = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Assets/Linguini_Folder'
attack_folder = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Assets/Attack_Images'
attack_images = []
walk_images = []
scale = pygame.transform.scale

import_images(attack_folder, attack_images)
import_images(Linguini_Folder, walk_images)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Basic Variables
        self.image = pygame.image.load(linguini)
        self.rect = self.image.get_rect()

        # Movement Variables
        self.moving = False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .60, -.12
        self.position, self.velocity = pygame.math.Vector2(480, 320), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        # Draw Variables
        self.animation_index = {"attack": 0, "walk": 0}

        # Attack Variables
        self.attacking = False
        self.atktime = 0
        self.attack_cd = 0
        self.attack_cd_begin = False
        self.right, self.left = False, False
        self.range = pygame.Rect(self.position.x, self.position.y, 100, 50)
        self.attack_begin_side = [0, 0]
        self.life = 5

    def draw(self, display, scroll_x, scroll_y):
        # Draw Character
        if self.moving is False:
            display.blit(self.image, (self.rect.x - scroll_x, self.rect.y - scroll_y))
        if self.moving:
            display.blit(walk_images[int(self.animation_index["walk"])],
                         (self.rect.x - scroll_x, self.rect.y - scroll_y, self.rect.width, self.rect.height))
            # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
            self.animation_index["walk"] += 0.15
            if self.animation_index["walk"] >= 3:
                self.animation_index["walk"] = 0

        # Draw Attack
        if self.attacking:

            # Draw Attack to the Right
            if self.attack_begin_side == [1, 0]:
                # Draws attack (scales it, iterates through it (as an int), defines position and size)
                display.blit(scale(attack_images[int(self.animation_index["attack"])], (75, 50)),
                             (self.range.x - scroll_x, self.range.y - scroll_y, self.range.width, self.range.height))
                # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
                self.animation_index["attack"] += 1

            # Draws Attack to the Left
            elif self.attack_begin_side == [0, 1]:
                # Draws attack(flips it, scales it, iterates through it (as an int), defines position and size)
                display.blit(pygame.transform.flip(scale(attack_images[int(self.animation_index["attack"])],
                                                         (75, 50)), True, False),
                             (self.range.x - scroll_x, self.range.y - scroll_y, self.range.width, self.range.height))
                self.animation_index["attack"] += 1

    def update(self, dt, tiles, key):
        # Joins all functions into one to add to the main loop
        self.horizontal_motion(dt, key)
        self.check_X_collisions(tiles)
        self.vertical_motion(dt)
        self.check_Y_collision(tiles)
        self.attack(key)

    def horizontal_motion(self, dt, key):
        # Creates a smooth accelerations of the character
        self.acceleration.x = 0
        if key[pygame.K_d]:
            self.right, self.left = True, False
            self.acceleration.x += 3
            self.moving = True
        elif key[pygame.K_a]:
            self.right, self.left = False, True
            self.acceleration.x -= 3
            self.moving = True
        else:
            self.moving = False
            self.animation_index["walk"] = 0

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limitvel(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_motion(self, dt):
        # Creates a smooth jumping motion
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limitvel(self, max_vel):
        # In case that player is going left (velocity is neg), the min will choose vel, as it´s neg, but if it´s going
        # above max vel, it´ll chose -max vel as it´s closer to 0. In case the character is going right ( + vel), if
        # it´s going below the max_vel, the min will choose vel, and the max as well as it´s +, in case it´s going
        # faster than max vel, min will choose max_vel, and max will too.
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))

        # abs = absolute number; will stop player when it´s advancing too little, which will make movement better
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def begin_jump(self, key):
        # Checks the input for beginning the jump
        if key[pygame.K_SPACE]:
            self.jump()
        elif self.is_jumping:
            self.velocity.y *= .50
            self.is_jumping = False

    def jump(self):
        # Carries out the jumping
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 12
            self.on_ground = False

    def get_hits(self, tiles):
        # Returns a list of the tiles the player is colliding with
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_X_collisions(self, tiles):
        # Checks collisions for all the horizontal collisions with tiles
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.rect.w
                self.rect.x = self.position.x

            elif self.velocity.x < 0:
                self.position.x = tile.right
                self.rect.x = self.position.x

    def check_Y_collision(self, tiles):
        # Checks collisions for all the vertical collisions with tiles
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.bottom + self.rect.h
                self.rect.bottom = self.position.y

    def attack(self, key):
        # Carries out the attack motion
        if self.attacking:
            self.atktime += 1

        # Defines the attack hitbox depending on if player facing right or left (respectively)
        if self.attack_begin_side == [1, 0]:
            self.range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y - 15, 75, 50)
        if self.attack_begin_side == [0, 1]:
            self.range = pygame.Rect(self.rect.x - 75, self.rect.y - 15, 75, 50)

        # Resets array checking which side is player facing
        if self.attack_begin_side == [0, 0]:
            self.range = pygame.Rect(1000, 1000, 1, 1)

        # Takes attack input and checks if every cooldown is done
        if key[pygame.K_o] and self.attacking is False and not self.attack_cd_begin:
            if self.right:
                self.attack_begin_side = [1, 0]
            if self.left:
                self.attack_begin_side = [0, 1]
            self.attack_cd_begin = True
            self.attacking = True
        elif self.atktime == 5:
            self.attack_begin_side = [0, 0]
            self.attacking = False
            self.atktime = 0
            self.animation_index["attack"] = 0

        # Defines cooldown for first attack
        if self.attack_cd_begin:
            self.attack_cd += 1
        if self.attack_cd == 25:
            self.attack_cd_begin = False
            self.attack_cd = 0
