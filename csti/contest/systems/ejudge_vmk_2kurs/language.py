from csti.etc.language import GeneralLanguage, Language


class Ejudge2KursVmkLanguage(Language):
    c = {
        **GeneralLanguage.c.value,
        "id": 2,
    }
