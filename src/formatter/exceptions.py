from src.consts import Language

class FormatError(Exception): pass

class FormatNotSupported(FormatError):
    def __init__(self, lang: Language):
        super().__init__(f"Не поддерживается форматирование языка: {lang.name}")