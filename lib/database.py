import xml.etree.ElementTree as ET
from lib.player import *
import requests
import datetime

class NetworkDatabase:
    
    def __init__(self, _ip='127.0.0.1', _port='8000'):
        self.server_ip = _ip
        self.server_port = _port
        self.urlbase = 'http://' + self.server_ip + ':' + self.server_port + '/tasker/api/'

    def getPlayerTasks(self, player_id):
        resp = requests.get(self.urlbase + 'playertasks/?assignee=' + str(player_id))
        task_elements = resp.json()
        tasks = []
        for t in task_elements:
            tid = t.get('id')
            tn = t.get('desc')
            tl = t.get('location')
            tf = t.get('once')
            tr = t.get('monday')
            tr = t.get('tuesday')
            tr = t.get('wednesday')
            tr = t.get('thursday')
            tr = t.get('friday')
            tr = t.get('saturday')
            tr = t.get('sunday')
            tr = t.get('biweekly')
            tr = t.get('duethiswk')
            tr = t.get('monthlyy')
            tr = t.get('quarterly')
            tc = int(t.get('complete'))
            tlc = t.get('last_completed')
            tcr = t.get('created')
            tdl = t.get('deadline')
            tpid = t.get('assignee_id')
            tasks.append(Task(tid, tn, tl, tc, pn, tf, tr, tcr, tdl, pid, tlc))
        return tasks
        
    def getAllPlayers(self):
        resp = requests.get(self.urlbase + 'players')
        player_elements = resp.json()
        players = []
        for pe in player_elements:
            pn = pe.get('name')
            pc = pe.get('color')
            pid = pe.get('id')
            new_player = Player(pid, pn, pc)
            pid = pe.get('id')
            query = {'assignee':pid}
            
            resp = requests.get(self.urlbase + 'playertasks/', params=query)
            tasks = []
            print(resp.json())
            task_elements = resp.json()
            for t in task_elements:
                tid = t.get('id')
                tn = t.get('desc')
                tl = t.get('location')
                tf = t.get('once')
                tr = t.get('monday')
                tr = t.get('tuesday')
                tr = t.get('wednesday')
                tr = t.get('thursday')
                tr = t.get('friday')
                tr = t.get('saturday')
                tr = t.get('sunday')
                tr = t.get('biweekly')
                tr = t.get('duethiswk')
                tr = t.get('monthlyy')
                tr = t.get('quarterly')
                tc = t.get('complete')
                tcr = t.get('created')
                tdl = t.get('deadline')
                tpid = t.get('assignee_id')
                tlc = t.get('last_completed')
                tasks.append(Task(tid, tn, tl, tc, pn, tf, tr, tcr, tdl, pid, tlc))
            new_player.tasks = tasks
            players.append(new_player)
        return players

    def updateTaskElement(self, task):
        resp = requests.put(self.urlbase + 'tasks/' + str(task.id) + '/', json=self.serialize(task))
        print(resp.json())
    
    def serialize(self, el):
        if type(el) == Task:
            jstr = {}
            jstr['id'] = el.id
            jstr['desc'] = el.desc
            jstr['location'] = el.location
            jstr['recurring'] = el.recurring
            jstr['freq'] = el.frequency
            jstr['deadline'] = el.deadline
            jstr['complete'] = el.complete
            jstr['created'] = el.created
            jstr['assignee'] = el.assignee_id
            return jstr

class XmlDatabase:

    def __init__(self, _file):
        self.loadFile(_file)
        
    def loadFile(self, _file):
        self.file = _file
        self.tree = ET.parse(_file)
    
    def getAllPlayers(self):
        self.player_elements = self.tree.getroot().findall('Player')
        self.players = []
        for pe in self.player_elements:
            pn = pe.get('name')
            pc = pe.get('color')
            new_player = Player(pn, pc)
            task_elements = pe.find('Tasks').findall('Task')
            tasks = []
            for t in task_elements:
                tn = t.get('desc')
                tl = t.get('location')
                tf = t.get('freq')
                tc = int(t.get('complete'))
                tasks.append(Task(tn, tl, tc, pn, tf))
            new_player.tasks = tasks
            self.players.append(new_player)
        return self.players

    def getPlayerElement(self, _name):
        for pe in self.player_elements:
            if pe.get('name') == _name:
                return pe
        
    def getTaskElements(self, _assignee):
        
        task_elements = pe.find('Tasks').findall('Task')
        return task_elements

    def updateTaskElement(self, _task):
        for pe in self.player_elements:
            if pe.get('name') == _task.assignee:
                task_elements = pe.find('Tasks').findall('Task')
                for te in task_elements:
                    if te.get('name') == _task.name:
                        te.set('complete', str(_task.complete))
                        print('Updated ' + te.get('name') + ' complete ' + str(te.get('complete')))
            

    
    def saveAll(self):
        self.tree.write(self.file)
