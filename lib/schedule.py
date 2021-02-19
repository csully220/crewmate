import datetime


class Occurrence:
    title = ''
    description = ''
    start = ''
    end = ''
    cancelled = False
    original_start = ''
    original_end = ''
    created_on = ''
    updated_on = ''
    completed = False
    completed_on = None
    event = ''

    @property
    def taskid(self):
        return (self.event)

    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600

    def from_JSON(cls, json):
        oc = json
        occurrences = []
        for o in oc:
            new_o = Occurrence()
            o.event = oc.get('event')
            o.title = oc.get('title')
            o.description = oc.get('description')
            o.start = oc.get('start')
            o.end = oc.get('end')
            o.completed = oc.get('completed')
            o.completed_on = oc.get('completed_on')
            occurrences.append(new_o)
        return occurrences

class Calendar:

    name = ''
    slug = ''

    def __str__(self):
        return self.name