class Cmd():
    def __init__(self, op, args):
        self.op = op
        self.args = args
    
    def __repr__(self):
        return f"{self.op}({', '.join([str(x) for x in self.args])})"

class Assign(Cmd):
    def __init__(self, eq):
        super().__init__("ASSIGN", [eq])
        self.eq = eq

# class Assign(Cmd):
#     def __init__(self, var, val):
#         super().__init__("ASSIGN", [var, val])
#         self.var = var
#         self.val = val

class DAssign(Cmd):
    def __init__(self, var1, exp1, var2, exp2):
        super().__init__("DASSIGN", [var1, exp1, var2, exp2])
        self.var1 = var1
        self.exp1 = exp1
        self.exp2 = var2
        self.exp2 = exp2

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

# Helper function to get modified variables
# def get_modified_vars(block):
#     vars_set = set()
#     for cmd in flatten_block(block):
#         if isinstance(cmd, Havoc):
#             if cmd.isarr:
#                 vars_set.add((cmd.var, True))
#             else:
#                 vars_set.add((cmd.var, False))
#     return list(vars_set)
    
# def flatten_block(block):
#     if len(block) == 0:
#         return block
#     if isinstance(block[0], Fork):
#         return flatten_block(block[0].cmd1) + flatten_block(block[0].cmd2) + flatten_block(block[1:])
#     return block[:1] + flatten_block(block[1:])
