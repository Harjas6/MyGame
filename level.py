import pygame
from settings import *


class Level:
    def __init__(self):
        self.disp_surf = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.make_map()

    def make_map(self):
        self.make_background()
        for row_num, row in enumerate(MAP):
            for col_num, item in enumerate(row):
                x = row_num * TILESIZE
                y = col_num * TILESIZE
                if item == 'p':
                    self.player = Player((x, y), [self.visible_sprites])

    def make_background(self):
        for x in range(0, 10):
            for y in range(0, 10):
                x_pos = x * TILESIZE
                y_pos = y * TILESIZE
                Block((x_pos, y_pos), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.disp_surf)
        self.visible_sprites.update()


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/grass.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = + 1
        else:
            self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed

    def update(self):
        self.input()
        self.move()
