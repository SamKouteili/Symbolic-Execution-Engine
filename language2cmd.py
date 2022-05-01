from z3 import IntVal, Int, IntSort, Array, Store, Not, Or, And, Implies, ForAll, Exists, substitute
from cmd import Assume, Assert, Fork, Assign

def unravel_while_loop(bexp, block, lim):
    if lim == 0:
        return [Assume(Not(bexp))]
    return [Fork(
                [Assume(bexp)] + block + unravel_while_loop(bexp, block, lim-1),
                [Assume(Not(bexp))]
            )]

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
    return Assign(new_x == Store(old_x, ind, exp))

VARS = {}

def get_variable(var, inc=False):
    if inc:
        if var not in VARS:
            VARS[var] = 0
        else:
            VARS[var] += 1
    return Int(f"{var}_{VARS[var]}")

# def assign(var, exp):
#     global TMP_COUNTER
#     TMP_COUNTER += 1
#     if var.num_args() == 2:
#         arr = var.arg(0)
#         ind = var.arg(1)
#         tmp_arr = Array(f"_tmp_{arr}{TMP_COUNTER}",IntSort(),IntSort())
#         tmp_ind = substitute(ind, (arr, tmp_arr))
#         tmp_exp = substitute(exp, (arr, tmp_arr))
#         return [Assume(tmp_arr == arr), 
#                 Havoc(arr, isarr=True), 
#                 Assume(arr == Store(tmp_arr, tmp_ind, tmp_exp))]
#     else:
#         tmp = Int(f"_tmp_{var}{TMP_COUNTER}")
#         return [Assume(tmp == var), 
#                 Havoc(var), 
#                 Assume(var == substitute(exp, (var, tmp)))]



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
        lambda _, nodes: [Assign(get_variable(nodes[0], inc=True) == nodes[2])],
        lambda _, nodes: [Assign(get_variable(nodes[0], inc=True) == nodes[4]), Assign(get_variable(nodes[2], inc=True) == nodes[6])],
        lambda _, nodes: [get_array_assign(nodes)], #TODO
        lambda _, nodes: [Fork(
                            [Assume(nodes[1])] + nodes[3],
                            [Assume(Not(nodes[1]))] + nodes[5]
                        )],
        lambda _, nodes: [Fork(
                            [Assume(nodes[1])] + nodes[3],
                            [Assume(Not(nodes[1]))]
                        )],
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