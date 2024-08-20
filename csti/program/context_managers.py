from csti.program.program import Program


class prepareProgram:
	"""
    Контекстный менеджер подготовки программы для запуска (компиляция, если требуется).
    Очищает временные файлы при выходе.

    with prepareProgram(program) as prepared:
		...
	"""

	def __init__(self, program: Program):
		self._program = program

	def __enter__(self) -> Program:
		if self._program.canBeCompiled:
			self._program.compile()
		return self._program
	
	def __exit__(self, *args):
		self._program.clear()


class formatProgram:
	"""
	Контекстный менеджер форматирования программы.
	Очищает отформатированный файл при выходе.

	with formatProgram(program) as formatted:
		...
	"""

	def __init__(self, program: Program):
		self._origin: Program = program
		self._formatted: Program|None = None
	
	def __enter__(self) -> Program:
		if self._origin.canBeFormatted:
			self._formatted = self._origin.format()
			return self._formatted
		return self._origin
	
	def __exit__(self, *args):
		if self._formatted:
			self._formatted.clear(clearSelf=True)
