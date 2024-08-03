from src.contest.contest import Contest
from src.contest.parser.contest_parser import ContestParser

if __name__ == "__main__":
	
	for i in range(1, ContestParser.getAviableHwCount() + 1):
		print(ContestParser.getHomework(i))
