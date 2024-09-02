from __future__ import annotations

import os

from csti.contest_env.data_manager import DataManager
from csti.contest import Contest


class ContestEnv:
	def __init__(self, dir: str):
		self._dir = dir
		self._dataManager = DataManager(os.path.join(self.dir, DataManager.FOLDER))

	@staticmethod
	def create(baseDir: str, contest: Contest) -> ContestEnv:
		envDir = os.path.join(baseDir, f"contest-{contest.id}")
		os.makedirs(envDir, exist_ok=True)

		dataManager = DataManager.create(os.path.join(envDir, DataManager.FOLDER))
		dataManager.saveContest(
			contest.id, 
			list(map(lambda x: x.id, contest.tasks)), 
			contest.currentTask.id
		)

		for task in contest.tasks:
			fileName = task.id + contest.lang.fileExtension

			with open(os.path.join(envDir, fileName), "w") as f:
				f.write(contest.lang.comment + " " + task.name + "\n")

		return ContestEnv(envDir)
	
	@staticmethod
	def createInCurrentDir(contest: Contest) -> ContestEnv:
		return ContestEnv.create(os.getcwd(), contest)
	
	@staticmethod
	def inCurrentDir() -> ContestEnv:
		return ContestEnv(os.getcwd())

	@property
	def dir(self) -> str:
		return self._dir

	@property
	def dataManager(self) -> DataManager:
		return self._dataManager
