from src.program import Program
from src.program.utils import normalizeText
from src.consts import Language

if __name__ == "__main__":
	with Program(Language.c, "tests/programs/add.c") as program:
		print(normalizeText(program.run("1 4")))
		print(normalizeText(program.run("5 4")))
