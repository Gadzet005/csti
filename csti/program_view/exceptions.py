class ProgramError(Exception):
    pass


class RunError(ProgramError):
    pass


class TimeoutError(ProgramError):
    pass


class CompileError(ProgramError):
    pass


class FormatError(ProgramError):
    pass
