from matplotlib.pyplot import get
from z3 import IntVal, Int, IntSort, Array, Store, Not, Or, And, Implies, ForAll, Exists
from cmd import Assume, Assert, Fork, Assign

# Array variables

def get_array(arr):
    return Array(str(arr),IntSort(),IntSort())

def exp_array(arr, ind):
    A = get_array(arr)
    return A[ind]

def get_array_assign(nodes):
    x = nodes[0]
    ind = nodes[2]
    exp = nodes[5]
    old_x = get_array(get_variable(x))
    new_x = get_array(get_variable(x, inc=True))
    return Assign(new_x == Store(old_x, ind, exp), new_x)

# Get new and/or existing variable

VARS = {}

def get_variable(var, inc=False):
    if inc:
        if var not in VARS:
            VARS[var] = 0
        else:
            VARS[var] += 1
    return Int(f"{var}.{VARS[var]}")

# Balance variables index when entering fork

def get_assigned_vars(block):
    if len(block) == 0:
        return []
    hd = block[0]
    if isinstance(hd, Assign):
        return [hd.new_var] + get_assigned_vars(block[1:])
    elif isinstance(hd, Fork):
        return get_assigned_vars(hd.cmd1) + get_assigned_vars(block[1:])
    return []

def get_first_last_assigned(block):
    assigned_vars = get_assigned_vars(block)
    first_assigned = {}
    last_assigned = {}
    for var in assigned_vars:
        name, ind = str(var).split(".")
        ind = int(ind)
        if name not in first_assigned or first_assigned[name] > ind:
            first_assigned[name] = ind
        if name not in last_assigned or last_assigned[name] < ind:
            last_assigned[name] = ind
    return first_assigned, last_assigned

def balance_assigned_vars(block1, block2):
    first_assigned1, last_assigned1 = get_first_last_assigned(block1)
    first_assigned2, last_assigned2 = get_first_last_assigned(block2)
    add1 = []
    add2 = []
    for name in last_assigned1:
        if name not in last_assigned2:
            before_fork = Int(f"{name}.{first_assigned1[name]-1}")
            after_fork = Int(f"{name}.{last_assigned1[name]}")
            add2.append(Assume(before_fork == after_fork))
        elif last_assigned2[name] < last_assigned1[name]:
            in_fork2 = Int(f"{name}.{last_assigned2[name]}")
            in_fork1 = Int(f"{name}.{last_assigned1[name]}")
            add2.append(Assume(in_fork2 == in_fork1))
    for name in last_assigned2:
        if name not in last_assigned1:
            before_fork = Int(f"{name}.{first_assigned2[name]-1}")
            after_fork = Int(f"{name}.{last_assigned2[name]}")
            add1.append(Assume(before_fork == after_fork))
        elif last_assigned1[name] < last_assigned2[name]:
            in_fork1 = Int(f"{name}.{last_assigned1[name]}")
            in_fork2 = Int(f"{name}.{last_assigned2[name]}")
            add1.append(Assume(in_fork1 == in_fork2))
    return block1 + add1, block2 + add2

def create_fork(nodes, els):
    block1 = nodes[3]
    block2 = nodes[5] if els else []
    block1, block2 = balance_assigned_vars(block1, block2)
    return [Fork(
                [Assume(nodes[1])] + block1,
                [Assume(Not(nodes[1]))] + block2
            )]

language2cmd = {
    "N": lambda _, n: IntVal(n),
    "X": lambda _, x: x,
    "AEXP" : [
        lambda _, nodes: nodes[0],
        lambda _, nodes: get_variable(nodes[0]),
        lambda _, nodes: exp_array(get_variable(nodes[0]), nodes[2]),
        lambda _, nodes: - nodes[1],
        lambda _, nodes: (nodes[0] + nodes[2]),
        lambda _, nodes: (nodes[0] - nodes[2]),
        lambda _, nodes: (nodes[0] * nodes[2]),
        lambda _, nodes: (nodes[0] / nodes[2]),
        lambda _, nodes: (nodes[0] % nodes[2]),
        lambda _, nodes: (nodes[1])
    ],
    "COMP" : [
        lambda _, nodes: (nodes[0] == nodes[2]),
        lambda _, nodes: (nodes[0] != nodes[2]),
        lambda _, nodes: (nodes[0] <= nodes[2]),
        lambda _, nodes: (nodes[0] >= nodes[2]),
        lambda _, nodes: (nodes[0] < nodes[2]),
        lambda _, nodes: (nodes[0] > nodes[2])
    ],
    "BEXP" : [
        lambda _, nodes: nodes[0],
        lambda _, nodes: Not(nodes[1]),
        lambda _, nodes: Or(nodes[0], nodes[2]),
        lambda _, nodes: And(nodes[0], nodes[2]),
        lambda _, nodes: (nodes[1])
    ],
    "ASSN" : [
        lambda _, nodes: nodes[0],
        lambda _, nodes: Not(nodes[1]),
        lambda _, nodes: Or(nodes[0], nodes[2]),
        lambda _, nodes: And(nodes[0], nodes[2]),
        lambda _, nodes: Implies(nodes[0], nodes[2]),
        lambda _, nodes: ForAll(nodes[1], nodes[3]),
        lambda _, nodes: Exists(nodes[1], nodes[3]),
        lambda _, nodes: (nodes[1])
    ],
    "QVAR": lambda _, nodes: get_variable(nodes[0], inc=True),
    "STMT" : [
        lambda _, nodes: [Assign(get_variable(nodes[0], inc=True) == nodes[2], get_variable(nodes[0]))],
        lambda _, nodes: [Assign(get_variable(nodes[0], inc=True) == nodes[4], get_variable(nodes[0])), Assign(get_variable(nodes[2], inc=True) == nodes[6], get_variable(nodes[2]))],
        lambda _, nodes: [get_array_assign(nodes)],
        lambda _, nodes: create_fork(nodes, els=True),
        lambda _, nodes: create_fork(nodes, els=False),
        lambda _, nodes: [Assume(nodes[1])],
        lambda _, nodes: [Assert(nodes[1])]
    ],
    "BLOCK": lambda _, nodes: [inner for outer in nodes[0] for inner in outer],
    "VAR": [
        lambda _, nodes: get_variable(nodes[0], inc=True),
        lambda _, nodes: get_array(get_variable(nodes[0], inc=True))
    ],
    "PROG": lambda _, nodes: [nodes[1], nodes[3], [Assume(bexp) for _, bexp in nodes[5]] + nodes[7]]
}