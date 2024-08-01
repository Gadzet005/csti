class ProgramError(Exception): pass
class RuntimeError(ProgramError): pass
class CompileError(ProgramError): pass