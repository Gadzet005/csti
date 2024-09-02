from typing import Callable, Type, Any

def configField(
	name: str,
	type: Type,
	nestedIn: list|None = None,
	defaultValue: Any = None,
	serializer: Callable = lambda x: x,
	deserializer: Callable = lambda x: x
):
	""" 
	Добавляет getter и setter для поля из конфига.\n
	@param name: Имя поля в конфиге (в .yaml файле).
	@param type: Тип поля в конфиге.
	@param nestedIn: Список полей в которые данное поле вложено. \
		Например, для user.info.login: nestedIn = [user, info].
	@param defaultValue: Значение поля по умолчанию.
	@param serializer: Функция преобразования примитивного типа в объект.
	@param deserializer: Функция преобразования объекта обратно в примитивный тип.
	"""

	raw = name.split("-")
	for i in range(1, len(raw)):
		raw[i] = raw[i].capitalize()
	attrName = "".join(raw)

	@property
	def attr(self):
		raw = self.get(name, nestedIn, defaultValue)
		return serializer(type(raw))
	
	@attr.setter
	def attr(self, value):
		self.set(name, type(deserializer(value)), nestedIn)

	def decorator(cls):
		setattr(cls, attrName, attr)
		return cls

	return decorator
