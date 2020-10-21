import pygame
from pygame.locals import *

class Task:
    def __init__(self, _name, _location, _completion, _owner):
        self.name = _name
        self.owner = _owner
        self.location = _location
        self.completion = _completion

class Player(pygame.sprite.Sprite):
    step = 10
    direction = 'RIGHT'
    chosen = False
    
    def __init__(self, _name, _color, _tasks=[]):
        super().__init__()
        self.name = _name
        self.color = _color
        self.tasks = _tasks
        _plyrimgstr = './data/images/players/' + _color + '_small.png'
        #_plyrimgstr = './data/red_plyr.png'
        self.leftimg = pygame.image.load(_plyrimgstr).convert()
        self.rightimg = pygame.transform.flip(self.leftimg, True, False)
        self.img = self.rightimg
        self.image = self.rightimg
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 150
        #self.btn_choose = PlayerButton(self.color,self.name)

    def moveRight(self):
        if self.dx < 5:
            self.dx = self.dx + 1
        self.direction = 'LEFT'
 
    def moveLeft(self):
        if self.dx > -5:
            self.dx = self.dx - 1
        #self.x = self.x - self.step
        self.direction = 'RIGHT'
 
    def moveUp(self):
        #if self.dy > -5:
            self.dy = self.dy - 1
        #self.y = self.y - self.step
 
    def moveDown(self):
        #if self.dy < 5:
            self.dy = self.dy + 1
        #self.y = self.y + self.step

    def stop(self):
        self.dx = 0
        self.dy = 0
 
    def update(self):
        if self.rect.x > 0 and self.rect.x < 1200:
            self.rect.x += self.dx
        if self.rect.y > 0 and self.rect.y < 600:
            self.rect.y += self.dy
        #k = 1
        #if self.dx < 0:
        #    self.dx += k
        #if self.dx > 0:
        #    self.dx -= k
        #if self.dy < 0:
        #   self.dy += k
        #if self.dy > 0:
        #    self.dy -= k


    #def draw(self, surface):
    #    if self.direction == 'LEFT':
    #        surface.blit(self.leftimg,(self.x,self.y))
    #   elif self.direction == 'RIGHT':
    #       surface.blit(self.rightimg,(self.x,self.y)) 
