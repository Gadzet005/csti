from src.consts import APP_NAME, Language, Locale

LOCALE = Locale.russian.value
LANG_ID = Language.asm


from platformdirs import user_config_dir
from src.utils import Singleton
import yaml
import os


configPath = f"{user_config_dir(APP_NAME)}/config.yaml"

def generateConfig():

	"""
	Генерирует конфигурационный файл.
 
	"""
	os.makedirs(os.path.dirname(configPath), exist_ok=True)
	with open("config_template/config.py") as file:
		if file in os.listdir(user_config_dir(APP_NAME)):
			pass	
	


def getSignInData() -> tuple[str, str]:
	with open(f"{user_config_dir(APP_NAME)}/auth.yaml", "r") as file:
		config = yaml.safe_load(file)
	login = config["login"]
	password = config["password"]

	return (login, password)


class ConfigManager(metaclass=Singleton):
	def __init__(self):
		with open(configPath, "r") as file:
			config = yaml.safe_load(file)
		self.name = config["name"]
		self.homeUrl = config["home-url"]
