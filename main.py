from src.contest_interface import ContestInterface
from src.consts import Contest, Language


if __name__ == "__main__":
    contest = ContestInterface()
    contest.openContest(Contest.hse_asm_3.value, "", "")

    task = contest.getTask(1)
    print(task.getCondition())