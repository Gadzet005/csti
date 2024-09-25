import typing as t
from copy import deepcopy

from csti.storage.exceptions import FieldNotFound
from csti.storage.field import Field
from csti.storage.template_element import TemplateElement


class Group(TemplateElement):
    def __init__(self, name: str = "", members: list[TemplateElement] = list()):
        super().__init__(name)
        self._members = {member.name: member for member in members}

    def get(self, name: str) -> TemplateElement:
        return self._members.get(name)  # type: ignore

    def extend(self, newMembers: list[TemplateElement]):
        for member in newMembers:
            self._members[member.name] = member


class StorageTemplate:
    """Шаблон хранилища."""

    def __init__(self, members: list[TemplateElement]):
        self._rootGroup = Group(members=members)

    def get(self, *location: str) -> tuple[bool, t.Optional[TemplateElement]]:
        cur = self._rootGroup
        for elem in location:
            if not isinstance(cur, Group):
                return False, None
            try:
                cur = cur.get(elem)
            except KeyError:
                return False, None

        return True, cur

    def getField(self, *location: str) -> Field:
        success, result = self.get(*location)
        if not success or not isinstance(result, Field):
            raise FieldNotFound(location)
        return result
    
    def extend(self, newMembers: list[TemplateElement]) -> t.Self:
        """ Расширяет шаблон новыми полями. """
        new = deepcopy(self)
        new._rootGroup.extend(newMembers)
        return new
