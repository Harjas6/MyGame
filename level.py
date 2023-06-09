import math
import pygame

from random import choice, randint
from settings import *


# Represents the level/what will be seen on screen
class Level:
    # Initializes the display
    def __init__(self):
        self.disp_surf = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.time_passed = pygame.time.get_ticks()
        self.map = choice(MAPS)
        self.make_screen()

    # Does the intial printing of the level on the screen
    def make_screen(self):

        self.make_background()
        # Goes through map placing player and obstacles where needed
        for row_num, row in enumerate(self.map):
            for col_num, item in enumerate(row):
                x = row_num * TILESIZE
                y = col_num * TILESIZE
                if item == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                elif item == 's':
                    Block((x, y), [self.visible_sprites, self.obstacle_sprites], name='spike')

    # Prints out the background
    def make_background(self):
        for x in range(0, len(self.map) + 1):
            for y in range(0, len(self.map[0]) + 1):
                x_pos = x * TILESIZE
                y_pos = y * TILESIZE
                Block((x_pos, y_pos), [self.visible_sprites])

    # Updates the screen with new locations of sprites. Returns False if there is a collison True otherwise
    def run(self):
        self.discard_projectiles()
        self.generate_projectiles()
        self.visible_sprites.update()
        if self.player.is_collison():
            return False
        self.visible_sprites.draw(self.disp_surf)
        return True

    # Every 1200 ms generates 3 randomly placed projectile
    def generate_projectiles(self):
        if pygame.time.get_ticks() - self.time_passed > 1200:
            self.time_passed = pygame.time.get_ticks()
            # 3 random x and y positions slightly offscreen
            positions = [(randint(-50, 0), randint(-50, HEIGHT + 50)),
                         (randint(WIDTH, WIDTH + 50), randint(-50, HEIGHT + 50)),
                         (randint(-50, WIDTH + 50), randint(-50, 0)),
                         (randint(-50, WIDTH + 50), randint(HEIGHT, HEIGHT + 50))]
            # 3 projectiles created choosing one of the possible positions
            Projectile(choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)
            Projectile(choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)
            Projectile(choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)

    # Discards projectiles that do not need to be rendered
    def discard_projectiles(self):
        for projectile in self.projectile_sprites:
            if self.projectile_offscreen(projectile):
                self.projectile_sprites.remove(projectile)

    # Checks if a projectile is far enough offscreen and if so Returns True
    def projectile_offscreen(self, projectile):
        return projectile.rect.x > (WIDTH + 100) or projectile.rect.x < -100 or \
            projectile.rect.y > (HEIGHT + 100) or projectile.rect.y < 100


class Block(pygame.sprite.Sprite):
    # Creates a block with an image specified by name and places it in a group(s)
    def __init__(self, pos, groups, name='grass'):
        super().__init__(groups)
        if name == 'grass':
            self.image = pygame.image.load('images/grass.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
        elif name == "spike":
            self.image = pygame.image.load('images/spike.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)


# represents the user player
class Player(pygame.sprite.Sprite):
    # creates a player in the given position and set atrributes
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacles
        self.speed = 7

    # Updates player
    def update(self):
        self.input()
        self.move()

    # Handles input
    def input(self):
        keys = pygame.key.get_pressed()
        self.set_y_direct(keys)
        self.set_x_direct(keys)

    # Moves player with a normalized direction
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Changes player position
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        # IF new position is offscreen, undos above change keeping player on screen
        if self.rect.x > WIDTH - self.image.get_size()[0] or self.rect.x < 0:
            self.rect.x -= self.direction.x * self.speed
        if self.rect.y > HEIGHT - self.image.get_size()[1] or self.rect.y < 0:
            self.rect.y -= self.direction.y * self.speed

    # Sets x direction according to input
    def set_x_direct(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = + 1
        else:
            self.direction.x = 0

    # Sets y direction according to input
    def set_y_direct(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    # if there is collision with an obstacle return true false otherwise
    def is_collison(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                return True
        return False


# represents a projectile
class Projectile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load('images/orb.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        direct = self.aim_at_player(player)
        self.direction = pygame.math.Vector2(direct)
        # Chooses one random speed to allow for variety
        self.speed = choice([3, 5, 4, 6])


# updates sprites location
    def update(self):
        self.move()

# Adds x and y velocity
    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed


# Return a normalized vector pointing at the player current position
    def aim_at_player(self, player):
        player_x, player_y = player.rect.x, player.rect.y
        direct = (player_x - self.rect.x, player_y - self.rect.y)
        length = math.hypot(*direct)
        return direct[0]/length, direct[1]/length
