import requests

from src.config import HOME_URL, LANG_ID, LOCALE
from src.consts import ContestConsts
from src.utils import Singleton

from src.contest.exceptions import AuthException
from src.contest.parser import ContestParser


class ContestInterface(metaclass=Singleton):
	def __init__(self, login: str|None = None, password: str|None = None):
		if login:
			self._login: str = login
		if password:
			self._password: str = password
		
		self._sessionId = None
		self._cookieSessionId = None
		self._session: requests.Session|None = None
	
	def selectContest(self, globalId):
		if self._login is None or self._password is None:
			raise AuthException("Логин или пароль не проинициализирован")

		self._session = requests.Session() # TODO: Перенести в конструктор мб.
		response = self._session.post(
			ContestConsts.getRequestsUrl(),
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"contest_id": globalId,
				"login": self._login,
				"password": self._password,
				"locale_id": LOCALE
			}
		)

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""
		
		sessionId = ContestParser.getSessionId(response.content)
		if sessionId == ContestConsts.NON_AUTHENTICATED_SESSION_ID:
			raise AuthException("В доступе к контесту отказано. \
				Проверьте номер контеста, лоигин и пароль.")

		self._sessionId = sessionId


	# --------------------- Homework -------------------
	def requestHome(self) -> bytes:
		response = requests.get(HOME_URL)

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""

		return response.content

	def getAviableHomeworkCount(self) -> int:
		homeHtml = ContestInterface().requestHome()
		homeworkCount = ContestParser.getAviableHomeworkCount(homeHtml)
		return homeworkCount

	def getHomework(self, namePattern: str, localContestId: int) -> tuple[int, map]:
		homeHtml = ContestInterface().requestHome()
		homework = ContestParser.getHomework(homeHtml, namePattern, localContestId)
		return homework

	# --------------------- Task -----------------------
	def requestTask(self, taskId: int) -> bytes:
		if self._session == None:
			# TODO: Recconect.
			raise Exception()

		response = self._session.get(
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

	def sendTask(self, taskId: int, file: str):
		if self._session == None:
			# TODO: Recconect.
			raise Exception()

		response = self._session.post(
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

		"""
			TODO: Сделать гибкую систему ошибок(особенно проверка на срок 
			годность сессии).
		"""

		return response

