from csti.etc.language import Language, GeneralLanguage


class Ejudge2KursVmkLanguage(Language):
    c = {
        **GeneralLanguage.c.value,
        "id": 2,
    }
