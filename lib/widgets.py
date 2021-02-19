import pygame
from pygame.locals import *

green = pygame.Color(68,216,68)
white = pygame.Color(255,255,255)
yellow = pygame.Color(255,235,4)
red = pygame.Color(255,0,0)

class Taskbar():
    def __init__(self, _fill=50, _idx=0, _x=0, _y=0):
        self.img = pygame.image.load(r'./data/images/buttons/taskbar.png')
        self.x = _x
        self.y = _y
        self.w = 860
        self.h = 75
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        surface.blit(self.img,(self.x,self.y))

class Checkbox():
    def __init__(self, _checked=False, _label='', _x=0, _y=0):
        self.checked = _checked
        self.label = _label
        self.x = _x
        self.y = _y
        self.w = 40 
        self.h = 40
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        _font = pygame.font.SysFont('Comic Sans MS', 26)
        if self.checked:
            self.img = pygame.image.load(r'./data/images/buttons/check.png')
            _desc = _font.render(self.label, False, green)

        else:
            self.img = pygame.image.load(r'./data/images/buttons/nocheck.png')
            _desc = _font.render(self.label, False, white)

        surface.blit(self.img,(self.x,self.y))
        surface.blit(_desc,(self.x + 30,self.y - 12))

class TaskCheckbox(Checkbox):
    def __init__(self, _checked=True, _label='', _x=0, _y=0, _id=0):
        self.id = _id
        self.checked = _checked
        self.label = _label
        self.x = _x
        self.y = _y
        self.w = 40 
        self.h = 40
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        _font = pygame.font.SysFont('Comic Sans MS', 26)
        if self.checked:
            self.img = pygame.image.load(r'./data/images/buttons/check.png')
            _desc = _font.render(self.label, False, green)

        else:
            self.img = pygame.image.load(r'./data/images/buttons/nocheck.png')
            _desc = _font.render(self.label, False, white)

        surface.blit(self.img,(self.x,self.y))
        surface.blit(_desc,(self.x + 30,self.y - 12))
        
class Button():
    def __init__(self, _action, _label, _x, _y):
        self.img = pygame.image.load(r'./data/images/buttons/blank.png')
        self.action = _action
        self.active = False
        self.label = _label
        self.x = _x
        self.y = _y
        if _action == 'exit':
            self.w = 160
        else:
            self.w = 192
        self.h = 80
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        _font = pygame.font.SysFont('Comic Sans MS', 32)
        _color = white
        if self.action == 'exit':
            if self.active:
                #_color = green
                _img = pygame.image.load(r'./data/images/buttons/exit_active.png')
            else:
                _color = white
                _img = pygame.image.load(r'./data/images/buttons/exit.png')

            _lbl = _font.render(self.label, False, _color)
            surface.blit(_img,(self.x,self.y))
            surface.blit(_lbl,(self.x + 50,self.y + 16))

        else:
            
            _img = pygame.image.load(r'./data/images/buttons/blank.png')
            if self.active:
                #_color = green
                _img = pygame.image.load(r'./data/images/buttons/active.png')
            _lbl = _font.render(self.label, False, _color)
            surface.blit(_img,(self.x,self.y))
            surface.blit(_lbl,(self.x + 40,self.y + 16))
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class PlayerButton():
    def __init__(self, _color, _name='', _x=0, _y=0):
        self.img = pygame.image.load(r'./data/images/players/' + _color + '_tn.png')
        self.name = _name
        self.color = _color
        self.x = _x
        self.y = _y
        self.w = 90
        self.h = 120
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface, chosen=False, xoffset=0, yoffset=0, center=False):
        if center:
            xoffset += -1 * (self.w/2)
            yoffset += -1 * (self.h/2)
        _font = pygame.font.SysFont('Comic Sans MS', 26)
        #_lbl = _font.render(self.lbl, False, (255, 255, 255))
        _color = white
        if(chosen):
            _color = green
        _lbl = _font.render(self.name, False, _color)

        surface.blit(_lbl, (self.x + xoffset,self.y + yoffset))
        surface.blit(self.img,(self.x + xoffset,self.y + yoffset + 36))
