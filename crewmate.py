import pygame
from pygame.locals import *
import time
import xml.etree.ElementTree as ET
from auwidgets import *
from auplayer import *

class App:

    windowWidth = 1200
    windowHeight = 600
    bg = pygame.image.load(r'.\data\images\bg_welcome.png')
    players = {}
    plyrbtns = []
    tskbtns = []
    buttons = []
    
 
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.players = {}
        self.sprites = pygame.sprite.Group()
        
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
        self.display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.RESIZABLE)
        pygame.display.set_caption('Crewmate IRL Task Simulator')
        
        #read in the player information
        self.tree = ET.parse('.\data\players.xml')
        _players = self.tree.getroot().findall('Player')
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
                print('completion ' + str(_tc))
                tasks.append(Task(_tn, _tl, _tc, _pn))
            new_plyr.tasks = tasks
            self.players[new_plyr.name] = new_plyr
        self.player = self.players['Common']
        
        self.menu = 'WELCOME'
        self.lastMenu = 'NONE'
        self.font_sm = pygame.font.SysFont('Comic Sans MS', 26)
        self.font_med = pygame.font.SysFont('Comic Sans MS', 32)
        self.font_lg = pygame.font.SysFont('Comic Sans MS', 40)
        

        #print(self.player.name)
        self.sprites.add(self.player)
        
        self.running = True
 
    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
 
    def on_loop(self):
        self.sprites.update()
        if self.menu != self.lastMenu:
            self.lastMenu = self.menu
            self.plyrbtns.clear()
            self.buttons.clear()
            self.tskbtns.clear()
            
            if self.menu == 'WELCOME':

                #self.player.draw(self.display_surf)
                pbx = 60
                pby = 100
                yofs = 0
                i = 0
                for pn, po in self.players.items():
                    if pn != 'Common':
                        _btn = PlayerButton(po.color, po.name)
                        if i == 4:
                            pby = 100
                            pbx = 150
                            yofs = 0
                        _btn.x = pbx
                        _btn.y = pby + yofs
                        yofs = yofs + 94
                        #_btn.draw(self.display_surf, po.chosen)
                        i += 1;
                        self.addWidget(_btn)

                self.addWidget(self.btn_plyrsel)
                self.addWidget(self.btn_tasks)

            elif self.menu == 'TASKS':
                _x = 60
                _y = 160
                _yofs = 40
                # Player tasks
                
                _y += 40
                _x += 30
                for _t in self.player.tasks:
                    #print(t)
                    _strtsk = _t.location + ' - ' + _t.name
                    _chk = _t.completion == 1
                    _chkbx = Checkbox(True, _strtsk, _x - 30, _y + 12)
