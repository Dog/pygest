from .models import Model
from .manager import Manager
from .fields import Field, DateField

__all__ = [
    "Model",
    "Manager",
    "Field",
    "DateField"
]

__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "pygest")