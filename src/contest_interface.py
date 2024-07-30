import re
import requests
from bs4 import BeautifulSoup

from .consts import BASE_URL, DEFAULT_LOCALE
from .exceptions import AuthException, ParserException, IllegalStateException

class Task:
	def __init__(self, _id, contestInterface):
		self._id: int = _id
		self._contestInterface: ContestInterface = contestInterface
	
	def getCondition(self):
		response = self._contestInterface.get(
			f"{BASE_URL}/cgi-bin/new-client",
			params={
				"SID": self._contestInterface.sessionId,
				"action": 139,
				"prob_id": self._id
			}
		)

		return response.text

	def getStatus(self):
		pass

	def submitSolution(self, solutionFilePath, solutionLangId):
		try:
			file = open(solutionFilePath, 'r')
		except OSError:
			raise FileNotFoundError(
				f"Файл '{solutionFilePath}', отправленный в качестве решения задачи №{self._id} не найден"
			)

		response = self._contestInterface.post(
			f"{BASE_URL}/cgi-bin/new-client",
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"SID": self._contestInterface.sessionId,
				"prob_id": self._id,
				"lang_id": solutionLangId,
				"file": file,
				"action_40": ""
			}
		)

		return response.text


class ContestInterface:
	def __init__(self):
		self._currentContestId: int = None
		self._sessionId: int = None
		self._session: requests.Session = None

	@property
	def isValid(self) -> bool:
		return self._currentContestId is not None
	
	@property
	def sessionId(self) -> int:
		return self._sessionId
	
	# Проверка состояния
	def _checkState(self):
		if not self.isValid:
			raise IllegalStateException("Не открыт контест. Требуется вызов метода openContest")


	def openContest(self, contestId, login, password):
		# Закрываем предыдущий контест
		self.closeContest()

		session = requests.Session()
		response = session.post(
			f"{BASE_URL}/cgi-bin/new-client",
			headers={
				"Content-Type": "multipart/form-data",
			},
			data={
				"contest_id": contestId,
				"login": login,
				"password": password,
				"locale_id": DEFAULT_LOCALE
			}
		)

		soup = BeautifulSoup(response.content, "html.parser")
		script = soup.find("script", string=re.compile("var SID="))	
		SIDMatches = re.findall(r'var SID="(\w{16})"', script.text)

		if len(SIDMatches) != 1:
			raise ParserException("Ошибка при парсинге SID")
		
		SID = SIDMatches[0]

		if SID == "0000000000000000":
			raise AuthException("В доступе к контесту отказано. Проверьте логин и пароль")
		
		# Успешный доступ к контесту
		self._session = session
		self._sessionId = SID
		self._currentContestId = contestId

	def closeContest(self):
		self._currentContestId = None
		self._sessionId = None
		if self._session:
			self._session.close()
		self._session = None
	

	def getTask(self, taskId):
		self._checkState()
		return Task(taskId, self)
	

	# Выволнение запроса в текущей сессии
	def makeRequest(self, *ars, **kwargs):
		self._checkState()
		return self._session.request(*ars, **kwargs)

	def get(self, *args, **kwargs):
		return self.makeRequest("GET", *args, **kwargs)
	
	def post(self, *args, **kwargs):
		return self.makeRequest("POST", *args, **kwargs)