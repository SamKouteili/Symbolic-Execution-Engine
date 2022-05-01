class Cmd():
    def __init__(self, op, args):
        self.op = op
        self.args = args
    
    def __repr__(self):
        return f"{self.op}({', '.join([str(x) for x in self.args])})"

class Assign(Cmd):
    def __init__(self, eq, new_var):
        super().__init__("ASSIGN", [eq])
        self.eq = eq
        self.new_var = new_var

class Assume(Cmd):
    def __init__(self, bexp):
        super().__init__("ASSUME", [bexp])
        self.bexp = bexp

class Assert(Cmd):
    def __init__(self, bexp):
        super().__init__("ASSERT", [bexp])
        self.bexp = bexp

class Fork(Cmd):
    def __init__(self, cmd1, cmd2):
        super().__init__("FORK", [cmd1, cmd2])
        self.cmd1 = cmd1
        self.cmd2 = cmd2