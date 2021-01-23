class Occurrence:
    event = ''#models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("event"))
    title = '' #models.CharField(_("title"), max_length=255, blank=True)
    description = '' #models.TextField(_("description"), blank=True)
    start = '' #models.DateTimeField(_("start"), db_index=True)
    end = '' #models.DateTimeField(_("end"), db_index=True)
    cancelled = False #models.BooleanField(_("cancelled"), default=False)
    original_start = '' #models.DateTimeField(_("original start"))
    original_end = '' #models.DateTimeField(_("original end"))
    #created_on = '' #models.DateTimeField(_("created on"), auto_now_add=True)
    #updated_on = '' #models.DateTimeField(_("updated on"), auto_now=True)

    @property
    def complete(self):
        return (self.description == 'complete')

    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600
         
    def get_from_JSON(self, json):
        oc = json
        occurrences = []
        for o in oc:
            new_o = Occurrence()
            o.event = oc.get('event')
            o.title = oc.get('title')
            o.description = oc.get('description')
            o.start = oc.get('start')
            o.end = oc.get('end')
            occurrences.append(new_o)
        return occurrences




class Calendar:

    name = ''
    slug = ''

    def __str__(self):
        return self.name