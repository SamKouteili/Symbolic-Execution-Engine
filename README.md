# Symbolic Execution Engine
CPSC 554 - Spring 2022

*Authors: Sam Kouteili, Nhi Nguyen*

Symbolic Execution Engine for simple imperative programs. The engine considers *lim* versions of a program, where each iteration unfolds program loops *n* times (*n* is a unique number between 0 and *lim*). Program outputs all unique potential error states (i.e example values that may lead to an error state) for each program iteration. E.g
```
program simple(x y)
    pre x > 0
is
    while x > y do
        x := x - 1;
    end
    assert x != y;
end
```
should return the following output if `lim=2`:
```
simple 1 1
simple 1 0
simple 2 0
```
Indeed, if we unroll the while loop 0 times, `x=1, y=1` returns an error state. If we unroll the while loop once, `x=1, y=0` returns an error state, etc.

## Part 1: Compilation & Installations

**Step 1: Install requirements**

`pip install -r requirements.txt`

**Step 2: Running the Symbolic Excution Engine**

`python see.py [file_name.imp] [lim] [--debug]`

## Part 2: Benchmarks

Unique benchmarks presented in [benchmarks](benchmarks) directory. 

Expected outputs presented in [benchmarks/outputs](benchmarks/outputs) folder. 

Outputs do not necessarily have to exactly adhere to the ones presented.
