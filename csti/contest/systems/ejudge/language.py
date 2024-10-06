from csti.etc.language import GeneralLanguage, Language


class EjudgeLanguage(Language):
    c = GeneralLanguage.c.value
    cpp = {
        **GeneralLanguage.cpp.value,
        "id": 3,
    }
