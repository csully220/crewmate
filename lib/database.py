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

    def getTasksToday(self, playerid):
        query = '?playerid=' + str(playerid) + '&period=week'
        try:
            resp = requests.get(self.urlbase + 'tasks/' + query)
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
            occurrences.append(new_o)
        return occurrences

    def updateOccurrence(self, occurrence):
        try:
            query = '?playerid=' + str(playerid) + '&period=week'
            resp = requests.put(self.urlbase + 'tasks/' + str(task.id) + '/', json=self.serialize(task))
        except:
            print('ERROR: Failed to get response from server')
            return
        print(resp.json())


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
        #pid = pe.get('id')
        #query = {'assignee':pid}
        #try:
        #    resp = requests.get(self.urlbase + 'playertasks/', params=query)
        #except:
        #    print('ERROR: Failed to get response from server')
        #    return []
        #tasks = []
        #print(resp.json())
        #task_elements = resp.json()
        #for t in task_elements:
        #
        #    id = t.get('id')
        #    start = t.get('start')
        #    end = t.get('end')
        #    title = t.get('title')
        #    description = t.get('description')
        #    created_on = t.get('created_on')
        #    updated_on = t.get('updated_on')
        #    end_recurring_period = t.get('end_recurring_period')
        #    color_event = t.get('color')
        #    location = t.get('location')
        #    creator = t.get('creator')
        #    rule = t.get('rule')
        #    calendar = t.get('calendar')
        #    assignee = t.get('assignee')
        #    
        #    tasks.append(Task(id, start, end, title, description, created_on, updated_on, end_recurring_period, color_event, location, creator, rule, calendar, assignee))
        #new_player.tasks = tasks
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

    def updateOccurrence(self, occ):
        try:
            resp = requests.post(self.urlbase + 'occurrences/', json=self.serialize(occ))
        except:
            print('ERROR: Failed to get response from server')
            return
        print(resp.json())

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
            now = datetime.now(timezone.utc)
            dt = now.isoformat(timespec='seconds')
            dt1 = dt[:-6]
            dt2 = dt1 + 'Z'
            #jstr['updated_on'] = dt2
            jstr['completed'] = oc.completed
            if oc.completed:
                jstr['completed_on'] = dt2
            jstr['event'] = oc.event
            
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
