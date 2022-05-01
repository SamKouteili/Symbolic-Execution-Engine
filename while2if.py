from ntpath import join


def join_unchange(nodes):
    return " ".join([str(node) for node in nodes])

def unravel_while_loop_recursive(bexp, block, lim):
    if lim == 0:
        return f"assume ! {bexp} ;"
    return f"if {bexp} then {block} {unravel_while_loop_recursive(bexp, block, lim-1)} end"

def create_while2if(lim):
    while2if = {
        "N": lambda _, n: n,
        "X": lambda _, x: x,
        "AEXP" : [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes)
        ],
        "COMP" : [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes)
        ],
        "BEXP" : [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes)
        ],
        "ASSN" : [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange([nodes[0], join_unchange(nodes[1]), nodes[2], nodes[3]]),
            lambda _, nodes: join_unchange([nodes[0], join_unchange(nodes[1]), nodes[2], nodes[3]]),
            lambda _, nodes: join_unchange(nodes)
        ],
        "STMT" : [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: unravel_while_loop_recursive(nodes[1], nodes[3], lim),
            lambda _, nodes: join_unchange(nodes)
        ],
        "BLOCK": lambda _, nodes: join_unchange(nodes[0]),
        "VAR": [
            lambda _, nodes: join_unchange(nodes),
            lambda _, nodes: join_unchange(nodes)
        ],
        "PROG": lambda _, nodes: join_unchange(nodes[:3] + [join_unchange(nodes[3])] + [nodes[4]] + [join_unchange(node) for node in nodes[5]] + nodes[6:])
    }
    return while2if