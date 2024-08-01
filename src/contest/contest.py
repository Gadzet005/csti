import requests

from .contest_interface import ContestInterface
from .parser import Parser
from .task import Task

from src.consts import DEFAULT_LOCALE, NO_AUTH_SID, \
	DEFAULT_REQUESTS_URL
from src.exceptions import AuthException, ContestException

solutionLangId = "50"


class Contest(ContestInterface):
	def __init__(self, id_: int):
		# TODO: Сделать из id свойство. 
		self._id: int = id_ 
		self._sessionId: str = NO_AUTH_SID
		self._session: requests.Session|None = None
		
		self._startSession()

		self._task: Task|None = None

	def _startSession(self) -> None:
		if self._session:
			raise ContestException("Сессия уже проинициализирована.")
		
		self._session = requests.Session();
		response = self._session.post(
			DEFAULT_REQUESTS_URL,
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
		
		sessionId = Parser.getSessionId(response.content)
		
		if sessionId == NO_AUTH_SID:
			raise AuthException("В доступе к контесту отказано. \
				Проверьте номер контеста, лоигин и пароль.")

		self._sessionId = sessionId

	@property
	def _getSession(self) -> requests.Session:
		if self._session is None:
			raise ContestException("Сессия не проинициализирована.")
		return self._session

	def selectTask(self, taskId: int):
		if taskId <= 0:
			raise ContestException("TaskID меньше нуля")
		self._task = Task(self, taskId)

	@property
	def getTask(self) -> Task|None:
		return self._task

	# -----------ContestInterface-----------
	def requestTask(self, taskId: int) -> requests.Response:
		return self._getSession.get(
			DEFAULT_REQUESTS_URL,
			params = {
				"SID": self._sessionId,
				"action": 139, # TODO: добавить enum.
				"prob_id": taskId
			}
		)

	def sendTask(self, taskId: int, file: str) -> requests.Response:
		return self._getSession.post(
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

