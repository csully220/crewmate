import pygame
from pygame.locals import *
import time
import xml.etree.ElementTree as ET


class Task:
    def __init__(self, _name, _location, _completion):
        self.name = _name
        self.location = _location
        self.completion = _completion

class Player:
 
    def __init__(self, _name, _color, _tasks=[]):
        self.name = _name
        self.color = _color
        self.tasks = _tasks
        self.img = _color + '_plyr.png'
        self.x = 100
        self.y = 100
 

    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:

    windowWidth = 800
    windowHeight = 600
    bg = ".\data\bg.png"
    players = []
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.game = Game()
        self.players = []

        tree = ET.parse('.\data\players.xml')
        _players = tree.getroot().findall('Player')
        for _p in _players:
            _pn = _p.get('name')
            _pc = _p.get('color')
            new_plyr = Player(_pn, _pc)
            _tasks = _p.find('Tasks').findall('Task')
            for _t in _tasks:
                _tn = _t.get('name')
                _tl = _t.get('location')
                _tc = int(_t.get('completion'))
                new_plyr.tasks.append(Task(_tn, _tl, _tc))
            self.players.append(new_plyr)
        
        for p in self.players:
            print("Players:")
            print(p.name)
            print(p.color)
            print("Tasks:")
            for t in p.tasks:
                print(t.name)
                print(t.location)
                print(t.completion)
                
        self.player = self.players[0]
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Among Us Crewmate Simulator')
        self._running = True
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
        #if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
        #    print("You lose! Collision: ")
        #    print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
        #    print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
        #    exit(0)
 
    def on_render(self):
        self._display_surf.image(self.bg)
        s#elf.player.draw(self._display_surf, self._image_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
