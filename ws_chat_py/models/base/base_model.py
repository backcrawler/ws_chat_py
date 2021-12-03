from abc import ABC


class BaseModel(ABC):
    def __init__(self, field_name_to_value: dict):
        self._field_name_to_value = field_name_to_value

    def _get_field(self, name):
        return self._field_name_to_value.get(name)

    def _set_field(self, name, value):
        if self._field_name_to_value[name] != value:
            self._field_name_to_value[name] = value

            if isinstance(value, BaseModel):
                value._set_parent(self)

    def _set_parent(self, parent):
        pass
