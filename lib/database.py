import xml.etree.ElementTree as ET
from lib.player import *
from lib.task import *
import requests
import datetime
import pytz

class NetworkDatabase:
    
    def __init__(self, _ip='127.0.0.1', _port='8000'):
        self.server_ip = _ip
        self.server_port = _port
        self.urlbase = 'http://' + self.server_ip + ':' + self.server_port + '/taskapi/'

    def getPlayer(self, pk):
        try:
            resp = requests.get(self.urlbase + 'players/' + str(pk))
        except:
            print('ERROR: Failed to get response from server')
            return []
        pe = resp.json()
        pn = pe.get('name')
        pc = pe.get('color')
        pid = pe.get('id')
        new_player = Player(pid, pn, pc)
        pid = pe.get('id')
        query = {'assignee':pid}
        try:
            resp = requests.get(self.urlbase + 'playertasks/', params=query)
        except:
            print('ERROR: Failed to get response from server')
            return []
        tasks = []
        print(resp.json())
        task_elements = resp.json()
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
        new_player.tasks = tasks
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
            resp = requests.get(self.urlbase + 'players')
        except:
            print('ERROR: Failed to get response from server')
            return []
        player_elements = resp.json()
        players = []
        for pe in player_elements:
            pn = pe.get('name')
            pc = pe.get('color')
            pid = pe.get('id')
            new_player = Player(pid, pn, pc)
            pid = pe.get('id')
            query = {'assignee':pid}
            try:
                resp = requests.get(self.urlbase + 'playertasks/', params=query)
            except:
                print('ERROR: Failed to get response from server')
                return []
            tasks = []
            #print(resp.json())
            task_elements = resp.json()
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
            new_player.tasks = tasks
            players.append(new_player)
        return players

    def updateTaskElement(self, task):
        try:
            resp = requests.put(self.urlbase + 'tasks/' + str(task.id) + '/', json=self.serialize(task))
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
           
            
    def serialize(self, el):
        if type(el) == Task:
            jstr = {}
            jstr['id'] = el.id
            jstr['desc'] = el.desc
            jstr['location'] = el.location
            jstr['complete'] = el.complete
            jstr['created'] = el.created
            #jstr['last_completed'] = el.last_completed
            
            jstr['once'] = el.freq_data['once']
            jstr['monday'] = el.freq_data['monday']
            jstr['tuesday'] = el.freq_data['tuesday']
            jstr['wednesday'] = el.freq_data['wednesday']
            jstr['thursday'] = el.freq_data['thursday']
            jstr['friday'] = el.freq_data['friday']
            jstr['saturday'] = el.freq_data['saturday']
            jstr['sunday'] = el.freq_data['sunday']
            jstr['biweekly'] = el.freq_data['biweekly']
            jstr['duethiswk'] = el.freq_data['duethiswk']
            jstr['monthly'] = el.freq_data['monthly']
            jstr['quarterly'] = el.freq_data['quarterly']
            
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
