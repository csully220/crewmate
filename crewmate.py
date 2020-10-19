import pygame
from pygame.locals import *
import time
import xml.etree.ElementTree as ET


class Task:
    def __init__(self, _name, _location, _completion):
        self.name = _name
        self.location = _location
        self.completion = _completion
        self.btn_complete = Checkbox()

class Player:
    step = 10
    direction = 'RIGHT'
    chosen = False
    
    def __init__(self, _name, _color, _tasks=[]):
        self.name = _name
        self.color = _color
        self.tasks = _tasks
        _plyrimgstr = './data/images/players/' + _color + '_small.png'
        #_plyrimgstr = './data/red_plyr.png'
        self.leftimg = pygame.image.load(_plyrimgstr)
        self.rightimg = pygame.transform.flip(self.leftimg, True, False)
        self.img = self.rightimg
        self.x = 100
        self.y = 100

        self.btn_choose = PlayerButton(self.color,self.name)

    def moveRight(self):
        self.x = self.x + self.step
        self.direction = 'LEFT'
 
    def moveLeft(self):
        self.x = self.x - self.step
        self.direction = 'RIGHT'
 
    def moveUp(self):
        self.y = self.y - self.step
 
    def moveDown(self):
        self.y = self.y + self.step
 
    def draw(self, surface):
        if self.direction == 'LEFT':
            surface.blit(self.leftimg,(self.x,self.y))
        elif self.direction == 'RIGHT':
            surface.blit(self.rightimg,(self.x,self.y)) 


class Checkbox():
    def __init__(self, _checked=False, _x=0, _y=0):
        self.checked = _checked
        if(self.checked):
            self.img = pygame.image.load(r'./data/images/buttons/check.png')
        else:
            self.img = pygame.image.load(r'./data/images/buttons/nocheck.png')
        self.x = _x
        self.y = _y
        self.w = 40 
        self.h = 40
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface, _checked=False):
        if _checked:
            self.img = pygame.image.load(r'./data/images/buttons/check.png')
        else:
            self.img = pygame.image.load(r'./data/images/buttons/nocheck.png')
        surface.blit(self.img,(self.x,self.y))


class Button():
    def __init__(self, _action, _x, _y):
        self.img = pygame.image.load(r'./data/images/buttons/' + _action + '.png')
        self.action = _action
        self.x = _x
        self.y = _y
        self.w = 192
        self.h = 80
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        surface.blit(self.img,(self.x,self.y))



