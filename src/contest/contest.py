import requests

from config import LANG_ID, LOCALE, login, password
from src.consts import ContestConsts
from src.contest.contest_interface import ContestInterface
from src.contest.exceptions import AuthException, ContestException
from src.contest.parser.contest_parser import ContestParser
from src.contest.task.task import Task


class Contest(ContestInterface):
	def __init__(self, id_: int):
		self._id: int = id_ 
		self._sessionId: str = ContestConsts.NON_AUTHENTICATED_SESSION_ID
		self._session: requests.Session|None = None
		
		self._startSession()

		self._task: Task|None = None

	def _startSession(self) -> None:
		if self._session:
			raise ContestException("Сессия уже проинициализирована.")
		
		self._session = requests.Session();
		response = self._session.post(
			ContestConsts.getRequestsUrl(),
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"contest_id": self._id,
				"login": login,
				"password": password,
				"locale_id": LOCALE
			}
		)
		
		sessionId = ContestParser.getSessionId(response.content)
		
		if sessionId == ContestConsts.NON_AUTHENTICATED_SESSION_ID:
			raise AuthException("В доступе к контесту отказано. \
				Проверьте номер контеста, лоигин и пароль.")

		self._sessionId = sessionId

	@property
	def session(self) -> requests.Session:
		if self._session is None:
			raise ContestException("Сессия не проинициализирована.")
		return self._session

	def selectTask(self, taskId: int):
		if taskId <= 0:
			raise ContestException("TaskID меньше нуля")
		self._task = Task(self, taskId)

	@property
	def task(self) -> Task|None:
		return self._task

	# -----------ContestInterface-----------
	def requestTask(self, taskId: int) -> requests.Response:
		return self.session.get(
			ContestConsts.getRequestsUrl(),
			params = {
				"SID": self._sessionId,
				"action": 139, # TODO: добавить enum.
				"prob_id": taskId
			}
		)

	def sendTask(self, taskId: int, file: str) -> requests.Response:
		return self.session.post(
			ContestConsts.getRequestsUrl(),
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"SID": self._sessionId,
				"prob_id": taskId,
				"lang_id": LANG_ID.value,
				"file": file,
				"action_40": ""
			}
		)

