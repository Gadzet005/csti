import time

from src.contest import Contest

if __name__ == "__main__":
	for i in range(1752, 1753):
		contest = Contest(1753)
		contest.selectTask(1)
		for j in range(2):
			t0 = time.time()
			contest.task.getName()
			contest.task.getCondition()
			contest.task.getTests()
			t1 = time.time()
			print(t1 - t0)
