from __future__ import annotations

import os
import subprocess

from csti.consts import Language
from csti.program.exceptions import (
	CompileError, FormatError, NotSupportedLanguage, 
	RunError, TimeoutError
)
from csti.program.make import MakeTarget
from csti.program.test_result import TestResultList, TestStatus
from csti.program.utils import normalizeText


class Program:
	""" 
	Выполняет запуск, компиляцию, форматирование и 
	тестирование программы на заданном языке.
	"""

	def __init__(self, lang: Language, filePath: str):
		self.lang = lang
		self.filePath = filePath

	def compile(self):
		""" Компилирует программу """

		if not self.lang.canBeCompiled:
			raise NotSupportedLanguage(self.lang)

		result: subprocess.CompletedProcess = subprocess.run([
			"make", MakeTarget.compile.value, "-f", self.lang.makefile, 
			f"DIR={self.dir}", 
			f"FILE={self.file}", 
			f"COMPILED_FILE={self.compiledFile}"
		], capture_output=True
		)

		if result.returncode != 0:
			self.clear()
			raise CompileError(result.stderr.decode())
	
	def run(self, input: str|None = None, timeout: str|None = None) -> str:
		""" 
		Запускает программу и возвращает её вывод. 
		Если язык компилируемый, то требуется вызов метода compile
		"""

		inputBuffer = input.encode() if input else None

		try:
			result: subprocess.CompletedProcess = subprocess.run([
					"make", MakeTarget.run.value, "-f", self.lang.makefile,
					f"DIR={self.dir}",
					f"COMPILED_FILE={self.compiledFile}", 
					f"OUTPUT_FILE={self.outputFile}",
				], capture_output=True, input=inputBuffer, timeout=timeout
			)
		except subprocess.TimeoutExpired:
			raise TimeoutError

		if result.returncode != 0:
			raise RunError(result.stderr.decode())
		
		output = ""
		with open(os.path.join(self.dir, self.outputFile), 'r') as file:
			output = file.read()

		return output

	def format(self) -> Program:
		""" 
		Выполняет форматирование программы, возвращает экземпляр 
		Program для отформатированного файла 
		"""

		if not self.lang.canBeFormatted:
			raise NotSupportedLanguage(self.lang)

		result: subprocess.CompletedProcess = subprocess.run([
				"make", MakeTarget.format.name, "-f", self.lang.makefile,
				f"FORMAT_CONFIG={self.lang.formatConfig}",
				f"DIR={self.dir}", 
				f"FILE={self.file}", 
				f"FORMATTED_FILE={self.formattedFile}"
			], capture_output=True
		)

		formattedPath = os.path.join(self.dir, self.formattedFile)

		if result.returncode != 0:
			try:
				os.remove(formattedPath)
			except FileNotFoundError:
				pass
			raise FormatError(result.stderr.decode())

		return Program(self.lang, formattedPath)

	def clear(self, clearSelf=False):
		""" 
		Очистка временных файлов \n
		@param clearSelf: Требуется ли очистка самой программы?
		"""

		subprocess.run([
			"make", MakeTarget.clear.name, "-f", self.lang.makefile, 
			f"DIR={self.dir}",
			f"COMPILED_FILE={self.compiledFile}", 
			f"OUTPUT_FILE={self.outputFile}"
		], capture_output=True
		)

		if clearSelf:
			os.remove(self.filePath)

	# TODO: добавить ограничение занимаемой памяти при выполнении теста
	def test(
			self, testCases: list[tuple[str, str]], timeLimit: int|None = None, 
			memoryLimit: int|None = None
		) -> TestResultList:
		"""
		Запуск тестов. Если язык компилируемый, то требуется вызов метода compile\n
		@param testCases: [(вход, ожидаемый выход), ...]
		@param timeLimit: Максимальное время в секундах для выполнения теста
		@param memoryLimit: Максимальное количество памяти в мегабайтах для выполнения теста
		"""

		results = TestResultList()
		for input, expected in testCases:
			try:
				output = normalizeText(self.run(input, timeLimit))
				expected = normalizeText(expected)

				if output == expected:
					results.append(TestStatus.ok)
				else:
					results.append(
						TestStatus.wrongAnswer, 
						input=input,
						output=output,
                        expected=expected
					)
			except RunError as error:
				results.append(
					TestStatus.runtimeError, input=input, message=error.__str__()
				)
			except TimeoutError:
				results.append(
					TestStatus.timeLimit, input=input
				)

		return results


	@property
	def filePath(self):
		""" Полный путь к файлу """
		return self._filePath
	
	@filePath.setter
	def filePath(self, filePath: str):
		self._filePath = filePath
		self._dir, self._file = os.path.split(filePath)
		self._fileName, self._fileExt = os.path.splitext(self._file)

	@property
	def dir(self):
		""" Дирректория файла """
		return self._dir
	
	@property
	def file(self):
		""" Название файла (с расширением) """
		return self._file
	
	@property
	def compiledFile(self):
		""" Файл после компиляции """
		return self.fileName + "-compiled"

	@property
	def outputFile(self):
		""" Выходные данные файла """
		return self.fileName + "-output.txt"

	@property
	def formattedFile(self):
		""" Файл после форматирования """
		return self.fileName + "-formatted" + self.fileExt

	@property
	def fileName(self):
		""" Название файла (без расширения) """
		return self._fileName
	
	@property
	def fileExt(self):
		""" Расширение файла (с точкой) """
		return self._fileExt

	@property
	def lang(self):
		""" Язык программирования """
		return self._lang
	
	@lang.setter
	def lang(self, lang: Language):
		self._lang = lang
	
	@property
	def code(self):
		""" Код программы """
		with open(self.filePath, 'r') as file:
			return file.read()
		
	@property
	def canBeCompiled(self):
		""" Компилируемый ли язык """
		return self.lang.canBeCompiled
	
	@property
	def canBeFormatted(self):
		""" Форматируемый ли язык """
		return self.lang.canBeFormatted
