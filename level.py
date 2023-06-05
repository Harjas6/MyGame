import pygame
from settings import *

# Represents the level/ what will be seen on screen
class Level:
    # Initializes the display
    def __init__(self):
        self.disp_surf = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.make_screen()

# Does the intial printing of the level on the screen
    def make_screen(self):
        self.make_background()
        for row_num, row in enumerate(MAP):
            for col_num, item in enumerate(row):
                x = row_num * TILESIZE
                y = col_num * TILESIZE
                if item == 'p':
                    self.player = Player((x, y), [self.visible_sprites],self.obstacle_sprites )
                elif item == 's':
                    Block((x,y), [self.visible_sprites,self.obstacle_sprites], name='spike'),


# Prints out the background
    def make_background(self):
        for x in range(0, len(MAP)+1):
            for y in range(0, len(MAP[0])+1):
                    x_pos = x * TILESIZE
                    y_pos = y * TILESIZE
                    Block((x_pos, y_pos), [self.visible_sprites])

# Updates the screen with new locations of sprites
    def run(self):
        self.visible_sprites.draw(self.disp_surf)
        self.visible_sprites.update()


class Block(pygame.sprite.Sprite):
    # Creates a block and places it in a group
    def __init__(self, pos, groups, name='grass'):
        super().__init__(groups)
        if name == 'grass':
            self.image = pygame.image.load('images/grass.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
        elif name == "spike":
            self.image = pygame.image.load('images/spike.png').convert_alpha()
            #self.image = pygame.transform.scale(self.image, (50, 50))
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
        self.horiz_collison()
        self.rect.y += self.direction.y * self.speed
        self.vert_collison()


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


    # Handles horizontal collisons between the player and static objects
    def horiz_collison(self):
        if self.direction.x > 0:
            self.obstacle_loop('right')
        elif self.direction.x < 0:
            self.obstacle_loop('left')

    # Handles vertical collisons between the player and static objects
    def vert_collison(self):
        if self.direction.y > 0:
            self.obstacle_loop('down')
        elif self.direction.y < 0:
            self.obstacle_loop('up')

    # if object collide with player puts player on correct side of object
    def obstacle_loop(self, direc):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                match direc:
                    case 'down':
                        self.rect.bottom = sprite.rect.top
                    case 'up':
                        self.rect.top = sprite.rect.bottom
                    case 'left':
                        self.rect.left = sprite.rect.right
                    case 'right':
                        self.rect.right = sprite.rect.left
