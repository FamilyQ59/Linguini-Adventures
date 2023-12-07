from Collisions import check_collision
import Colors
import math
import random
from Load import *
from Main import player

Phantom_Animation = [pygame.image.load(os.path.join("../Images/Phantom1.png")),
                     pygame.image.load(os.path.join("../Images/Phantom2.png")),
                     pygame.image.load(os.path.join("../Images/Phantom3.png")),
                     pygame.image.load(os.path.join("../Images/Phantom4.png"))]

Phantom_Projectile = [pygame.image.load(os.path.join("../Images/Phant_projectile1.png")),
                      pygame.image.load(os.path.join("../Images/Phant_projectile2.png")),
                      pygame.image.load(os.path.join("../Images/Phant_projectile3.png"))]

Shooter_Head = [pygame.image.load(os.path.join("../Images/Shooter_1.png")),
                pygame.image.load(os.path.join("../Images/Shooter_2.png"))]

scale = pygame.transform.scale

Phantom_hit = os.path.join("../Images/Phantom_hit.png")

Shooter_Head_Hit = os.path.join("../Images/Shooter_Head_Hit.png")

ninja_attack_images = [pygame.image.load(os.path.join("../Images/Ninja_attack1.png")),
                       pygame.image.load(os.path.join("../Images/Ninja_attack2.png")),
                       pygame.image.load(os.path.join("../Images/Ninja_attack3.png")),
                       pygame.image.load(os.path.join("../Images/Ninja_attack4.png")),
                       pygame.image.load(os.path.join("../Images/Ninja_attack5.png"))]

ninja_run = os.path.join("..", "Images", "Assets", 'Ninja_Run')
ninja_run_img = [pygame.image.load(os.path.join("../Images/Ninja_Run_1.png")),
                 pygame.image.load(os.path.join("../Images/Ninja_Run_2.png")),
                 pygame.image.load(os.path.join("../Images/Ninja_Run_3.png"))]

ninja_get_hit = os.path.join("../Images/Ninja_Run_Hit.png")

vulture_flight_img = [pygame.image.load(os.path.join("../Images/Vulture_1.png")),
                  pygame.image.load(os.path.join("../Images/Vulture_2.png")),
                  pygame.image.load(os.path.join("../Images/Vulture_3.png"))]

vulture_dive_img = [pygame.image.load(os.path.join("../Images/Vulture_dive_1.png")),
                    pygame.image.load(os.path.join("../Images/Vulture_dive_2.png")),
                    pygame.image.load(os.path.join("../Images/Vulture_dive_3.png"))]
spike_img = os.path.join("../Images/Spike.png")


