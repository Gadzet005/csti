import unittest
import os

from app.contest import Contest, ContestInterface
from app.config import login, password

# TODO: Крайне нестабильно и тестировать только при рабочем config.
class TestContest(unittest.TestCase):
	def testAll(self):
		ContestInterface(login, password)
		isSkipNext = False
		for id in range(1750, 1754):
			tasksId = [1, 4, 6, 7, 10]
			contest = Contest(id, tasksId)
			for taskLocalId in range(1, len(tasksId) + 1):
				contest.selectTask(taskLocalId)
				task = contest.getTask()
				print(task.getName())
				print(list(task.getInfo()))
				print(task.getCondition())
				print(task.getStatus())
				print(list(task.getTests()))
				if isSkipNext == False:
					input_ = input("Skip next ask: yes/no(default): ")
					if input_ == "yes":
						isSkipNext = True
					
				os.system("clear")
