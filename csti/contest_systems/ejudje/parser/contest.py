import re

from bs4 import BeautifulSoup

from csti.contest.exceptions import CantParseElement


class ContestParser(object):
    TYPE = "html.parser"

    @staticmethod
    def getSessionId(html: bytes) -> str:
        soup = BeautifulSoup(html, ContestParser.TYPE)
        script = soup.find("script", string=re.compile("var SID="))
        if script is None:
            raise CantParseElement("script")

        sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)
        if len(sessionIdMatches) != 1:
            raise CantParseElement("session id")

        return sessionIdMatches[0]

    @staticmethod
    def getContestInfo(html: bytes, name: str, contestLocalId: int) -> dict | None:
        """
        Возвращает информацию о контесте:
        - "contestGlobalId": int,
        - "taskIds": list[int]
        Возвращает None, если не парсинг не удался.
        """

        soup = BeautifulSoup(html, ContestParser.TYPE)
        tabcontent = soup.find("div", id=f"block_hw{contestLocalId}")
        if tabcontent is None:
            return

        contestButton = tabcontent.find("a", class_="button")
        if contestButton is None:
            return

        contestIdMatches = re.findall(r"Контест (\d{4})", contestButton.text)
        if contestIdMatches is not None and len(contestIdMatches) == 1:
            contestId = int(contestIdMatches[0])
        else:
            return

        homeworksMathes = tabcontent.find_all("td", string=re.compile(name))
        if homeworksMathes is None or len(homeworksMathes) != 1:
            return

        tasks = list()
        for taskId in homeworksMathes[0].parent.find_all(string=re.compile(r"\d")):
            if taskId.startswith("R"):
                # Reversed задачи имеют id 100 + их локальный id (без R)
                tasks.append(int(taskId[1:]) + 100)
            else:
                tasks.append(int(taskId))

        return {
            "contestGlobalId": contestId,
            "taskIds": tasks,
        }

    @staticmethod
    def getContestLocalIds(html: bytes) -> list[int]:
        soup = BeautifulSoup(html, ContestParser.TYPE)
        nav = soup.find("nav")
        if nav is None:
            raise CantParseElement("nav")

        hwContestButtons = list(map(int, re.findall(r"\d+", nav.text)))
        if hwContestButtons is None:
            raise CantParseElement("hwContestButtons")

        return hwContestButtons
