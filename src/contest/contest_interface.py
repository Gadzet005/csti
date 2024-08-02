from abc import ABC, abstractmethod

from requests.models import Response


class ContestInterface(ABC):
	@abstractmethod
	def requestTask(self, taskId: int) -> Response:
		pass
		
	@abstractmethod
	def sendTask(self, taskId: int, file: str) -> Response:
		pass

