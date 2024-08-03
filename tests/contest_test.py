import unittest

from src.contest import Contest
from src.contest.parser import ContestParser


# TODO: Крайне нестабильно и тестировать только при рабочем config.
class TestContest(unittest.TestCase):
	def testAll(self):
		count = ContestParser.getAviableHwCount()
		for index in range(1, count):
			homework = ContestParser.getHomework(index)
			absoluteIndex = homework[0]
			if absoluteIndex == -1:
				continue
			# TODO: Молимся что третья задача(самая наибольшая нормальная)
			maxTaskIndex = int(homework[1][2])
			contest = Contest(absoluteIndex)
			for jndex in range(1, maxTaskIndex + 1):
				contest.selectTask(jndex)
				task = contest.task
				task.getInfo()
				task.getName()
				task.getCondition()
				task.getTests()
				task.getStatus()

