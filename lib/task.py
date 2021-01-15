import datetime

class Task:
    
    def __init__(self, _id, _start, _end, _title, _desc, _created, _updated, _end_rec, _color, _location, _creator, _rule, _calendar, _assignee):

        self.id = _id
        self.start = _start
        self.end = _end
        self.title = _title
        self.description = _desc
        self.created_on = _created
        self.updated_on = _updated
        self.end_recurring_period = _end_rec
        self.color_event = _color
        self.location_ = _location
        self.creator = _creator
        self.rule = _rule
        self.calendar = _calendar
        self.assignee = _assignee
        
        
    def isOverDue(self):
        #if not self.complete:
        #print("last  " + self.last_completed)
        now = datetime.datetime.now(datetime.timezone.utc)
        print("now  " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
            
