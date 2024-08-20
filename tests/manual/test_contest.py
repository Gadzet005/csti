import os
import unittest

from csti.config import ConfigManager
from csti.contest.contest import Contest
from csti.contest.contest_interface import ContestInterface


# NOTE: Тестировать только при рабочем config.
class TestContest(unittest.TestCase):
	def testAll(self):
		ContestInterface().signIn(ConfigManager().login, ConfigManager().password)
		isSkipNext = False

		homeworksLocalId = ContestInterface().getAvailableHomeworksLocalId()
		for localId in homeworksLocalId:
			homework = ContestInterface().getHomework(ConfigManager().name, localId)
			id = homework[0]
			if id == "-1":
				continue

			tasksId = list(range(1, 13))
			contest = Contest(id, [ str(taskId) for taskId in tasksId])
			for taskLocalId in range(1, len(tasksId) + 1):
				contest.selectTask(taskLocalId)
				task = contest.currentTask
				print(task.getName())
				print(list(task.getInfo()))
				print(task.getCondition())
				print(task.getSolution())
				print(list(task.getTests()))
				if isSkipNext == False:
					input_ = input("Skip next ask: yes/no(default): ")
					if input_ == "yes" or input_ == "y":
						isSkipNext = True
					
				os.system("clear")