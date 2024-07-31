from src.consts import Language

class FormatException(Exception): pass

class FormatNotSupported(FormatException):
    def __init__(self, lang: Language):
        super().__init__(f"Не поддерживается форматирование языка: {lang.name}")