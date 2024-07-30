from .contest_interface import ContestInterface


class Task:
	def __init__(self, contestInterface: ContestInterface, id_: int) -> None:
		self._contestInterface: ContestInterface = contestInterface
		self._id: int = id_
	
	def getCondition(self):
		return self._contestInterface.requestTask(self._id)
	
	def getStatus(self):
		pass

	def sendSolution(self, file: str):
		return self._contestInterface.sendTask(self._id, file)

