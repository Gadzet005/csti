import unittest

from csti.contest.solution import Solution, SolutionStatus
from csti.contest_systems.ejudje.parser import TaskParser

condition = "На вход программе подаётся беззнаковое 32-битное целое число N и натуральное число K  (1 ≤ K ≤ 31).  Требуется циклически сдвинуть биты числа N вправо на K битов и вывести полученное таким образом число.Примечание: в системе команд процессоров семейства x86 для выполнения этой операции есть готовая инструкция — ROR.Запрещается использовать инструкции условной передачи данных и управления."

info = {
    "Ограничение времени": "1 с",
    "Ограничение памяти": "64M",
    "Оставшиеся посылки": "16",
}

tests = [
    ("2 1", "1"),
    ("1 2", "1073741824"),
    ("3 1", "2147483649"),
    ("12 2", "3"),
    ("19 3", "1610612738"),
]

solutions = [None, Solution(777, SolutionStatus.accepted_for_review, 11)]


class TestTaskParser(unittest.TestCase):
    def setUp(self):
        with open("tests/ejudje/parser/html/task_example0.html", "rb") as htmlFile:
            self.html = htmlFile.read()

    def testGetName(self):
        self.assertEqual(TaskParser.getName(self.html), "Задача 02-5: Поворот")

    def testGetCondition(self):
        self.assertEqual(TaskParser.getCondition(self.html), condition)

    def testGetInfo(self):
        self.assertEqual(TaskParser.getInfo(self.html), info)

    def testGetTests(self):
        self.assertEqual(list(TaskParser.getTests(self.html)), tests)

    def testGetLastSolution(self):
        for index in range(0, 2):
            with open(
                f"tests/ejudje/parser/html/task_example{index}.html", "rb"
            ) as htmlFile:
                self.assertEqual(
                    TaskParser.getLastSolution(htmlFile.read()), solutions[index]
                )