class Phantom:
    # Enemy rotating on an orbit, send homing projectiles onto player
    def __init__(self, pos):
        self.orbit_center = pygame.math.Vector2(pos)
        self.pos = pygame.math.Vector2(0, 0)
        self.hitbox = pygame.Rect(self.pos.x - 10, self.pos.y - 10, 20, 20)
        self.angle = random.choice([math.pi, math.pi * 2, math.pi * 3, math.pi * 4])
        self.speed = 0.05
        self.shot_cd, self.shot_timer = 0, 0
        self.projectiles = []
        self.life = 3
        self.color = Colors.Purple
        self.hit = 0
        self.animation_index = 0

    def loop(self, Tile_rects):
        # Call all variables that must be in the game loop together
        self.shoot(player.position.x, player.position.y, player.rect, Tile_rects)
        self.collision(player.range)
        self.move()

    def draw(self, surface, scroll_x, scroll_y):
        if self.life > 0:  # if it´s alive

            # Draw Orbit
            pygame.draw.circle(surface, (20, 0, 0),
                               (self.orbit_center.x - scroll_x, self.orbit_center.y - scroll_y),
                               45, 2)
            # Hitbox
            self.hitbox = pygame.Rect(self.pos.x - 10, self.pos.y - 10, 30, 30)

            # Draw Phantom
            surface.blit(scale(Phantom_Animation[int(self.animation_index)], (30, 30)),
                         (self.pos.x - 15 - scroll_x, self.pos.y - scroll_y - 10, 30, 30))
            # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
            self.animation_index += 1

            if self.animation_index >= 4:
                self.animation_index = 0

            # Draw Phantom Hit
            if self.hit == 1:
                surface.blit(scale(pygame.image.load(Phantom_hit), (30, 30)),
                             (self.pos.x - 15 - scroll_x, self.pos.y - scroll_y - 10, 30, 30))

            # Projectiles
            for shot in self.projectiles:
                shot.draw(surface, scroll_x, scroll_y)

    def move(self):
        # Move in a circular motion along it´s orbit
        self.pos.x = self.orbit_center.x + 45 * math.cos(self.angle)
        self.pos.y = self.orbit_center.y + 45 * math.sin(self.angle)
        self.angle += self.speed

    def shoot(self, character_position_x, character_position_y, character_hitbox, Tile_rects):
        if self.life > 0:  # If phantom is alive
            self.shot_cd += 1  # shot cooldown

            if self.shot_cd == 100:  # Shoot after cooldown
                shot = Phantom_projectile(pygame.math.Vector2(self.pos.x, self.pos.y))
                self.projectiles.append(shot)
                self.shot_cd = 0

            for shot in self.projectiles:  # Call movement and check projectile collisions
                self.shot_timer += 1
                shot.movement(character_position_x, character_position_y)
                try:
                    if self.shot_timer == 300 and len(self.projectiles) > 0:
                        self.projectiles.remove(self.projectiles[0])
                        self.shot_timer = 0

                    if check_collision(character_hitbox, shot.hitbox) and len(self.projectiles) > 0:
                        player.life -= 1
                        self.projectiles.remove(shot)

                    for rect in Tile_rects:  # Check collisions with all tiles
                        if check_collision(rect, shot.hitbox) and len(self.projectiles) > 0:
                            self.projectiles.remove(shot)
                except ValueError:
                    print("a")

    def collision(self, player_attack):
        # Check collisions between phantom and player directly
        if self.life > 0:  # If it´s alive
            if check_collision(player_attack, self.hitbox) and self.hit == 0:
                self.color = Colors.Red
                self.life -= 1
                self.hit = 1
            if player.attacking is False:
                self.hit = 0
                self.color = Colors.Purple

            if check_collision(player.rect, self.hitbox):
                player.life -= 0.1

            # Collision with shot and player attack
            try:
                for shot in self.projectiles:
                    if check_collision(player.range, shot.hitbox) and player.attacking and len(self.projectiles) > 0:
                        self.projectiles.remove(shot)
            except ValueError:
                print("a")


class Phantom_projectile:
    def __init__(self, pos):
        self.position = pos
        self.hitbox = pygame.Rect(self.position.x - 5, self.position.y - 5, 15, 15)
        self.distance = 0
        self.speed = 2.5
        self.size = 5
        self.dead = False
        self.animation_index = 0

    def draw(self, surface, scroll_x, scroll_y):
        # Draw projectile and define hitbox
        self.hitbox = pygame.Rect(self.position.x - 7, self.position.y - 7, 15, 15)

        # Draw Phantom Projectile
        surface.blit(scale(Phantom_Projectile[int(self.animation_index)], (15, 15)),
                     (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, 15, 15))
        # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
        self.animation_index += 1

        if self.animation_index >= 3:
            self.animation_index = 0

    def movement(self, character_position_x, character_position_y):
        # Move along a vector constantly updating between player and projectile
        self.distance = math.sqrt((character_position_x - self.position.x) ** 2 +
                                  (character_position_y - self.position.y) ** 2)
        self.position.x += self.speed * (character_position_x - self.position.x) / self.distance
        self.position.y += self.speed * (character_position_y - self.position.y) / self.distance


