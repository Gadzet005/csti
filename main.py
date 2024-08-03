from src.contest.contest import Contest
import time

import requests_cache

requests_cache.install_cache(expire_after=360, allowable_methods=('GET', 'POST'))

if __name__ == "__main__":
	for i in range(1750, 1751):
		contest = Contest(i)
		t0 = time.time()
		for i1 in range(1, 10):
			contest.selectTask(i1)
			contest.task.getName()
			contest.task.getCondition()
			contest.task.getTests()
		
		t1 = time.time()
		print(t1 - t0)
	
	
	
		t2 = time.time()
		for i1 in range(1, 2):
			contest.selectTask(i1)
			print(list(contest.task.getInfo()))
			print(contest.task.getStatus())
		t3 = time.time()
		print(t3 - t2)
	

