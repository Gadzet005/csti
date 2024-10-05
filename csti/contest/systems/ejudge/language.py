from csti.etc.language import Language, GeneralLanguage


class EjudgeLanguage(Language):
    c = GeneralLanguage.c.value
    cpp = {
        **GeneralLanguage.cpp.value,
        "id": 3,
    }
