import bisect

class Metadata(object):
    def __init__(self):
        self.fields = []
        self.pk = None

    def add_field(self, field):
        bisect.insort(self.fields, field)
        self.setup_pk(field)

    def setup_pk(self, field):
        if not self.pk and field.primary_key:
            self.pk = field

    @property
    def concrete_fields(self):
        return (f for f in self.fields if f.concrete)