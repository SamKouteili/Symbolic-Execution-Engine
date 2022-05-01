from parglare import Parser, Grammar
from language2cmd import language2cmd
from while2if import create_while2if, join_unchange
from symbolic_outcomes import symbolic_outcomes
from z3 import Tactic, And, Not, sat, Int
import argparse

def print_title(name):
    print(f"\n{'#'*20}\n {name}\n{'#'*20}")

def see(progname, progvars, symbOuts) :
    noViolations = True
    for symbOut in symbOuts :
        s = Tactic('smt').solver()
        s.add(symbOut)
        if s.check() == sat :
            noViolations = False
            print_true_vars(progname, progvars, s.model()) # double check
            # break # needs to break out of inner for-loop
    
    if noViolations :
        print("No Violations Found")

def print_true_vars(progname, progvars, m) :
    varnames = [str(var) for var in progvars]
    varsset = set(varnames)
    varsdict = {}
    for d in m.decls():
        if d.name() in varnames:
            varsdict[d.name()] = m[d]
    print(progname, join_unchange([varsdict[v] if v in varsdict else -1 for v in varnames]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Symbolic Execution Engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("filename", type=str, help="program file with extension .imp")
    parser.add_argument("lim", type=int, help="loop limit")
    parser.add_argument("--debug", default=False, action="store_true", help="debug mode")
    args = parser.parse_args()

    file = args.filename
    with open(file) as f:
        program = f.read()
    if args.debug:
        print_title("Program")
        print(program)
        print_title("Loop Limit")
        print(args.lim)
    
    while2if = create_while2if(args.lim)
    grammar = Grammar.from_file("language.pg")
    parser = Parser(grammar, actions=while2if)
    if_program = parser.parse(program)
    if args.debug:
        print_title("If Program")
        print(if_program)

    grammar = Grammar.from_file("modified_language.pg")
    cmd_parser = Parser(grammar, actions=language2cmd)
    cmd_program = cmd_parser.parse(if_program)
    if args.debug:
        print_title("Command Program")
        print(cmd_program)

    progname, progvars, progcmds = cmd_program

    symbOuts = symbolic_outcomes(progcmds, True, True) # formula with just true
    symbOuts = [And(C, Not(P)) for C, P in symbOuts]
    if args.debug:
        print_title("Symbolic Outcomes")
        for (i, symbOut) in enumerate(symbOuts):
            print(f"Outcome {i+1}")
            print(f"{symbOut}\n")

    see(progname, progvars, symbOuts)