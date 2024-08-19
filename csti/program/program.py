from __future__ import annotations

import os
import subprocess

from consts import Language
from program.exceptions import (CompileError, FormatError,
									NotSupportedLanguage, RunError,
									TimeoutError)
from program.make import LangInfo, MakeTarget
from program.test_result import TestResultList, TestStatus
from program.utils import normalizeText


class Program:
	""" 
	Выполняет запуск, компиляцию, форматирование и 
	тестирование программы на заданном языке 
	"""

	def __init__(self, lang: Language, filePath: str):
		self.lang = lang
		self.filePath = filePath

	def __enter__(self):
		if self._langInfo.canBeCompiled:
			self.compile()
		return self
	
	def __exit__(self, *args):
		self.clear()


	def compile(self):
		""" Компилирует программу """

		if not self._langInfo.canBeCompiled:
			raise NotSupportedLanguage(self.lang)

		result: subprocess.CompletedProcess = subprocess.run([
			"make", MakeTarget.compile.value, "-f", self._langInfo.makefile, 
			f"DIR={self.dir}", 
			f"FILE={self.file}", 
			f"COMPILED_FILE={self.compiledFile}"
		], capture_output=True
		)

		if result.returncode != 0:
			raise CompileError(result.stderr.decode())
	
	def run(self, input: str|None = None, timeout: str|None = None) -> str:
		""" 
		Запускает программу и возвращает её вывод. 
		Если язык компилируемый, то требуется вызов метода compile
		"""

		inputBuffer = input.encode() if input else None

		try:
			result: subprocess.CompletedProcess = subprocess.run([
					"make", MakeTarget.run.value, "-f", self._langInfo.makefile,
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

		if not self._langInfo.canBeFormatted:
			raise NotSupportedLanguage(self.lang)

		result: subprocess.CompletedProcess = subprocess.run([
				"make", MakeTarget.format.name, "-f", self._langInfo.makefile,
				f"FORMAT_CONFIG={self._langInfo.formatConfig}",
				f"DIR={self.dir}", 
				f"FILE={self.file}", 
				f"FORMATTED_FILE={self.formattedFile}"
			], capture_output=True
		)

		if result.returncode != 0:
			raise FormatError(result.stderr.decode())

		return Program(self.lang, os.path.join(self.dir, self.formattedFile))

	def clear(self, clearSelf=False):
		""" 
		Очистка временных файлов 
		clearSelf: Требуется ли очистка самой программы?
		"""

		subprocess.run([
			"make", MakeTarget.clear.name, "-f", self._langInfo.makefile, 
			f"DIR={self.dir}",
			f"COMPILED_FILE={self.compiledFile}", 
			f"OUTPUT_FILE={self.outputFile}"
		], capture_output=True
		)

		if clearSelf:
			os.remove(self.filePath)

	def test(self, testCases: list[tuple[str, str]], timeout: str|None = None) -> TestResultList:
		"""
		Запуск тестов. Если язык компилируемый, то требуется вызов метода compile\n
		testCases: [(вход, ожидаемый выход), ...]
		"""

		results = TestResultList()
		for input, expected in testCases:
			try:
				output = normalizeText(self.run(input, timeout))
				expected = normalizeText(expected)

				if output == expected:
					results.append(TestStatus.ok)
				else:
					results.append(
						TestStatus.wrongAnswer, 
						f"Входные данные:\n{input}\n"
						f"Выходные данные:\n{output}\n"
						f"Ожидаемые выходные данные:\n{expected}"
					)
			except RunError as error:
				results.append(TestStatus.runtimeError, error.__str__())
			except TimeoutError:
				results.append(TestStatus.timeLimit)

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
		self._langInfo = LangInfo.fromLang(lang)
