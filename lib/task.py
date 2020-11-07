import datetime

class Task:
    def __init__(self, _id='', _desc='', _location='', _complete='', _freq_data={}, _created='', _assignee_id='', _last_completed=''):
        self.id = _id
        self.desc = _desc
        self.assignee_id = _assignee_id
        self.location = _location
        self.complete = _complete
        self.created = _created
        self.freq_data = _freq_data
        self.last_completed = _last_completed
        
    def isOverDue(self):
        #if not self.complete:
        print("last  " + self.last_completed)
        print("now  " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
            