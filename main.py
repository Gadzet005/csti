from src.contest.contest import Contest

if __name__ == "__main__":
    contest = Contest(1752)
    print(contest.task.getCondition().text)
