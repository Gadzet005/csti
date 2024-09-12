from csti.cli.print import cprint
from csti.program_view.test_result import TestStatus, TestResultList


def printTestResults(testResults: TestResultList):
    """ Выводит результаты тестирования программы """

    cprint.byFlag(
        f"Пройдено тестов: {testResults.passed} из {testResults.total}.", 
        flag=testResults.arePassedAll
    )

    for idx, testResult in enumerate(testResults, 1):
        cprint.byFlag(
            f"[{idx}/{testResults.total}] {testResult.status.value}",
            flag=testResult.status == TestStatus.ok
        )

        match testResult.status:
            case TestStatus.wrongAnswer:
                cprint.info("Входные данные:")
                cprint.text(testResult.input)
                cprint.info("Вывод:")
                cprint.text(testResult.output)
                cprint.info("Ожидаемый результат:")
                cprint.text(testResult.expected)
            case TestStatus.runtimeError:
                cprint.info("Входные данные:")
                cprint.text(testResult.input)
                cprint.info("Ошибка:")
                cprint.text(testResult.message)
            case TestStatus.timeLimit:
                cprint.info("Входные данные:")
                cprint.text(testResult.input)
                cprint.error("Превышено время выполнения.")
            case TestStatus.memoryLimit:
                cprint.info("Входные данные:")
                cprint.text(testResult.input)
                cprint.error("Превышено лимит памяти.")
            case _:
                pass
