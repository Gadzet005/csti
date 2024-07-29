import requests
from .consts import CONTEST_SOLUTIONS_BASE_URL, DEFAULT_LANG_ID

"""
Объект для взаимодействия с сайтом контеста
"""
class ContestInterface:
    def __init__(self, contestId, username, password):
        self.contestId = contestId
        self.username = username
        self.session, self.SID = ContestInterface.createSession(contestId, username, password)
    
    # Возвращает сессию и SID для указанного контеста и пользователя
    @staticmethod
    def createSession(contestId, username, password):
        session = requests.Session()
        response = session.post(
            f"{CONTEST_SOLUTIONS_BASE_URL}/cgi-bin/new-client",
            headers={
                "Content-Type": "multipart/form-data",
            },
            data={
                "contest_id": contestId,
                "login": username,
                "password": password,
                "locale_id": DEFAULT_LANG_ID
            }
        )

        # TODO: сделать парсинг
        print(response.text[:500])
        SID = input(">>> SID:\n")

        return session, SID
    
    # Возвращает текст задания с указанным ID
    def getTask(self, task_id):
        response = self.session.get(
            f"{CONTEST_SOLUTIONS_BASE_URL}/cgi-bin/new-client",
            params={
                "SID": self.SID,
                "action": 139,
                "prob_id": task_id
            }
        )

        return response.text
    
    # Отправляет решение на проверку
    def submitSolution(self, task_id, solutionFilePath, solutionLangId):
        response = self.session.post(
            f"{CONTEST_SOLUTIONS_BASE_URL}/cgi-bin/new-client",
            headers={
                "Content-Type": "multipart/form-data",
            },
            data={
                "SID": self.SID,
                "prob_id": task_id,
                "lang_id": solutionLangId,
                "file": open(solutionFilePath, 'r'),
                "action_40": ""
            }
        )

        return response.text