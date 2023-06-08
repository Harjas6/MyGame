import math

import pygame
import random
from settings import *


# Represents the level/what will be seen on screen
class Level:
    # Initializes the display
    def __init__(self):
        self.disp_surf = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.make_screen()
        self.time_passed = pygame.time.get_ticks()

    # Does the intial printing of the level on the screen
    def make_screen(self):
        self.make_background()
        for row_num, row in enumerate(MAP):
            for col_num, item in enumerate(row):
                x = row_num * TILESIZE
                y = col_num * TILESIZE
                if item == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                elif item == 's':
                    Block((x, y), [self.visible_sprites, self.obstacle_sprites], name='spike')

    # Prints out the background
    def make_background(self):
        for x in range(0, len(MAP) + 1):
            for y in range(0, len(MAP[0]) + 1):
                x_pos = x * TILESIZE
                y_pos = y * TILESIZE
                Block((x_pos, y_pos), [self.visible_sprites])

    # Updates the screen with new locations of sprites
    def run(self):
        self.discard_projectiles()
        self.generate_projectiles()
        self.visible_sprites.update()
        if self.player.is_collison():
            return True
        self.visible_sprites.draw(self.disp_surf)
        return True

    def generate_projectiles(self):
        if pygame.time.get_ticks() - self.time_passed > 1000:
            self.time_passed = pygame.time.get_ticks()
            positions = [(random.randint(-50, 0), random.randint(-50, HEIGHT + 50)),
                         (random.randint(WIDTH, WIDTH + 50), random.randint(-50, HEIGHT + 50)),
                         (random.randint(-50, WIDTH + 50), random.randint(-50, 0)),
                         (random.randint(-50, WIDTH + 50), random.randint(HEIGHT, HEIGHT + 50))]
            Projectile(random.choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)
            Projectile(random.choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)
            Projectile(random.choice(positions), [self.visible_sprites, self.projectile_sprites, self.obstacle_sprites],
                       self.player)

    def discard_projectiles(self):
        for projectile in self.projectile_sprites:
            if self.projectile_offscreen(projectile):
                self.projectile_sprites.remove(projectile)

    def projectile_offscreen(self, projectile):
        return projectile.rect.x > (WIDTH + 100) or projectile.rect.x < -100 or \
            projectile.rect.y > (HEIGHT + 100) or projectile.rect.y < 100


class Block(pygame.sprite.Sprite):
    # Creates a block and places it in a group
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
        self.speed = 5

    # Updates player
    def update(self):
        self.input()
        self.move()

    # Handles input
    def input(self):
        keys = pygame.key.get_pressed()
        self.check_y_direct(keys)
        self.check_x_direct(keys)

    # Moves player with a normalized direction
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.is_collison()

    # Check if player is moving horizontal
    def check_x_direct(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = + 1
        else:
            self.direction.x = 0

    # Check if player is moving vertical
    def check_y_direct(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    # if there is collison with an obstacle return true
    def is_collison(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                return True
        return False


# !!! PROBABLY DO NOT NEED ANYMORE
# # Handles horizontal collisons between the player and static objects
# def horiz_collison(self):
#     if self.direction.x > 0:
#         self.obstacle_loop('right')
#     elif self.direction.x < 0:
#         self.obstacle_loop('left')
#
# # Handles vertical collisons between the player and static objects
# def vert_collison(self):
#     if self.direction.y > 0:
#         self.obstacle_loop('down')
#     elif self.direction.y < 0:
#         self.obstacle_loop('up')
#
# # if object collide with player puts player on correct side of object
# def obstacle_loop(self, direc):
#     for sprite in self.obstacle_sprites:
#         if sprite.rect.colliderect(self.rect):
#             match direc:
#                 case 'down':
#                     self.rect.bottom = sprite.rect.top
#                 case 'up':
#                     self.rect.top = sprite.rect.bottom
#                 case 'left':
#                     self.rect.left = sprite.rect.right
#                 case 'right':
#                     self.rect.right = sprite.rect.left
#

class Projectile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load('images/orb.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        direct = self.aim_at_player(player)
        self.direction = pygame.math.Vector2(direct)
        self.speed = 6

    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def collide(self, player):
        if self.rect.colliderect(player.rect):
            print(True)

    def aim_at_player(self, player):
        player_x, player_y = player.rect.x, player.rect.y
        direct = (player_x - self.rect.x, player_y - self.rect.y)
        length = math.hypot(*direct)
        return direct[0] / length, direct[1] / length
