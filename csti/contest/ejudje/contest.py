from csti.contest.contest import Contest

class EjudjeContest(Contest):
    @property
    def isValid(self) -> bool:
        return self.info["other"]["isValid"]

    @property
    def globalId(self) -> int:
        return self.info["other"]["globalId"]
