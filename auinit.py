import os
os.chdir(r'C:\Users\colin\Documents\Code Projects\crewmate')

import pygame
from pygame.locals import *
import time
import xml.etree.ElementTree as ET
from auwidgets import *
from auplayer import *


def getcom():
    tree = ET.parse('.\data\players.xml')
    ET.parse('.\data\players.xml')
    _players = tree.getroot().findall('Player')
    p = _players[0]
    xt = p.find('Tasks').findall('Task')
    t = xt[0]
    c = t.get('completion')
    return xt