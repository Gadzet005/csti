import os
import shutil

import yaml
from platformdirs import user_config_dir

from src.consts import APP_NAME, Language, Locale
from src.utils import Singleton

# LANG_ID = Language.asm



appConfigDir = user_config_dir(APP_NAME)
configPath = f"{appConfigDir}/config.yaml"
configTemplateDir = "src/config/config_template"


def generateConfig():
	"""
	Генерация конфигурационного файла из шаблона.
	"""
	shutil.copytree(configTemplateDir, appConfigDir)


class ConfigManager(metaclass=Singleton):
	def __init__(self):
		isConfigExist = os.path.exists(configPath)
		if isConfigExist == False:
			generateConfig()

		with open(configPath, "r") as file:
			config = yaml.safe_load(file)

		self._login: str = config["user"]["login"]
		self._password: str = config["user"]["password"]
		self._locale: Locale = Locale[config["locale"]]
		
		self._name: str = config["user"]["name"]
		self._homeUrl: str = config["home-url"]

	@property
	def login(self) -> str:
		return self._login

	@property
	def password(self) -> str:
		return self._password

	@property
	def name(self) -> str:
		return self._name

	@property
	def homeUrl(self) -> str:
		return self._homeUrl

	@property
	def locale(self) -> Locale:
		return self._locale
