class ProgramError(Exception):
    def __init__(self, message=None):
        self.message = message

class RuntimeError(ProgramError): pass
class CompileError(ProgramError): pass