from csti.cli.utils.print import Printer
from csti.program_view.test_result import TestResultList, TestStatus


def printTestResults(testResults: TestResultList, printer: Printer):
    """Выводит результаты тестирования программы"""

    printer.byFlag(
        f"Пройдено тестов: {testResults.passed} из {testResults.total}.",
        flag=testResults.arePassedAll,
    )

    for idx, testResult in enumerate(testResults, 1):
        printer.byFlag(
            f"[{idx}/{testResults.total}] {testResult.status.value}",
            flag=testResult.status == TestStatus.ok,
        )

        match testResult.status:
            case TestStatus.wrongAnswer:
                printer.info("Входные данные:")
                printer.text(testResult.input)
                printer.info("Вывод:")
                printer.text(testResult.output)
                printer.info("Ожидаемый результат:")
                printer.text(testResult.expected)
            case TestStatus.runtimeError:
                printer.info("Входные данные:")
                printer.text(testResult.input)
                printer.info("Ошибка:")
                printer.text(testResult.message)
            case TestStatus.timeLimit:
                printer.info("Входные данные:")
                printer.text(testResult.input)
                printer.error("Превышено время выполнения.")
            case TestStatus.memoryLimit:
                printer.info("Входные данные:")
                printer.text(testResult.input)
                printer.error("Превышено лимит памяти.")
            case _:
                pass
