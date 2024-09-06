from __future__ import annotations

import abc
from typing import Any, overload

from csti.data_storage.template import StorageTemplate
from csti.data_storage.exceptions import FieldNotInitialized


class DataStorage(abc.ABC):
	"""	Интерфейс хранилища данных. """
	
	template: StorageTemplate = StorageTemplate([])
	
	@staticmethod
	def init(*args, **kwargs) -> DataStorage:
		""" Инициализация хранилища (создание файлов, папок и т.д.). """
		return DataStorage()

	@abc.abstractmethod
	def _get(self, location: list[str]) -> Any:
		""" 
		Получение значения без какой-либо обработки. 
		Ошибка FieldNotInitialized, если значение не найдено.
		"""
		pass

	@abc.abstractmethod
	def _set(self, location: list[str], value: Any):
		""" Выставление значения без какой-либо обработки. """
		pass
	

	@overload
	def get(self, *location: list[str]) -> Any:
		"""
		Получить значение из хранилища.\n
		@param location: \
		 	Список названий полей, в которые данное поле вложено и название самого поля. \
			Например, для user.info.name location=[user, info, name].
		"""
		pass

	@overload
	def get(self, *location: list[str], default=None) -> Any:
		""" 
		Получить значение из хранилища.\n
		@param location: \
		 	Список названий полей, в которые данное поле вложено и название самого поля. \
			Например, для user.info.name location=[user, info, name].
		@param default: \
			Значение, которое будет возвращено, если поле не найдено и \
			не установлено базовое значение по умолчанию.
		"""
		pass

	def get(self, *location: list[str], **kwargs) -> Any:
		field = self.template.getField(*location)

		try:
			rawValue = self._get(location)
			return field.deserialize(rawValue)
		except FieldNotInitialized as error:
			if field.defaultValue is not None:
				return field.defaultValue
			elif "default" in kwargs:
				default = kwargs.pop("default")
				return default
			else:
				raise error


	def contains(self, *location: list[str]) -> bool:
		""" Наличие значения в поле. """
		try:
			self._get(*location)
			return True
		except FieldNotInitialized:
			return False
	
	def set(self, *location: list[str], value: Any):
		""" 
		@param location: \
		 	Список названий полей, в которые данное поле вложено и название самого поля. \
			Например, для user.info.name location=[user, info, name].
		"""

		field = self.template.getField(*location)
		self._set(location, field.serialize(value))


class SaveLoadStorage(DataStorage):
	""" 
	Интерфейс хранилища, которое не предполагает 
	автоматического сохранения при вызове метода set.
	"""

	def __init__(self):
		super().__init__()
		self.data = None
	
	@abc.abstractmethod
	def save(self):
		pass
	
	@abc.abstractmethod
	def load(self):
		pass
