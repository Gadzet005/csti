from csti.etc.language import Language

LANG_DIR = "csti/contest/systems/contest_solutions/langs/nasm/"


class ContestSolutionsLanguage(Language):
    nasm = {
        "id": 50,
        "fullName": "Nasm x86",
        "isCompiledLanguage": True,
        "availableFileExtensions": [".asm"],
        "comment": ";",
        "makefile": LANG_DIR + "makefile",
        "templateFile": LANG_DIR + "template.asm",
    }
