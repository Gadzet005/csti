from csti.data_storage.template_member import TemplateMember
from csti.data_storage.field import Field
from csti.data_storage.exceptions import FieldNotFound


class Group(TemplateMember):
	def __init__(self, name: str, members: list[TemplateMember]):
		super().__init__(name)
		self._members = {member.name: member for member in members}

	def get(self, name: str) -> TemplateMember:
		return self._members.get(name)


class StorageTemplate:
	""" Шаблон хранилища. """

	def __init__(self, members: list[TemplateMember]):
		self._rootGroup = Group("", members)

	def getField(self, *location: list[str]) -> Field:
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
