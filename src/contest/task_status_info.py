from dataclasses import dataclass

from src.consts import TaskStatus

@dataclass
class TaskStatusInfo:
	solutionId: int
	status: TaskStatus
	testsPassed: int