##                    _chkbx.desc = _strtsk
##                    _chkbx.checked = _t.completion
##                    _chkbx.x = _x - 30
##                    _chkbx.y = _y + 12
                    _y = _y + _yofs
                    self.addWidget(_chkbx)

    def on_render(self):
        self.display_surf.blit(self.bg, (0, 0))
        # Render Welcome Screen
        if self.menu == 'WELCOME':
            self.display_surf.blit(self.bg, (0, 0))
            self.display_surf.blit(self.font_med.render('Select Player', False, white), (60,30))
            self.display_surf.blit(self.font_lg.render('Crewmate IRL Task Simulator', False, white), (320,220))
            for _pb in self.plyrbtns:
                _pb.draw(self.display_surf, self.players[_pb.name].chosen)
            self.btn_plyrsel.draw(self.display_surf)
            self.btn_tasks.draw(self.display_surf)

        # Render Task List Screen
        elif self.menu == 'TASKS':
            self.display_surf.blit(self.bg, (0, 0))
            # calculate amount of fill
            tot_tsks = len(self.player.tasks)
            comp_tsks = 0
            for t in self.player.tasks:
                if t.completion == 1:
                    comp_tsks += 1
            ratio = comp_tsks/tot_tsks
            fill_w = 845
            scaled_w = round(fill_w * ratio)
            
            tbar = pygame.image.load(r'.\data\images\taskbar.png')
            tbar_fill= pygame.Rect(66, 66, scaled_w, 68)
            self.display_surf.blit(tbar, (60, 60))
            pygame.draw.rect(self.display_surf, green, tbar_fill)
            self.display_surf.blit(tbar, (60, 60))
            self.display_surf.blit(self.font_med.render(self.player.name + '\'s Tasks:' , False, white), (60,160))
            for _t in self.tskbtns:
                _t.draw(self.display_surf)
        self.sprites.draw(self.display_surf)
        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False
 
        while( self.running ):
            pygame.event.pump()
            ev = pygame.event.get()

            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    mspos = pygame.mouse.get_pos()
                    if self.menu == 'WELCOME':
                        # CHOOSE PLAYER
                        _plyrclkd = False
                        for _pb in self.plyrbtns:
                            if _pb.get_rect().collidepoint(mspos):
                                print('Chose ' + _pb.name)
                                self.player = self.players[_pb.name]
                                _plyrclkd = True
                                #self.players[_pb.name].chosen = True
                        if(_plyrclkd):
                            _plyrclkd = False
                            for pn, po in self.players.items():
                                po.chosen = False
                                if po.name == self.player.name:
                                    po.chosen = True
                            self.menu = 'TASKS'
                            self.bg = pygame.image.load(r'.\data\images\bg_sparse.png')

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
                        # TASK CHECKBOXES
                        idx = 0
                        for tb in self.tskbtns:
                            _tbrect = pygame.Rect(tb.x, tb.y, tb.w, tb.h)
                            if _tbrect.collidepoint(mspos):
                                _ptask = None
                                _plyrs = self.tree.getroot().findall('Player')
                                for _plyr in _plyrs:
                                    if _plyr.get('name') == self.player.name:
                                        _ptasks = _plyr.find('Tasks').findall('Task')
                                        _ptask = _ptasks[idx]
                                if self.player.tasks[idx].completion > 0:
                                    self.player.tasks[idx].completion = 0
                                    _ptask.set('completion', '0')
                                    print('Task incomplete')
                                elif self.player.tasks[idx].completion == 0:
                                    self.player.tasks[idx].completion = 1
                                    _ptask.set('completion', '1')
                                    print('Task complete')
                                self.lastMenu = 'NONE'
                            idx += 1
                        # EXIT
                        exit_rect = pygame.Rect(76, 540, 100, 50)
                        if exit_rect.collidepoint(mspos):
                            self.menu = 'WELCOME'
                            self.bg = pygame.image.load(r'.\data\images\bg_welcome.png')
                    print(mspos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player.moveRight()
                        #print('right')
                    if event.key == pygame.K_LEFT:
                        self.player.moveLeft()
                        #print('left')
                    if event.key == pygame.K_UP:
                        self.player.moveUp()
                        #print('up')
                    if event.key == pygame.K_DOWN:
                        self.player.moveDown()
                        #print('down')
                    if event.key == pygame.K_SPACE:
                        self.player.stop()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        

##            keys = pygame.key.get_pressed() 
## 
##            if (keys[K_RIGHT]):
##                self.player.moveRight()
## 
##            if (keys[K_LEFT]):
##                self.player.moveLeft()
## 
##            if (keys[K_UP]):
##                self.player.moveUp()
## 
##            if (keys[K_DOWN]):
##                self.player.moveDown()
##            if (keys[K_SPACE]):
##                self.player.stop()
##            if (keys[K_ESCAPE]):
##                self.running = False
                
            self.on_loop()
            self.on_render()

            self.clock.tick(30)
            #time.sleep (50.0 / 1000.0);
        self.tree.write('players.xml')
        self.on_cleanup()
        
    def addWidget(self, widget):
        if type(widget) == Checkbox:
            #print('Checkbox')
            self.tskbtns.append(widget)
        if type(widget) == Button:
            #print('Button')
            self.buttons.append(widget)
        if type(widget) == PlayerButton:
            #print('Player Button')
            self.plyrbtns.append(widget)   

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
