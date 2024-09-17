import typing as t

from termcolor import colored


class Color:
    """
    Класс для добавления к тексту escape-последовательностей
    (для придания цвета и форматирования).
    """

    Transformer: t.TypeAlias = t.Callable[[str], str]

    success = lambda x: colored(x, "green")
    error = lambda x: colored(x, "red")
    warning = lambda x: colored(x, "yellow")
    primary = lambda x: colored(x, "blue")
    info = lambda x: colored(x, "cyan")
    debug = lambda x: colored(x, "magenta", attrs=["bold"])

    @staticmethod
    def makeColored(
        values: tuple[str, ...],
        colorBy: Transformer,
    ) -> tuple[str, ...]:
        """Перекрашивает список строк."""
        return tuple(map(lambda x: colorBy(x), values))


class Printer:
    """Класс для цветного вывода в терминал."""

    def __init__(self, file: t.Optional[t.TextIO] = None, noColor: bool = False):
        self._file = file
        self._noColor = noColor

    @property
    def file(self) -> t.Optional[t.TextIO]:
        return self._file

    def __call__(self, *args, **kwargs):
        self.text(*args, **kwargs)

    def colored(
        self, messages: tuple[str, ...], colorBy: Color.Transformer
    ) -> tuple[str, ...]:
        if self._noColor or self._file is not None:
            return messages
        else:
            return Color.makeColored(messages, colorBy)

    def text(self, *args, **kwargs):
        print(*args, file=self._file, **kwargs)

    def success(self, *args, **kwargs):
        print(*self.colored(args, Color.success), file=self._file, **kwargs)

    def error(self, *args, **kwargs):
        print(*self.colored(args, Color.error), file=self._file, **kwargs)

    def warning(self, *args, **kwargs):
        print(*self.colored(args, Color.warning), file=self._file, **kwargs)

    def primary(self, *args, **kwargs):
        print(*self.colored(args, Color.primary), file=self._file, **kwargs)

    def info(self, *args, **kwargs):
        print(*self.colored(args, Color.info), file=self._file, **kwargs)

    def debug(self, *args, **kwargs):
        print(*self.colored(args, Color.debug), file=self._file, **kwargs)

    def byFlag(
        self,
        *args,
        flag: bool,
        flagOn: Color.Transformer = Color.success,
        flagOff: Color.Transformer = Color.error,
        **kwargs
    ):
        """
        Если flag=`True`, то выведется `flagOn`.

        Если flag=`False`, то выведется `flagOff`.
        """

        colorBy = flagOn if flag else flagOff
        print(*self.colored(args, colorBy), **kwargs)
