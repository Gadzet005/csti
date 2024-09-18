from csti.data_storage.exceptions import FieldNotFound
from csti.data_storage.field import Field
from csti.data_storage.template_element import TemplateElement


class Group(TemplateElement):
    def __init__(self, name: str, members: list[TemplateElement]):
        super().__init__(name)
        self._members = {member.name: member for member in members}

    def get(self, name: str) -> TemplateElement:
        return self._members.get(name)  # type: ignore


class StorageTemplate:
    """Шаблон хранилища."""

    def __init__(self, members: list[TemplateElement]):
        self._rootGroup = Group("", members)

    def getField(self, *location: str) -> Field:
        cur = self._rootGroup
        for elem in location:
            if not isinstance(cur, Group):
                raise FieldNotFound(location)
            try:
                cur = cur.get(elem)
            except KeyError:
                raise FieldNotFound(location)

        if not isinstance(cur, Field):
            raise FieldNotFound(location)

        return cur
