from bs4 import BeautifulSoup
import re
import requests

from .contest_interface import ContestInterface
from .task import Task

from src.consts import BASE_URL, DEFAULT_LOCALE, NO_AUTH_SID, \
	DEFAULT_REQUESTS_URL
from src.exceptions import AuthException, ContestException, \
	ParserException, IllegalStateException

login = "2310110"
password = "qwe123asd"
solutionLangId = "50"



class Contest(ContestInterface):
	def __init__(self, id_: int):
		# TODO: Сделать из id свойство. 
		self._id: int = id_ 
		self._sessionId: str = NO_AUTH_SID
		self._session: requests.Session|None = None
		self._startSession()

		self.task = Task(self, 1)


	def _startSession(self) -> None:
		if self._session:
			raise ContestException("Сессия уже проинициализирована.")
	
		print(1)
		self._session = requests.Session();
		response = self._session.post(
			f"{BASE_URL}/cgi-bin/new-client",
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"contest_id": self._id,
				"login": login,
				"password": password,
				"locale_id": DEFAULT_LOCALE
			}
		)
		
		print(2)
		soup = BeautifulSoup(response.content, "html.parser")
		script = soup.find("script", string=re.compile("var SID="))
		if script is None:
			raise ParserException("Ошибка при парсинге SID.") # TODO: Убрать повторения.
		
		sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)

		if len(sessionIdMatches) != 1:
			raise ParserException("Ошибка при парсинге SID.")
		
		sessionId = sessionIdMatches[0]
		
		if sessionId == NO_AUTH_SID:
			raise AuthException("В доступе к контесту отказано. \
				Проверьте номер контеста, лоигин и пароль.")

		self._sessionId = sessionId

	@property
	def getSession(self) -> requests.Session:
		if self._session is None:
			raise ContestException("Сессия не проинициализирована.")
		return self._session

	# -----------ContestInterface-----------
	def requestTask(self, taskId: int) -> requests.Response:
		return self.getSession.get(
			DEFAULT_REQUESTS_URL,
			params = {
				"SID": self._sessionId,
				"action": 139, # TODO: добавить enum.
				"prob_id": taskId
			}
		)

	def sendTask(self, taskId: int, file: str) -> requests.Response:
		return self.getSession.post(
			DEFAULT_REQUESTS_URL,
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"SID": self._sessionId,
				"prob_id": taskId,
				"lang_id": solutionLangId,
				"file": file,
				"action_40": ""
			}
		)

