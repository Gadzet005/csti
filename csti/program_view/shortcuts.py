import typing as t

from csti.program_view.program_view import ProgramView


class prepareForRun:
    """
    Контекстный менеджер подготовки программы для запуска.
    Очищает временные файлы при выходе.

    Пример::

        program = ProgramView(...)
        with prepareForRun(program):
            program.run()
    """

    def __init__(self, program: ProgramView):
        self._program = program

    def __enter__(self) -> ProgramView:
        self._program.compile()
        return self._program

    def __exit__(self, *args):
        self._program.clear()


class format:
    """
    Контекстный менеджер форматирования программы.
    Очищает отформатированный файл при выходе.

    Пример::

        program = ProgramView(...)
        with formatProgram(program, "style") as formatted:
            print(formatted.filePath)
    """

    def __init__(self, program: ProgramView, formatStyle: str):
        self._origin: ProgramView = program
        self._formatted: t.Optional[ProgramView] = None
        self._formatStyle = formatStyle

    def __enter__(self) -> ProgramView:
        self._formatted = self._origin.format(self._formatStyle)
        return self._formatted

    def __exit__(self, *args):
        if self._formatted:
            self._formatted.clear(clearSelf=True)


def run(program: ProgramView) -> str:
    """Запускает программу и возвращает её вывод."""
    with prepareForRun(program):
        return program.run()