class Soldier:
    # Enemy that shots when enemy is at a certain distance, shoots normal bullets
    def __init__(self, position, face_side):
        # Basic variables
        self.position = pygame.math.Vector2(position)
        self.hitbox = (self.position.x, self.position.y, 20, 40)
        self.life = 3
        self.color = Colors.Green
        self.range = 400

        # Define movement variables and initial direction
        self.move_definition = {"Left": False, "Right": False, "Move_length": 0}
        if face_side == "Left":
            self.move_definition["Left"] = True
        else:
            self.move_definition["Right"] = True

        # Define variables for interaction and shooting
        self.distance = 0
        self.shot_cd = {"Shoot": 0, "Initial_shot": 0}
        self.projectiles = []
        self.line_end = pygame.math.Vector2(0, 0)
        self.player_center = player.position + (player.rect.width / 2, -player.rect.height / 2)
        self.center = self.position + (0, 5)
        self.hit = 0
        self.animation_index = 0

    def draw(self, surface, scroll_X, scroll_Y):
        if self.life > 0:
            # Define player and self center for better visuals and accuracy
            self.player_center = player.position + (player.rect.width / 2, -player.rect.height / 2)

            # Draw Enemy
            self.hitbox = pygame.Rect(self.position.x, self.position.y, 30, 60)

            # Draw ShooterHead
            if self.move_definition["Left"]:
                surface.blit(scale(Shooter_Head[int(self.animation_index)], (30, 60)),
                             (self.position.x - scroll_X, self.position.y - scroll_Y, 30, 60))
            elif self.move_definition["Right"]:
                surface.blit(pygame.transform.flip(scale(Shooter_Head[int(self.animation_index)],
                                                         (30, 60)), True, False),
                             (self.position.x - scroll_X, self.position.y - scroll_Y, 30, 60))
            # 0.5 in order to iterate every 2 loops, that´s why when drawing it, it iterates through it as an int
            self.animation_index += 0.15

            if self.animation_index >= 2:
                self.animation_index = 0

            # Draw if facing left or right while shooting
            if player.position.x - self.position.x > 0 and self.distance < self.range:
                self.center = self.position + (27, 9)
                self.move_definition["Right"] = True
                self.move_definition["Left"] = False

            elif player.position.x - self.position.x < 0 and self.distance < self.range:
                self.center = self.position + (3, 9)
                self.move_definition["Right"] = False
                self.move_definition["Left"] = True

            # Draw ShooterHead Hit
            if self.hit == 1:
                surface.blit(scale(pygame.image.load(Shooter_Head_Hit), (30, 60)),
                             (self.position.x - scroll_X, self.position.y - scroll_Y, 30, 60))

            # Draw Laser between player and soldier
            if self.distance < self.range:
                self.color = Colors.Purple
                pygame.draw.line(surface, Colors.Red,
                                 self.player_center - (scroll_X, scroll_Y),
                                 self.center - (scroll_X, scroll_Y), 1)

            if self.distance > self.range:
                self.color = Colors.Green

            # Direction of the projectile (line that goes to the end of the screen and intersects the player)
            direction = (self.player_center.x - self.center.x, self.player_center.y - self.center.y)
            if direction[0] != 0:
                self.line_end.x = 0 if direction[0] < 0 else 2000
                self.line_end.y = self.center.y + (self.line_end.x - self.center.x) * direction[1] / direction[0]
            else:
                self.line_end.x = self.center.x
                self.line_end.y = 0 if direction[1] < 0 else 426

            # Draw Projectile
            for shot in self.projectiles:
                shot.draw(surface, scroll_X, scroll_Y)

    def movement(self, Range_px, Speed, Tile_rects, move=bool):
        # As long as player isn´t in visual range of soldier, move a determined range to the left, and then to right
        if move is True:
            if self.distance > self.range and self.life > 0:
                if self.move_definition["Left"]:
                    self.position.x -= Speed
                    self.move_definition["Move_length"] += Speed
                if self.move_definition["Right"]:
                    self.position.x += Speed
                    self.move_definition["Move_length"] += Speed

                if self.move_definition["Move_length"] >= Range_px and self.move_definition["Left"]:
                    self.move_definition["Left"] = False
                    self.move_definition["Right"] = True
                    self.move_definition["Move_length"] = 0

                if self.move_definition["Move_length"] >= Range_px and self.move_definition["Right"]:
                    self.move_definition["Right"] = False
                    self.move_definition["Left"] = True
                    self.move_definition["Move_length"] = 0

        # Call to loop
        self.shoot(Tile_rects)

    def shoot(self, Tile_rects):
        # Define distance between player and soldier
        self.distance = math.sqrt(
            (player.position.x - self.position.x) ** 2 + (player.position.y - self.position.y) ** 2)

        if self.life > 0:  # As long as enemy is alive
            self.shot_cd["Shoot"] += 1

            # Check collisions between phantom and player directly
            if check_collision(player.range, self.hitbox) and self.hit == 0:  # Attack and enemy
                self.color = Colors.Red
                self.life -= 2
                self.hit = 1
            if player.attacking is False:
                self.hit = 0
                self.color = Colors.Purple

            if check_collision(player.rect, self.hitbox):  # Player and Hitbox
                player.life -= 0.1

            # Create a cooldown for the first shoot
            if self.distance > self.range:
                self.shot_cd["Initial_shot"] = 0

            if self.distance < self.range:
                self.shot_cd["Initial_shot"] += 1

            # As long as player is between range, and both normal and initial cooldown are okay, shoot
            if self.shot_cd["Shoot"] >= 50 and self.distance < self.range and self.shot_cd["Initial_shot"] >= 50:
                shot = Soldier_projectile(self.center, self.line_end)
                self.projectiles.append(shot)
                self.shot_cd["Shoot"], self.shot_cd["Initial_shot"] = 0, 0

            # Check for projectile collisions and call it´s movement function
            for shot in self.projectiles:
                shot.movement()

                try:
                    if check_collision(player.rect, shot.hitbox) and len(self.projectiles) > 0:
                        player.life -= 1
                        self.projectiles.remove(shot)

                    if check_collision(player.range, shot.hitbox) and player.attacking and len(self.projectiles) > 0:
                        self.projectiles.remove(shot)

                    for rect in Tile_rects:
                        if check_collision(rect, shot.hitbox) and len(self.projectiles) > 0:
                            self.projectiles.remove(shot)
                except ValueError:
                    print("a")


