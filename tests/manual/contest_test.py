import unittest
import os

from src.contest import Contest, ContestInterface
from src.config import login, password, namePattern

# NOTE: Тестировать только при рабочем config.
class TestContest(unittest.TestCase):
	def testAll(self):
		ContestInterface().signIn(login, password)
		isSkipNext = False

		aviableHomeworkCount = ContestInterface().getAviableHomeworkCount()
		for localId in range(1, aviableHomeworkCount):
			homework = ContestInterface().getHomework(namePattern, localId)
			id = homework[0]
			if id == -1:
				continue

			tasksId = list(range(1, 13))
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
					if input_ == "yes" or input_ == "y":
						isSkipNext = True
					
				os.system("clear")
