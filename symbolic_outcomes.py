from ftplib import error_reply
from z3 import And, Not
from cmd import Assume, Assert, Fork, Assign

def symbolic_outcomes(blk, C, P):
    if len(blk) == 0 :
        return [(C, P)]
    else :
        hd = blk[0]
        if (isinstance(hd, Fork)) :
            symbOuts = symbolic_outcomes(hd.cmd2, C, P) + symbolic_outcomes(hd.cmd1, C, P)
            accOuts = []
            for outC, outP in symbOuts:
                accOuts += symbolic_outcomes(blk[1:], outC, outP)
            return accOuts
        elif (isinstance(hd, Assume)) :
            return symbolic_outcomes(blk[1:], And(C, hd.bexp), P)
        elif (isinstance(hd, Assign)) :
            return symbolic_outcomes(blk[1:], And(C, hd.eq), P) # cond is just assignment here
        elif (isinstance(hd, Assert)) :
            return symbolic_outcomes(blk[1:], C, And(P, hd.bexp)) # not sure about this