class Soldier_projectile:
    # Projectile for soldier
    def __init__(self, pos, objective):
        self.position = pygame.math.Vector2(pos)
        self.objective = pygame.math.Vector2(objective)
        self.distance = math.sqrt((self.position.x - self.objective.x) ** 2 + (self.position.y - self.objective.y) ** 2)
        self.radius = 3
        self.hitbox = pygame.Rect(self.position.x - 5, self.position.y - 5, self.radius * 2, self.radius * 2)
        self.speed = 15

    def draw(self, surface, scroll_x, scroll_y):
        # Define hitbox and draw bullet
        self.hitbox = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius,
                                  self.radius * 2, self.radius * 2)
        pygame.draw.rect(surface, Colors.Brown,
                         (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y,
                          self.hitbox.width, self.hitbox.height), 1)
        pygame.draw.circle(surface, Colors.Yellow,
                           (self.position.x - scroll_x, self.position.y - scroll_y), self.radius)

    def movement(self):
        # Move along a vector called only once, which means it isn´t a homing projectile
        self.position.x += self.speed * (self.objective.x - self.position.x) / self.distance
        self.position.y += self.speed * (self.objective.y - self.position.y) / self.distance


class Ninja:
    def __init__(self, position, DistanceToEachSide, life):
        self.position = pygame.math.Vector2(position)
        self.move_definition = {"Left": True, "Right": False, "Move_length": 0}
        self.limits = [self.position.x - DistanceToEachSide, self.position.x + DistanceToEachSide]
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 30, 60)
        self.life = 3
        self.color = Colors.Green
        self.animation_index = {"attack": 0, "walk": 0}
        self.life = life

        # Attack
        self.distance = 0
        self.attacking = False
        self.atktime = 0
        self.attack_cd = 0
        self.attack_cd_begin = False
        self.range = pygame.Rect(self.position.x, self.position.y, 100, 50)
        self.attack_begin_side = [0, 0]
        self.hit = {"PlayerAttack": False, "NinjaAttack": False}

    def draw(self, surface, scroll_x, scroll_y):
        if self.life > 0:
            self.hitbox = pygame.Rect(self.position.x, self.position.y, 30, 60)

            # Draw Movement to Left
            if self.move_definition["Left"]:
                surface.blit(scale(ninja_run_img[int(self.animation_index["walk"])], (30, 60)),
                             (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.width,
                              self.hitbox.height))
                # 0.5 in order to iterate every 2 loops, that's why when drawing it,it iterates through it as an int
                self.animation_index["walk"] += 0.5

            if self.animation_index["walk"] >= 3:
                self.animation_index["walk"] = 0

            # Draw Movement to Right
            if self.move_definition["Right"]:
                surface.blit(scale(pygame.transform.flip((ninja_run_img[int(self.animation_index["walk"])]),
                                                         True, False), (30, 60)),
                             (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.width,
                              self.hitbox.height))
                # 0.5 in order to iterate every 2 loops, that's why when drawing it,it iterates through it as an int
                self.animation_index["walk"] += 0.5

            if self.animation_index["walk"] >= 3:
                self.animation_index["walk"] = 0

            # Draw Attack
            if self.attacking:

                # Draw Attack to the Right
                if self.attack_begin_side == [1, 0]:
                    # Draws attack (scales it, iterates through it (as an int), defines position and size)
                    surface.blit(scale(ninja_attack_images[int(self.animation_index["attack"])], (75, 50)),
                                 (
                                     self.range.x - scroll_x, self.range.y - scroll_y, self.range.width,
                                     self.range.height))
                    # 0.5 in order to iterate every 2 loops, that's why when drawing it,it iterates through it as an int
                    self.animation_index["attack"] += 1

                # Draws Attack to the Left
                elif self.attack_begin_side == [0, 1]:
                    # Draws attack(flips it, scales it, iterates through it (as an int), defines position and size)
                    surface.blit(pygame.transform.flip(scale(ninja_attack_images[int(self.animation_index["attack"])],
                                                             (75, 50)), True, False),
                                 (
                                     self.range.x - scroll_x, self.range.y - scroll_y, self.range.width,
                                     self.range.height))
                    self.animation_index["attack"] += 1

            # Draw if Ninja is Hit
            if self.hit["PlayerAttack"] and self.move_definition["Left"]:
                surface.blit(scale(pygame.image.load(ninja_get_hit), (30, 60)),
                             (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.width,
                              self.hitbox.height))
            if self.hit["PlayerAttack"] and self.move_definition["Right"]:
                surface.blit(scale(pygame.transform.flip(pygame.image.load(ninja_get_hit), True, False), (30, 60)),
                             (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.width,
                              self.hitbox.height))

    def Interactions(self, Speed):

        if self.life > 0:

            # Distance
            self.distance = math.sqrt((player.rect.x - self.position.x) ** 2 + (player.rect.y - self.position.y) ** 2)

            # Movement
            if self.distance > self.range.width:
                if self.move_definition["Left"]:
                    self.position.x -= Speed
                    self.move_definition["Move_length"] += Speed
                if self.move_definition["Right"]:
                    self.position.x += Speed
                    self.move_definition["Move_length"] += Speed

                if self.position.x < self.limits[0]:
                    self.move_definition["Left"] = False
                    self.move_definition["Right"] = True
                    self.move_definition["Move_length"] = 0

                if self.position.x > self.limits[1]:
                    self.move_definition["Right"] = False
                    self.move_definition["Left"] = True
                    self.move_definition["Move_length"] = 0

            # Facing
            if player.position.x - self.position.x > 0 and self.distance < self.range.width:
                self.move_definition["Right"] = True
                self.move_definition["Left"] = False

            elif player.position.x - self.position.x < 0 and self.distance < self.range.width:
                self.move_definition["Right"] = False
                self.move_definition["Left"] = True

            self.attack()
            self.collisions()

    def attack(self):
        if self.life > 0:

            # Carries out the attack motion
            if self.attacking:
                self.atktime += 1

            # Defines the attack hitbox depending on if player facing right or left (respectively)
            if self.attack_begin_side == [1, 0]:
                self.range = pygame.Rect(self.hitbox.x + self.hitbox.width, self.hitbox.y, 75, 50)
            if self.attack_begin_side == [0, 1]:
                self.range = pygame.Rect(self.hitbox.x - 75, self.hitbox.y, 75, 50)

            # Resets array checking which side is player facing
            if self.attack_begin_side == [0, 0]:
                self.range = pygame.Rect(1000, 1000, 75, 50)

            # Takes attack input and checks if every cooldown is done
            if self.attacking is False and not self.attack_cd_begin and self.distance < self.range.width:
                if self.move_definition["Right"]:
                    self.attack_begin_side = [1, 0]
                if self.move_definition["Left"]:
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
            if self.attack_cd == 50:
                self.attack_cd_begin = False
                self.attack_cd = 0

    def collisions(self):
        if self.life > 0:
            if check_collision(self.range, player.rect) and self.hit["NinjaAttack"] is False:
                player.life -= 1
                self.hit["NinjaAttack"] = True
            if check_collision(self.hitbox, player.rect):
                player.life -= 0.1
            if check_collision(self.hitbox, player.range) and self.hit["PlayerAttack"] is False:
                self.life -= 1
                self.color = Colors.Red
                self.hit["PlayerAttack"] = True

            if self.attacking is False:
                self.hit["NinjaAttack"] = False
            if player.attacking is False:
                self.hit["PlayerAttack"] = False
                self.color = Colors.Green


