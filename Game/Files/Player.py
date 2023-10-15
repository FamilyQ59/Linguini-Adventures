import pygame

linguini = 'C:/Users/carlo/PycharmProjects/Linguini-Adventures/Game/Images/Selva/Linguini.png'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .70, -.12
        self.image = pygame.image.load(linguini)
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles, key):
        self.horizontal_motion(dt, key)
        self.check_X_collisions(tiles)
        self.vertical_motion(dt)
        self.check_Y_collision(tiles)

    def horizontal_motion(self, dt, key):
        self.acceleration.x = 0
        if key[pygame.K_d]:
            self.acceleration.x += 3
        elif key[pygame.K_a]:
            self.acceleration.x -= 3

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limitvel(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_motion(self, dt):
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
        if key[pygame.K_SPACE]:
            self.jump()
        elif self.is_jumping:
            self.velocity.y *= .50
            self.is_jumping = False

    def jump(self):
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
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x

            elif self.velocity.x < 0:
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def check_Y_collision(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
