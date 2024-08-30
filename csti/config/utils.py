from typing import Callable

def configField(
	name: str,
	nestedIn: list|None = None,
	serializer: Callable = lambda x: x,
	deserializer: Callable = lambda x: x
):
	""" 
	Добавляет getter и setter для поля из конфига.
	@param name: Имя поля в конфиге (в .yaml файле).
	@param nestedIn: Список полей в которые данное поле вложено. \
        Например, для user.info.login: nestedIn = [user, info].
	@param serializer: Функция преобразования примитивного типа в объект.
    @param deserializer: Функция преобразования объекта обратно в примитивный тип.
	"""

	raw = name.split("-")
	for i in range(1, len(raw)):
		raw[i] = raw[i].capitalize()
	attrName = "".join(raw)

	@property
	def attr(self):
		return serializer(self.get(name, nestedIn))
	
	@attr.setter
	def attr(self, value):
		self.set(name, deserializer(value), nestedIn)

	def decorator(cls):
		setattr(cls, attrName, attr)
		return cls

	return decorator
