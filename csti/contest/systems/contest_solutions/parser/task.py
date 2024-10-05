import typing as t
from inspect import cleandoc

from bs4 import BeautifulSoup

from csti.contest.solution import Solution, SolutionStatus


class TaskParser(object):
    PARSER_TYPE = "html.parser"
    TestCase: t.TypeAlias = tuple[str, str]
    TestCases: t.TypeAlias = list[TestCase]

    @staticmethod
    def getName(html: bytes) -> t.Optional[str]:
        soup = BeautifulSoup(html, TaskParser.PARSER_TYPE)
        nameElement = soup.find("h3")
        if nameElement is None:
            return

        return nameElement.text

    @staticmethod
    def getInfo(html: bytes) -> t.Optional[dict[str, str]]:
        soup = BeautifulSoup(html, TaskParser.PARSER_TYPE)
        infoContainer = soup.find("table", class_="line-table-wb")
        if infoContainer is None:
            return

        infoStrings = cleandoc(infoContainer.text).split("\n")
        info = {}
        for infoString in infoStrings:
            key, value = infoString.split(":", 1)
            info[key.strip()] = value.strip()

        return info

    @staticmethod
    def getCondition(html: bytes) -> t.Optional[str]:
        soup = BeautifulSoup(html, TaskParser.PARSER_TYPE)
        taskContainer = soup.find("div", id="probNavTaskArea-ins")
        if taskContainer is None:
            return

        conditionElements = taskContainer.find_all("p", recursive=False)  # type: ignore
        if conditionElements is None:
            return

        # TODO: Испривать форматирование(также перевод в текст сейчас 10^9 = 109 = 10_9)
        condition = "".join(
            map(
                lambda element: cleandoc(element.text).replace("\n", " "),
                conditionElements,
            )
        )

        return cleandoc(condition)

    @staticmethod
    def getTests(html: bytes) -> t.Optional[TestCases]:
        soup = BeautifulSoup(html, TaskParser.PARSER_TYPE)
        testsElements = soup.find_all("pre")
        if testsElements is None:
            return

        testsUnparse = map(lambda testElement: testElement.text, testsElements)
        testsIterator = iter(testsUnparse)

        return list(zip(testsIterator, testsIterator))

    @staticmethod
    def getLastSolution(html: bytes) -> t.Optional[Solution]:
        soup = BeautifulSoup(html, TaskParser.PARSER_TYPE)
        statusTable = soup.find("table", class_="table")
        if statusTable is None:
            return

        statusHistoryLine = statusTable.find_all("tr")  # type: ignore
        if statusHistoryLine is None:
            return

        # Не учитываем строку с информацией о колоннах
        statusBlocks = statusHistoryLine[1].find_all("td", class_="b1")
        if statusBlocks is None:
            return

        testPassedElement = statusBlocks[5].text

        return Solution(
            int(statusBlocks[0].text),
            SolutionStatus(statusBlocks[4].text),
            int(testPassedElement if testPassedElement.isdigit() else 0),
        )
