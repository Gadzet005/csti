class ProgramError(Exception): pass

class RunError(ProgramError): pass
class CompileError(ProgramError): pass
class FormatError(ProgramError): pass

class LanguageError(ProgramError): pass
class UnexpectedLanguage(LanguageError): pass
class NotSupportedLanguage(LanguageError): pass
