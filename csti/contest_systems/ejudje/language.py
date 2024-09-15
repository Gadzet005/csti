from csti.etc.language import GeneralLanguage, Language


class EjudjeLanguage(Language):
    nasm = {
        **GeneralLanguage.nasm.value,
        "id": 50,
    }
