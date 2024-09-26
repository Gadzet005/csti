import unittest

import requests

from csti.contest.systems.contest_solutions.api import ContestSolutionsAPI
from csti.contest.systems.contest_solutions.parser import ContestParser


class TestContestParser(unittest.TestCase):
    def testGetSessionId(self):
        response = requests.post(ContestSolutionsAPI.REQUEST_URL)
        self.assertEqual(
            ContestParser.getSessionId(response.content),
            ContestSolutionsAPI.BAD_SESSION_ID,
        )
