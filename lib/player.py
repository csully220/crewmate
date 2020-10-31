import pygame
from pygame.locals import *
import time

class Task:
    def __init__(self, _id, _desc, _location, _complete, _owner, _frequency, _recurring, _created, _deadline, _owner_id):
        self.id = _id
        self.desc = _desc
        self.owner = _owner
        self.owner_id = _owner_id
        self.location = _location
        self.frequency = _frequency
        self.recurring = _recurring
        self.complete = _complete
        self.created = _created
        self.deadline = _deadline

class Player(pygame.sprite.Sprite):
    step = 10
    direction = 'RIGHT'
    chosen = False
    
    def __init__(self, _id, _name, _color, _tasks=[]):
        super().__init__()
        self.id = _id
        self.name = _name
        self.color = _color
        self.tasks = _tasks
        _plyrimgstr = './data/images/players/' + _color + '_small.png'
        #_plyrimgstr = './data/red_plyr.png'
        self.rightimg = pygame.image.load(_plyrimgstr).convert()
        self.leftimg = pygame.transform.flip(self.rightimg, True, False)
        self.img = self.rightimg
        self.image = self.rightimg
        self.x = 30
        self.y = 80
        self.dx = 0
        self.dy = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #self.btn_choose = PlayerButton(self.color,self.name)

    def moveRight(self):
        if self.dx < 8:
            self.dx = self.dx + 2
        self.image = self.rightimg
 
    def moveLeft(self):
        if self.dx > -8:
            self.dx = self.dx - 2
        self.image = self.leftimg
 
    def moveUp(self):
        if self.dy > -8:
            self.dy = self.dy - 2
 
    def moveDown(self):
        if self.dy < 8:
            self.dy = self.dy + 2

    def stop(self):
        self.dx = 0
        self.dy = 0
 
    def update(self):
        if self.dx < 0:
            self.dx += 1
        if self.dx > 0:
            self.dx -= 1
        if self.dy < 0:
            self.dy += 1
        if self.dy > 0:
            self.dy -= 1
    
        if self.rect.x > 0 and self.rect.x < 1200:
            self.rect.x += self.dx
        else:
            self.rect.x = 30
        if self.rect.y > 0 and self.rect.y < 600:
            self.rect.y += self.dy
        else:
            self.rect.y = 80
