from csti.etc.language import GeneralLanguage, Language


class ContestSolutionsLanguage(Language):
    nasm = {
        **GeneralLanguage.nasm.value,
        "id": 50,
    }
