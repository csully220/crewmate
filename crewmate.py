import pygame
from pygame.locals import *
import time
import configparser
import requests

from lib.widgets import *
from lib.player import *
from lib.database import *

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
        self.clock = pygame.time.Clock()
        self.running = True
        self.display_surf = None
        self.image_surf = None
        config = configparser.ConfigParser()
        config.read('.\data\crewmate.cfg')
        if config['general']['database_type'] == 'local':
            self.db = XmlDatabase('.\data\players.xml')
        elif config['general']['database_type'] == 'network':
            ip = config['network']['server_ip']
            port = config['network']['server_port']
            self.db = NetworkDatabase(ip, port)

        
        #for p in self.players:
        #    print("Players:")
        #    print(p.name)
        #    print(p.color)
        #    print("Tasks:")
        #    for t in p.tasks:
        #        print(t.name)
        #        print(t.location)
        #        print(t.complete)

        #format the menus

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.RESIZABLE)
        pygame.display.set_caption('Crewmate IRL Task Simulator')

        #read in the player information
        _plyrs = self.db.getAllPlayers()
        self.players = {}
        for _p in _plyrs:
            self.players[_p.name] = _p
            self.sprites = pygame.sprite.Group()

        self.player = self.players['Common']
        self.player.chosen = True

        self.menu = 'WELCOME'
        self.lastMenu = 'NONE'
        self.font_sm = pygame.font.SysFont('Comic Sans MS', 26)
        self.font_med = pygame.font.SysFont('Comic Sans MS', 32)
        self.font_lg = pygame.font.SysFont('Comic Sans MS', 40)

        self.sprites.add(self.player)

        self.running = True

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

    def on_loop(self):
        self.sprites.update()
        self.nowtime = time.localtime()
        self.current_date = time.strftime("%D", self.nowtime)
        self.current_time = time.strftime("%H:%M:%S", self.nowtime)
        if self.menu != self.lastMenu:
            self.lastMenu = self.menu
            self.plyrbtns.clear()
            self.buttons.clear()
            self.tskbtns.clear()
            
            if self.menu == 'WELCOME':
                #self.player.draw(self.display_surf)
                center = len(self.players)/2
                xofs = 100
                pbx = 600 - (center * (xofs-1)) - (xofs/2)
                pby = 236
                i = 0
                for pn, po in self.players.items():
                    if pn != 'Common':
                        _btn = PlayerButton(po.color, po.name)
                        _btn.y = pby
                        pbx += xofs
                        _btn.x = pbx
                        i += 1;
                        self.addWidget(_btn)
                        
                btn_common = Button('common', 'Common', 400, 356)
                btn_progress = Button('tasks', 'Progress', 606, 356)
                
                self.addWidget(btn_common)
                self.addWidget(btn_progress)

        if self.menu == 'TASKS':
            _x = 90
            _y = 200
            _yofs = 40
            # Player tasks
            for _t in self.player.tasks:
                #print(t)
                _dl = time.strftime("%D - %H:%M", _t.deadline)
                #tr = time.strftime("%H:%M:%S", _t.deadline) - time.strftime("%H:%M:%S", self.nowtime)
                _strtsk = _t.location + ' - ' + _t.name # + '   Deadline: ' + _dl
                _chk = _t.complete == 1
                _chkbx = Checkbox(_chk, _strtsk, _x - 30, _y + 12)
                _y = _y + _yofs
                self.addWidget(_chkbx)

    def on_render(self):
        self.display_surf.blit(self.bg, (0, 0))
        # Render Welcome Screen
        if self.menu == 'WELCOME':
            self.display_surf.blit(self.bg, (0, 0))
            self.display_surf.blit(self.font_med.render(self.current_date, False, white), (60,30))
            self.display_surf.blit(self.font_med.render(self.current_time, False, white), (940,30))
            self.display_surf.blit(self.font_lg.render('Crewmate IRL Task Simulator', False, white), (320,160))
            for _pb in self.plyrbtns:
                _pb.draw(self.display_surf, self.players[_pb.name].chosen)
            for _b in self.buttons:
                _b.draw(self.display_surf)

        # Render Task List Screen
        elif self.menu == 'TASKS':
            self.display_surf.blit(self.bg, (0, 0))
            # calculate amount of fill
            tot_tsks = len(self.player.tasks)
            comp_tsks = 0
            for t in self.player.tasks:
                if t.complete == 1:
                    comp_tsks += 1
            if tot_tsks:
                ratio = comp_tsks/tot_tsks
            else:
                ratio = 0
            fill_w = 845
            scaled_w = round(fill_w * ratio)
            
            tbar = pygame.image.load(r'.\data\images\taskbar.png')
            tbar_fill= pygame.Rect(66, 66, scaled_w, 68)
            self.display_surf.blit(tbar, (60, 60))
            pygame.draw.rect(self.display_surf, green, tbar_fill)
            self.display_surf.blit(tbar, (60, 60))
            if self.player.name != 'Common':
                _lbl = self.player.name + '\'s Tasks:'
            else:
                _lbl = self.player.name + ' Tasks:'
            self.display_surf.blit(self.font_med.render(_lbl , False, white), (60,160))
            for _t in self.tskbtns:
                _t.draw(self.display_surf)
        #self.sprites.draw(self.display_surf)
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
                        # PLAYER SELECT BUTTONS
                        _plyrclkd = False
                        for _pb in self.plyrbtns:
                            if _pb.get_rect().collidepoint(mspos):
                                print('Chose ' + _pb.name)
                                self.sprites.remove(self.player)
                                self.player = self.players[_pb.name]
                                self.sprites.add(self.player)
                                _plyrclkd = True
                        if(_plyrclkd):
                            _plyrclkd = False
                            for pn, po in self.players.items():
                                po.chosen = False
                                if po.name == self.player.name:
                                    po.chosen = True
                            self.menu = 'TASKS'
                            self.bg = pygame.image.load(r'.\data\images\bg_sparse.png')

                        # OTHER BUTTONS
                        for _b in self.buttons:
                            if _b.rect.collidepoint(mspos):
                                print(_b.action)
                                if _b.action == 'common':
                                    self.player = self.players['Common']
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
                                print(idx)
                                if self.player.tasks[idx].complete > 0:
                                    self.player.tasks[idx].complete = 0
                                    print('Task incomplete')
                                elif self.player.tasks[idx].complete == 0:
                                    self.player.tasks[idx].complete = 1
                                    print('Task complete')
                                self.db.updateTaskElement(self.player.tasks[idx])
                                self.lastMenu = 'NONE'
                                break;
                            idx += 1
                         # EXIT
                        exit_rect = pygame.Rect(76, 540, 100, 50)
                        if exit_rect.collidepoint(mspos):
                            self.menu = 'WELCOME'
                            self.bg = pygame.image.load(r'.\data\images\bg_welcome.png')
                    print(mspos)
                if event.type == pygame.KEYDOWN:
##                    if event.key == pygame.K_RIGHT:
##                        self.player.moveRight()
##                        #print('right')
##                    if event.key == pygame.K_LEFT:
##                        self.player.moveLeft()
##                        #print('left')
##                    if event.key == pygame.K_UP:
##                        self.player.moveUp()
##                        #print('up')
##                    if event.key == pygame.K_DOWN:
##                        self.player.moveDown()
##                        #print('down')
                    if event.key == pygame.K_SPACE:
                        self.player.stop()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        

            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
            if (keys[K_SPACE]):
                self.player.stop()
            if (keys[K_ESCAPE]):
                self.running = False
                
            self.on_loop()
            self.on_render()

            self.clock.tick(30)

        #self.db.saveAll()
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
