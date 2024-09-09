import unittest

import requests

from csti.etc.settings import ContestConsts
from csti.contest.contest_interface import ContestInterface
from csti.contest.parser.contest_parser import ContestParser


class TestContestParser(unittest.TestCase):
    def testGetSessionId(self):
        response = requests.post(ContestConsts.getRequestsUrl())
        self.assertEqual(
            ContestParser.getSessionId(response.content),
            ContestConsts.NON_AUTHENTICATED_SESSION_ID
        )
