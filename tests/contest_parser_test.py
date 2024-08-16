import unittest

import requests

from src.consts import ContestConsts
from src.contest.contest_interface import ContestInterface
from src.contest.parser.contest_parser import ContestParser


class TestContestParser(unittest.TestCase):
	def testGetSessionId(self):
		response = requests.post(ContestConsts.getRequestsUrl())
		self.assertEqual(
			ContestParser.getSessionId(response.content),
			ContestConsts.NON_AUTHENTICATED_SESSION_ID
		)
	
	def testGetAviableHwCount(self):
		self.assertTrue(0 <= ContestInterface().getAviableHomeworkCount())
