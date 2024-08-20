import requests

from config import ConfigManager
from consts import ContestConsts
from contest.exceptions import AuthException, ContestInterfaceException
from contest.parser.contest_parser import ContestParser
from contest.task.solution import SolutionStatus
from utils import Singleton


class ContestInterface(metaclass=Singleton):
	def signIn(self, login: str, password: str):
		self._login: str = login
		self._password: str = password

		self._contestId: str|None = None
		self._sessionId: str|None = None
		self._cookieSessionId: str|None = None

		"""
		Переменная для кэширования сессии, не использовать!
		Вместо этого можно использовать Self.session
		"""
		self._session: requests.Session|None = None

	@property
	def session(self) -> requests.Session|None:
		if self._cookieSessionId is None:
			return None
		if self._session is None:
			self._session = requests.Session()
			self._session.cookies.set("EJSID", self._cookieSessionId)
		return self._session
	
	def selectContest(self, id: str):
		if self._login is None or self._password is None:
			raise AuthException("Логин или пароль не проинициализирован.")

		response = requests.post(
			ContestConsts.getRequestsUrl(),
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"contest_id": id,
				"login": self._login,
				"password": self._password,
				"locale_id": ConfigManager().locale.value
			}
		)
		
		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""
		
		sessionId = ContestParser.getSessionId(response.content)
		if sessionId == ContestConsts.NON_AUTHENTICATED_SESSION_ID:
			raise AuthException(
				"В доступе к контесту отказано. "
				"Проверьте номер контеста, логин и пароль."
			)
		
		self._contestId = id
		self._sessionId = sessionId
		self._cookieSessionId = response.cookies.get("EJSID")

	# --------------------- Homework -------------------
	def requestHome(self) -> bytes:
		response = requests.get(ConfigManager().homeUrl)

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""

		return response.content

	def getAvailableHomeworksLocalId(self) -> list[int]:
		homeHtml = self.requestHome()
		homeworksLocalId = ContestParser.getAvailableHomeworksLocalId(homeHtml)
		return homeworksLocalId

	def getHomework(self, namePattern: str, localContestId: int) -> tuple[str, list[tuple[str, SolutionStatus]]]:
		homeHtml = self.requestHome()
		homework = ContestParser.getHomework(homeHtml, namePattern, localContestId)
		return homework

	# --------------------- Task -----------------------
	@property
	def langId(self):
		if self._contestId == None:
			raise ContestInterfaceException("ContestId не инициализирован.")
		return f"{self._contestId[2]}0"

	def requestTask(self, taskId: str) -> bytes:
		if self.session is None:
			raise ContestInterfaceException("Сессия не инициализирована.")

		response = self.session.get(
			ContestConsts.getRequestsUrl(),
			params = {
				"SID": self._sessionId,
				"action": 139, # TODO: добавить enum.
				"prob_id": taskId
			}
		)

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""

		return response.content

	def sendTask(self, taskId: str, file: str):
		if self.session == None:
			raise ContestInterfaceException("Сессия не инициализирована.")

		response = self.session.post(
			ContestConsts.getRequestsUrl(),
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"SID": self._sessionId,
				"prob_id": taskId,
				"lang_id": self.langId,
				"file": file,
				"action_40": ""
			}
		)

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""

		return response
