import inspect
from .metadata import Metadata

def _has_contribute_to_class(value):
    return not inspect.isclass(value) and hasattr(value, 'contribute_to_class')

class BaseModel(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell

        contributable_attrs = {}
        for obj_name, obj in attrs.items():
            if _has_contribute_to_class(obj):
                contributable_attrs[obj_name] = obj
            else:
                new_attrs[obj_name] = obj

        new_class = super().__new__(cls, name, bases, new_attrs, **kwargs)
        new_class.add_to_class('_meta', Metadata())

        for obj_name, obj in contributable_attrs.items():
            new_class.add_to_class(obj_name, obj)

        return new_class

    def add_to_class(cls, name, value):
        if _has_contribute_to_class(value):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

class Model(metaclass=BaseModel):
    def __init__(self, *args, **kwargs):
        cls = self.__class__
        meta = self._meta
        _setattr = setattr

        fields_iter = iter(meta.concrete_fields)

        for val, field in zip(args, fields_iter):
            _setattr(self, field.python_name, field.to_python(val))

        super().__init__()

    @classmethod
    def from_api(cls, data):
        values = [data.get(f.api_name) for f in cls._meta.fields]
        return cls(*values)