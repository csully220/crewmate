import xml.etree.ElementTree as ET
from lib.player import *
from lib.task import *
import requests
import datetime
import pytz
from lib.schedule import Occurrence

class NetworkDatabase:

    def __init__(self, _ip='127.0.0.1', _port='8000'):
        self.server_ip = _ip
        self.server_port = _port
        self.urlbase = 'http://' + self.server_ip + ':' + self.server_port + '/taskapi/'


    def getOccurrences(self, playerid, period='day'):
        query = '?playerid=' + str(playerid) + '&period=' + period
        try:
            resp = requests.get(self.urlbase + 'occurrences/' + query)
        except:
            print('ERROR: Failed to get response from server')
            return []
        oc = resp.json()
        occurrences = []
        for o in oc:
            new_o = Occurrence()
            new_o.event = o.get('event')
            new_o.title = o.get('title')
            new_o.description = o.get('description')
            new_o.start = o.get('start')
            new_o.end = o.get('end')
            new_o.cancelled = o.get('cancelled')
            new_o.original_start = o.get('original_start')
            new_o.original_end = o.get('original_end')
            new_o.completed = o.get('completed')
            new_o.completed_on = o.get('completed_on')
            new_o.failed = o.get('failed')
            
            occurrences.append(new_o)
        return occurrences

    def getPlayer(self, pk):
        try:
            resp = requests.get(self.urlbase + 'player/' + str(pk))
        except:
            print('ERROR: Failed to get response from server')
            return []
        pe = resp.json()
        pn = pe.get('name')
        pc = pe.get('color')
        pid = pe.get('id')
        new_player = Player(pid, pn, pc)
        return new_player


    def getPlayerTasks(self, player_id):
        try:
            resp = requests.get(self.urlbase + 'playertasks/?assignee=' + str(player_id))
        except:
            print('ERROR: Failed to get response from server')
            return []
        task_elements = resp.json()
        tasks = []
        for t in task_elements:
        
           id = t.get('id')
           start = t.get('start')
           end = t.get('end')
           title = t.get('title')
           description = t.get('description')
           created_on = t.get('created_on')
           updated_on = t.get('updated_on')
           end_recurring_period = t.get('end_recurring_period')
           color_event = t.get('color')
           location = t.get('location')
           creator = t.get('creator')
           rule = t.get('rule')
           calendar = t.get('calendar')
           assignee = t.get('assignee')
       
           tasks.append(Task(id, start, end, title, description, created_on, updated_on, end_recurring_period, color_event, location, creator, rule, calendar, assignee))
        return tasks

    def getAllPlayers(self):
        try:
            resp = requests.get(self.urlbase + 'playerlist')
        except:
            print('ERROR: Failed to get response from server')
            return []
        player_elements = resp.json()
        players = []
        for pe in player_elements:
            pid = pe.get('id')
            color = pe.get('color')
            new_player = Player(pid, color)
            new_player.name = pe.get('name')
            new_player.account_balance = pe.get('account_balance')
            players.append(new_player)
        return players

    def getTask(self,pk):
        try:
            resp = requests.get(self.urlbase + 'tasks/' + str(pk) + '/')
        except:
            print('ERROR: Failed to get response from server')
            return []
        t = resp.json()
        
        tpk = t.get('pk')
        tdesc = t.get('description')
        tl = t.get('location')

        id = t.get('id')
        start = t.get('start')
        end = t.get('end')
        title = t.get('title')
        description = t.get('description')
        created_on = t.get('created_on')
        updated_on = t.get('updated_on')
        end_recurring_period = t.get('end_recurring_period')
        color_event = t.get('color')
        location = t.get('location')
        creator = t.get('creator')
        rule = t.get('rule')
        calendar = t.get('calendar')
        assignee = t.get('assignee')
        
        return Task(id, start, end, title, description, created_on, updated_on, end_recurring_period, color_event, location, creator, rule, calendar, assignee)

    def updateOccurrence(self, occ, playerid):
        try:
            jsondict = self.serialize(occ)
            resp = requests.post(self.urlbase + 'occurrences/?playerid=' + str(playerid) + '&period=day', json=jsondict)
        except Exception as e:
            print('ERROR: Failed to get response from server')
            print(e)
            return

    def serialize(self, oc):
        if type(oc) == Occurrence:
            jstr = {}
            jstr['title'] = oc.title
            jstr['description'] = oc.description
            jstr['start'] = oc.start
            jstr['end'] = oc.end
            jstr['original_start'] = oc.original_start
            jstr['original_end'] = oc.original_end
            jstr['cancelled'] = oc.cancelled
            now = datetime.datetime.now(datetime.timezone.utc)
            dt = now.isoformat(timespec='seconds')
            dt1 = dt[:-6]
            dt2 = dt1 + 'Z'
            jstr['completed'] = oc.completed
            if oc.completed:
                jstr['completed_on'] = dt2
            jstr['event'] = oc.event
            
            return jstr
        else:
            print('Serialize failed')

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
