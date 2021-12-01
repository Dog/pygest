from datetime import datetime
import re
from functools import total_ordering

@total_ordering
class Field(object):
    creation_counter = 0

    def __init__(self, api_name=None, primary_key=True):
        self.primary_key=primary_key
        self.api_name = api_name
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def set_attributes_from_name(self, name):
        self.python_name = name
        self.api_name = self.api_name or name
        self.concrete = self.api_name is not None

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, name, self)

    def to_python(self, value: object) -> object:
        return value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Field):
            return (
                self.creation_counter == other.creation_counter and
                getattr(self, 'model', None) == getattr(other, 'model', None)
            )
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Field):
            if (
                self.creation_counter != other.creation_counter or
                not hasattr(self, 'model') and not hasattr(other, 'model')
            ):
                return self.creation_counter < other.creation_counter
            elif hasattr(self, 'model') != hasattr(other, 'model'):
                return not hasattr(self, 'model')
            else:
                return (
                    self.model._meta.model_name < other.model._meta.model_name
                )
        return NotImplemented

    def __hash__(self):
        return hash((
            self.creation_counter,
            self.model._meta.model_name if hasattr(self, 'model') else None,
        ))

date_re = re.compile(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$')

class DateField(Field):
    def parse_date(self, value):
        match = date_re.match(value)
        if match:
            kw = {k: int(v) for k, v in match.groupdict().items()}
            return datetime.date(**kw)

    def to_python(self, value):
        if value is None:
            return value
        return self.parse_date(value)