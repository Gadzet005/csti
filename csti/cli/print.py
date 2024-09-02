from typing import Callable

from termcolor import colored


class Colors:
	text = 		lambda x, no_color=False: x
	success = 	lambda x, no_color=False: colored(x, "green", no_color=no_color)
	error = 	lambda x, no_color=False: colored(x, "red", no_color=no_color)
	warning = 	lambda x, no_color=False: colored(x, "yellow", no_color=no_color)
	primary = 	lambda x, no_color=False: colored(x, "blue", no_color=no_color)
	info = 		lambda x, no_color=False: colored(x, "cyan", no_color=no_color)
	debug = 	lambda x, no_color=False: colored(x, "magenta", attrs=["bold"], no_color=no_color)

	@staticmethod
	def makeColored(
		values: list[str], 
		colorBy = Callable[[str, bool], str], 
		no_color: bool = False
	) -> list[str]:
		""" Перекрашивает список строк """
		return list(map(lambda x: colorBy(x, no_color), values))


class Printer:
	""" Класс для цветного вывода в терминал """

	def __init__(self, noColor: bool = False):
		self._noColor = noColor

	def __call__(self, *args, **kwargs):
		self.text(*args, **kwargs)

	def text(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.text, self._noColor), 
			**kwargs
		)

	def success(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.success, self._noColor), 
			**kwargs
		)
	
	def error(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.error, self._noColor), 
			**kwargs
		)
	
	def warning(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.warning, self._noColor), 
			**kwargs
		)
	
	def primary(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.primary, self._noColor), 
			**kwargs
		)
	
	def info(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.info, self._noColor), 
			**kwargs
		)

	def debug(self, *args, **kwargs):
		print(
			*Colors.makeColored(args, Colors.debug, self._noColor), 
			**kwargs
		)

	def byFlag(
		self,
		*args,
		flag: bool, 
		flagOn: Callable[[str, bool], str] = Colors.success, 
		flagOff: Callable[[str, bool], str] = Colors.error, 
		**kwargs
	):
		""" 
		Если flag == True, то выведется flagOn.\n
		Если flag == False, то выведется flagOff.
		"""

		colorBy = flagOn if flag else flagOff
		print(
			*Colors.makeColored(args, colorBy, self._noColor), 
			**kwargs
		)


cprint = Printer()
ncprint = Printer(noColor=True)
