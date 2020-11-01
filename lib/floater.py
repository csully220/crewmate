import pygame
from pygame.locals import *
import random

class Floater(pygame.sprite.Sprite):
    
    def __init__(self, _id):
        super().__init__()
        self.id = _id
        _plyrimgstr = './data/images/players/floaters/floater_' + str(_id) + '.png'
        try:
            self.image = pygame.image.load(_plyrimgstr).convert_alpha()
        except pygame.error:
            _plyrimgstr = './data/images/players/floaters/floater_' + str(random.randrange(1, 6)) + '.png'
            self.image = pygame.image.load(_plyrimgstr).convert_alpha()
        
        vel_max_x = 40
        vel_max_y = 40
        rot_max = 30
        
        self.x = random.randrange(960-20, 960+20)
        self.y = random.randrange(540-20, 540+20)
        self.vel = {'x':random.randrange(-(vel_max_x),vel_max_x), 'y':random.randrange(-(vel_max_y),vel_max_y)}
        self.rotation = random.randrange(-(rot_max), rot_max)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def moveRight(self):
        if self.dx < 8:
            self.dx = self.dx + 2
 
    def moveLeft(self):
        if self.dx > -8:
            self.dx = self.dx - 2
 
    def moveUp(self):
        if self.dy > -8:
            self.dy = self.dy - 2
 
    def moveDown(self):
        if self.dy < 8:
            self.dy = self.dy + 2

    def stop(self):
        self.dx = 0
        self.dy = 0
 
    def rotate(self):
        """rotate an image while keeping its center and size"""
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, self.rotation)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        return rot_image
 
    def update(self):
        self.rotate()
        self.rect.x += self.vel['x']
        self.rect.y += self.vel['y']
