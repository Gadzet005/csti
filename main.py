from src.contest import Contest

if __name__ == "__main__":
	contest = Contest(1752)
	contest.selectTask(int(input()))
	print(contest.task.status)