class Vulture:
    def __init__(self, pos, DistanceToEachSide):

        # Life
        self.life = 3

        # Movement
        self.position = pygame.math.Vector2(pos)
        self.DistanceToEachSide = DistanceToEachSide
        self.limits = [self.position.x - DistanceToEachSide, self.position.x + DistanceToEachSide]
        if random.choice([True, False]):
            self.movement_definition = {"Left": False, "Right": True}
        else:
            self.movement_definition = {"Left": True, "Right": False}

        # Hitbox
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 40, 20)

        # Attack
        self.attacking = False
        self.distance = math.sqrt(
            (self.position.x - player.position.x) ** 2 + (self.position.y - player.position.y) ** 2)
        self.attack_limit = [0, 0]
        self.WhenToAttack = {"Left": 0, "Right": 0, "Top": 0}

        # Defines the probability of the diving motion beginning
        self.begin_attack = {"Target": random.randint(1, 3), "Chance": 0}
        self.speed = 10
        self.animation_index = {"Flight": 0}
        self.dive = {"player.x": 0, "player.y": 0, "self_pos": pygame.math.Vector2(), "once": False}
        self.distance_to_each_side = DistanceToEachSide

    def draw(self, surface, scroll_x, scroll_y):
        if self.life > 0:
            # Draw the vulture while it´s flying on the air
            if self.attacking is False:
                self.hitbox = pygame.Rect(self.position.x, self.position.y, 40, 20)

                # Draws attack (scales it, iterates through it (as an int), defines position and size)
                if self.movement_definition["Right"]:
                    surface.blit(scale(vulture_flight_img[int(self.animation_index["Flight"])], (40, 20)),
                                 (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.w, self.hitbox.h))

                if self.movement_definition["Left"]:
                    surface.blit(scale(pygame.transform.flip(
                        (vulture_flight_img[int(self.animation_index["Flight"])]), True, False), (40, 20)),
                        (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.w, self.hitbox.h))

                # 0.5 in order to iterate every 2 loops, that's why when drawing it,it iterates through it as an int
                self.animation_index["Flight"] += 0.1

                if self.animation_index["Flight"] >= 3:
                    self.animation_index["Flight"] = 0

            # Draw my vulture while it´s diving
            if self.attacking is True:
                self.hitbox = pygame.Rect(self.position.x, self.position.y, 40, 40)
                # Draws attack (scales it, iterates through it (as an int), defines position and size)
                if self.movement_definition["Left"]:
                    surface.blit(scale(vulture_dive_img[int(self.animation_index["Flight"])], (40, 40)),
                                 (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y,
                                  self.hitbox.w, self.hitbox.h))

                if self.movement_definition["Right"]:
                    surface.blit(scale(pygame.transform.flip(
                        (vulture_dive_img[int(self.animation_index["Flight"])]), True, False), (40, 40)),
                        (self.hitbox.x - scroll_x, self.hitbox.y - scroll_y, self.hitbox.w, self.hitbox.h))

                # 0.5 in order to iterate every 2 loops, that's why when drawing it,it iterates through it as an int
                self.animation_index["Flight"] += 0.1

                if self.animation_index["Flight"] >= 3:
                    self.animation_index["Flight"] = 0

    def Interactions(self, Tile_rects, limit_x_1, limit_x_2, player_y_limit):
        if self.life > 0:
            self.attack_limit = [0, 0]  # This variable checks when the vulture hits the limit and changes side,
            # it´s used when defining the chance of the attack beginning

            if limit_x_1 < player.rect.x < limit_x_2 and player.position.y >= player_y_limit:
                # Keeps vulture within limits
                self.limits = [player.rect.x - self.distance_to_each_side, player.rect.x + self.distance_to_each_side]

            if self.begin_attack["Chance"] < self.begin_attack["Target"]:  # Define movement while vulture flies:
                if self.movement_definition["Left"] and self.position.x > self.limits[0]:
                    self.position.x -= 5
                if self.movement_definition["Right"] and self.position.x < self.limits[1]:
                    self.position.x += 5

                if self.movement_definition["Left"] and self.position.x <= self.limits[0]:
                    self.attack_limit[0] = 1
                    self.movement_definition["Left"] = False
                    self.movement_definition["Right"] = True

                if self.movement_definition["Right"] and self.position.x >= self.limits[1]:
                    self.attack_limit[1] = 1
                    self.movement_definition["Left"] = True
                    self.movement_definition["Right"] = False

            # Begins Dive
            if self.begin_attack["Chance"] >= self.begin_attack["Target"] and player.position.y == player_y_limit:

                self.attacking = True

                # Define direction only once
                if self.dive["once"] is False:
                    self.dive["player.x"] = player.position.x
                    self.dive["player.y"] = player.position.y
                    self.dive["self_pos"] = self.position
                    self.dive["once"] = True

                # Calculate Distance
                self.distance = math.sqrt(
                    (self.dive["self_pos"].x - self.dive["player.x"]) ** 2 +
                    (self.dive["self_pos"].y - self.dive["player.y"]) ** 2)

                # Diving movement
            if self.attacking is True:
                self.position.x += self.speed * (self.dive["player.x"] -
                                                 self.dive["self_pos"].x) / self.distance
                self.position.y += self.speed * (self.dive["player.y"] -
                                                 self.dive["self_pos"].y) / self.distance

            elif player.position.y != player_y_limit:
                self.begin_attack["Chance"] = 0

            self.attack()
            self.collisions(Tile_rects)

    def attack(self):

        # When it collides with limit
        if self.begin_attack["Chance"] < self.begin_attack["Target"]:

            # Increases chances of beginning attack everytime the vulture collides with a limit
            if self.attack_limit[0] == 1:
                self.begin_attack["Chance"] += 1

            if self.attack_limit[1] == 1:
                self.begin_attack["Chance"] += 1

    def collisions(self, Tile_rects):
        if check_collision(self.hitbox, player.rect):
            self.life -= 3
            player.life -= 2.5

        for rect in Tile_rects:
            if check_collision(rect, self.hitbox):
                self.life -= 3


class Spike:
    def __init__(self, pos):
        self.position = pygame.math.Vector2(pos)
        self.hitbox = pygame.Rect(self.position.x + 6, self.position.y, 20, 32)

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(pygame.image.load(spike_img), (self.hitbox.x - 6 - scroll_x, self.hitbox.y - scroll_y,
                                                    self.hitbox.w, self.hitbox.h))

        self.collisions()

    def collisions(self):
        if check_collision(player.rect, self.hitbox):
            player.life -= 100


class Level_doors:
    def __init__(self, position, DoorNumber=int):
        self.position = pygame.math.Vector2(position)
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 32, 64)
        self.door_number = DoorNumber

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(SelectLvl.Level_doors[self.door_number], (self.position.x - scroll_x, self.position.y - scroll_y))

    def Collisions(self):
        if check_collision(player.rect, self.hitbox):
            return True
