from pathlib import Path
import enum

APP_NAME = "csti"
BASE_DIR = Path(__file__).parent.parent.parent


class ContestConsts:
	URL = "https://contest.solutions"
	PARSER_TYPE = "html.parser"
	NON_AUTHENTICATED_SESSION_ID = "0000000000000000"
	
	@staticmethod
	def getRequestsUrl() -> str:
		return f"{ContestConsts.URL}/cgi-bin/new-client"


class CliConsts:
	NO_CONTEST_SUPPORT = "Не поддерживаемый контест"


@enum.unique
class Locale(enum.IntEnum):
	english = 0
	russian = 1
	ukrainian = 2
	kazakh = 3
