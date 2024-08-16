from src.consts import APP_NAME, Language, Locale

LOCALE = Locale.russian.value
LANG_ID = Language.asm


from platformdirs import user_config_dir
from src.utils import Singleton
import yaml


def getSignInData() -> tuple[str, str]:
	with open(f"{user_config_dir(APP_NAME)}/auth.yaml", "r") as file:
		config = yaml.safe_load(file)
	login = config["login"]
	password = config["password"]

	return (login, password)


class ConfigManager(metaclass=Singleton):
	def __init__(self):
		with open(f"{user_config_dir(APP_NAME)}/config.yaml", "r") as file:
			config = yaml.safe_load(file)
		self.name = config["name"]
		self.homeUrl = config["home-url"]