class PlayerButton():
    def __init__(self, _color, _name='', _x=0, _y=0):
        self.img = pygame.image.load(r'./data/images/players/' + _color + '_tn.png')
        self.lbl = _name
        self.color = _color
        self.x = _x
        self.y = _y
        self.w = 90
        self.h = 120
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface, chosen=False):
        _font = pygame.font.SysFont('Comic Sans MS', 26)
        #_lbl = _font.render(self.lbl, False, (255, 255, 255))
        _color = Color(255, 255, 255)
        if(chosen):
            _color = Color(255, 255, 20)
        _lbl = _font.render(self.lbl, False, _color)
        
        surface.blit(_lbl, (self.x,self.y))
        surface.blit(self.img,(self.x,self.y + 36))
        
    def clicked(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False





class App:

    windowWidth = 1200
    windowHeight = 600
    bg = pygame.image.load(r'.\data\images\bg_welcome.png')
    players = []
    plyrbtns = []
    tskbtns = []
    menu = ''
 
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.players = {}
        self.menu = 'WELCOME'

        #read in the player information
        tree = ET.parse('.\data\players.xml')
        _players = tree.getroot().findall('Player')
        for _p in _players:
            _pn = _p.get('name')
            _pc = _p.get('color')
            new_plyr = Player(_pn, _pc)
            _xmltasks = _p.find('Tasks').findall('Task')
            tasks = []
            for _t in _xmltasks:
                _tn = _t.get('name')
                _tl = _t.get('location')
                _tc = int(_t.get('completion'))
                tasks.append(Task(_tn, _tl, _tc))
            new_plyr.tasks = tasks
            self.players[new_plyr.name] = new_plyr
        self.player = self.players['Common']
        
        #for p in self.players:
        #    print("Players:")
        #    print(p.name)
        #    print(p.color)
        #    print("Tasks:")
        #    for t in p.tasks:
        #        print(t.name)
        #        print(t.location)
        #        print(t.completion)

        #format the menus
        self.btn_plyrsel = Button('select', 400, 356)
        self.btn_tasks = Button('tasks', 606, 356)

        
 
    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 40)
        self.display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.RESIZABLE)
        pygame.display.set_caption('Among Us Crewmate Simulator')
        self.running = True
 
    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
 
    def on_loop(self):
        
        pass
        

 
    def on_render(self):
        
        if self.menu == 'WELCOME':
            self.plyrbtns.clear()
            self.display_surf.blit(self.bg, (0, 0))
            lbl_plyrsel = self.myfont.render('Select Player', False, (255, 255, 255))
            self.display_surf.blit(lbl_plyrsel, (60,30))
            lbl_plyrsel = self.myfont.render('Crewmate IRL Task Simulator', False, (255, 255, 255))
            self.display_surf.blit(lbl_plyrsel, (320,220))
            #self.player.draw(self.display_surf)
            pbx = 60
            pby = 100
            yofs = 0
            i = 0
            for pn, po in self.players.items():
                #if pn != 'Common':
                _btn = po.btn_choose
                if i == 4:
                    pby = 100
                    pbx = 150
                    yofs = 0
                _btn.x = pbx
                _btn.y = pby + yofs
                yofs = yofs + 94
                _btn.draw(self.display_surf, po.chosen)
                i += 1;

            self.btn_plyrsel.draw(self.display_surf)
            self.btn_tasks.draw(self.display_surf)
            
        elif self.menu == 'TASKS':
            self.tskbtns.clear()
            self.display_surf.blit(self.bg, (0, 0))
            _font = pygame.font.SysFont('Comic Sans MS', 26)
            _lbl = _font.render('Your Tasks:' , False, (255, 255, 255))
            self.display_surf.blit(_lbl, (60,60))
                
            _x = 90
            _y = 100
            _yofs = 40
            # Player tasks
            for t in self.player.tasks:
                #print(t)
                _strtsk = t.location + ' - ' + t.name
                _color = Color(255, 255, 255)
                if t.completion:
                    _color = Color(255, 255, 20)
                _lbl = _font.render(_strtsk , False, _color)
                self.display_surf.blit(_lbl, (_x,_y))
                
                _chkbx = t.btn_complete
                _chkbx.x = _x - 30
                _chkbx.y = _y + 12
                _chkbx.draw(self.display_surf, t.completion)
                self.tskbtns.append(_chkbx)
                _y = _y + _yofs
  
        pygame.display.flip()



    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False
 
        while( self.running ):
            ev = pygame.event.get()

            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    mspos = pygame.mouse.get_pos()
                    if self.menu == 'WELCOME':
                        # CHOOSE PLAYER
                        _plyrclkd = False
                        for pn, po in self.players.items():
                            if po.btn_choose.get_rect().collidepoint(mspos):
                                print('Chose ' + pn)
                                self.player = po
                                _plyrclkd = True
                                po.chosen = True
                        if(_plyrclkd):
                            _plyrclkd = False
                            for pn, po in self.players.items():
                                po.chosen = False
                                if po.name == self.player.name:
                                    po.chosen = True
                        # SELECT
                        if self.btn_plyrsel.rect.collidepoint(mspos):
                            print('Click!')
                            self.menu = 'TASKS'
                            self.bg = pygame.image.load(r'.\data\images\bg_sparse.png')
                        # TASKS
                        if self.btn_tasks.rect.collidepoint(mspos):
                            self.menu = 'TASKS'
                            self.bg = pygame.image.load(r'.\data\images\bg_sparse.png')
                        # EXIT
                        exit_rect = pygame.Rect(76, 540, 100, 50)
                        if exit_rect.collidepoint(mspos):
                            print('Exit!')
                            self.running = False
                            
                    elif self.menu == 'TASKS':
                        idx = 0
                        for tb in self.tskbtns:
                            _tbrect = pygame.Rect(tb.x, tb.y, tb.w, tb.h)
                            if _tbrect.collidepoint(mspos):
                                if self.player.tasks[idx].completion > 0:
                                    self.player.tasks[idx].completion = 0
                                    print('Task incomplete')
                                elif self.player.tasks[idx].completion == 0:
                                    self.player.tasks[idx].completion = 1
                                    print('Task complete')
                            idx += 1
                        # EXIT
                        exit_rect = pygame.Rect(76, 540, 100, 50)
                        if exit_rect.collidepoint(mspos):
                            self.menu = 'WELCOME'
                            self.bg = pygame.image.load(r'.\data\images\bg_welcome.png')
                    print(mspos)

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
                self.running = False

            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
