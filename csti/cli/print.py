from typing import Callable

from termcolor import colored


class Colored:
	text = 		lambda x: x
	success = 	lambda x: colored(x, "green")
	error = 	lambda x: colored(x, "red")
	warning = 	lambda x: colored(x, "yellow")
	primary = 	lambda x: colored(x, "blue")
	info = 		lambda x: colored(x, "cyan")
	debug = 	lambda x: colored(x, "magenta", attrs=["bold"])


class Printer:
	""" Класс для цветного вывода в терминал """

	def __init__(self, noColors: bool = False):
		self._noColors = noColors

	def __call__(self, msg: str = "", *args, **kwargs):
		self.text(msg, *args, **kwargs)

	def text(self, msg: str, *args, **kwargs):
		print(Colored.text(msg), *args, **kwargs)

	def success(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.success
		print(coloredFunc(msg), *args, **kwargs)
	
	def error(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.error
		print(coloredFunc(msg), *args, **kwargs)
	
	def warning(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.warning
		print(coloredFunc(msg), *args, **kwargs)
	
	def primary(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.primary
		print(coloredFunc(msg), *args, **kwargs)
	
	def info(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.info
		print(coloredFunc(msg), *args, **kwargs)

	def debug(self, msg: str, *args, **kwargs):
		coloredFunc = Colored.text if self._noColors else Colored.debug
		print(coloredFunc(msg), *args, **kwargs)

	def byFlag(
		self,
		msg: str,
		*args,
		flag: bool, 
		flagOn: Callable[[str], str] = Colored.success, 
		flagOff: Callable[[str], str] = Colored.error, 
		**kwargs
	):
		""" 
		Если flag == True, то выведется flagOn(msg).\n
		Если flag == False, то выведется flagOff(msg).
		"""

		if self._noColors:
			print(Colored.text(msg), *args, **kwargs)
		else:
			msg = flagOn(msg) if flag else flagOff(msg)
			print(msg, *args, **kwargs)


cprint = Printer()
ncprint = Printer(noColors=True)
