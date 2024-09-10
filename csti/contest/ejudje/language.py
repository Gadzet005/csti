from csti.etc.language import ILanguage, Language


class EjudjeLanguage(ILanguage):
    nasm = {
        **Language.nasm.value,
        "id": 50,
    }
     
    c = Language.c.value
