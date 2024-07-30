from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from ctypes import c_uint8
import re
import requests
from requests.models import Response
from requests.sessions import Session

from .consts import BASE_URL, DEFAULT_LOCALE
from .exceptions import AuthException, ContestException, ParserException, IllegalStateException


login = ""
password = ""
solutionLangId = "50"

NO_INIT_SID = "0000000000000000"
DEFAULT_REQUESTS_URL = f"{BASE_URL}/cgi-bin/new-client"


class ContestInterface(ABC):
	@abstractmethod
	def requestTask(self, taskId: c_uint8) -> requests.Response:
		pass
		
	@abstractmethod
	def sendTask(self, taskId: c_uint8, file: str) -> requests.Response:
		pass


class Contest(ContestInterface):
	def __init__(self, id_: c_uint8):
		# TODO: Сделать из id свойство. 
		self._id: c_uint8 = id_
		self._sessionId: str = NO_INIT_SID
		self._session: requests.Session|None = None
		self._startSession()

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
			})
		
		soup = BeautifulSoup(response.content, "html.parser")
		script = soup.find("script", string=re.compile("var SID="))
		
		if script is None:
			raise ParserException("Ошибка при парсинге SID.")
		
		sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)

		if len(sessionIdMatches) != 1:
			raise ParserException("Ошибка при парсинге SID.")
		
		sessionId = sessionIdMatches[0]
		
		if sessionId == NO_INIT_SID:
			raise AuthException("В доступе к контесту отказано. \
				Проверьте лоигин  и пароль.")

		self._sessionId = sessionId

	@property
	def getSession(self) -> requests.Session:
		if self._session is None:
			raise ContestException("Сессия не проинициализирована.")
		return self._session

	# -----------ContestInterface-----------
	def requestTask(self, taskId: c_uint8) -> requests.Response:
		return self.getSession.get(
			DEFAULT_REQUESTS_URL,
			params = {
				"SID": self._sessionId,
				"action": 139, # TODO: добавить enum.
				"prob_id": int(taskId)
			}
		)

	def sendTask(self, taskId: c_uint8, file: str) -> requests.Response:
		return self.getSession.post(
			DEFAULT_REQUESTS_URL,
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"SID": self._sessionId,
				"prob_id": int(taskId),
				"lang_id": solutionLangId,
				"file": file,
				"action_40": ""
			}
		)



class Task:
	def __init__(self, contestInterface: ContestInterface, \
			  id_: c_uint8) -> None:
		self._ownerInterface = contestInterface
		self._id = id_
	
	def getCondition(self):
		return self._ownerInterface.requestTask(self._id)
	
	def getStatus(self):
		pass

	def sendSolution(self, file: str):
		return self._ownerInterface.sendTask(self._id, file)

