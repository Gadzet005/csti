import os
import shutil

import yaml
from platformdirs import user_config_dir

from csti.consts import APP_NAME, Locale
from csti.utils import Singleton

from csti.config.utils import configField


appConfigDir = user_config_dir(APP_NAME)
globalConfigPath = f"{appConfigDir}/config.yaml"
configTemplateDir = "csti/config/config_template"


@configField(name="login", nestedIn=["user"])
@configField(name="password", nestedIn=["user"])
@configField(name="name", nestedIn=["user"])
@configField(name="home-url")
@configField(
	name="locale",
	serializer=lambda x: Locale[x],
	deserializer=lambda x: x.name
)
@configField(name="enable-auto-tests", nestedIn=["features"])
@configField(name="enable-auto-formatting", nestedIn=["features"])
class GlobalConfig(metaclass=Singleton):
	def __init__(self):
		self._data: dict = {}

		if not os.path.exists(globalConfigPath):
			self.createDefaultConfig()
		self.load()

	@staticmethod
	def createDefaultConfig():
		""" Генерация конфигурационного файла из шаблона. """
		shutil.copytree(configTemplateDir, appConfigDir)

	def load(self):
		with open(globalConfigPath, "r") as file:
			self._data = yaml.safe_load(file)

	def save(self):
		with open(globalConfigPath, "w") as file:
			yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)

	def _pull(self, key: str, nestedIn: list|None):
		if nestedIn is None:
			nestedIn = []

		data = self._data
		for name in nestedIn:
			data = data.get(name)
			if data is None:
				break
		
		if data is None or key not in data:
			field = ".".join(nestedIn + [key])
			raise KeyError(f"Поле {field} не найдено в глобальном конфиге")
		
		return data

	def get(self, key: str, nestedIn: list|None = None):
		""" 
		Получение значения поля в конфиге.
		@param key: Имя поля в конфиге.
        @param nestedIn: Список полей в которые данное поле вложено. \
			Например для user.info.login: nestedIn = [user, info].
		"""
		data = self._pull(key, nestedIn)
		return data[key]

	def set(self, key: str, value, nestedIn: list|None = None):
		""" Выставление значения поля в конфиге. Работает по аналогии с get. """

		data = self._pull(key, nestedIn)
		data[key] = value
