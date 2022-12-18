class InterpreterInterrupt(Exception):
    pass


class StopInterpretation(InterpreterInterrupt):
    pass


class StopProgram(InterpreterInterrupt):
    pass
