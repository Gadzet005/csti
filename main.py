from src.ContestInterface import ContestInterface
from src.consts import ASM_LANG_ID, HSE_ASM_CONTEST_3_ID


def main():
    contestInterface = ContestInterface(HSE_ASM_CONTEST_3_ID, "username", "password")
    taskText = contestInterface.getTask(1)
    print(taskText)


if __name__ == "__main__":
    main()