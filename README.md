# Verification Condition Generation
CPSC 554 - Spring 2022
*Author: Nhi Nguyen*

## Part 1: How to run vcgen

**Step 1: Install requirements**
`pip install -r requirements.txt`

**Step 2: Run vcgen**
`python vcgen.py [file_name.imp]`

*Optional: Debug mode*
`python vcgen.py [file_name.imp] --debug`

## Part 2: Benchmarks

There are 5 valid benchmarks and 4 invalid benchmarks in folder `benchmark`.

Valid benchmarks:
* cumsum.imp
* negate.imp
* palindrome.imp
* shuffle.imp
* xor.imp

Invalid benchmarks:
* cumsum_bad.imp
* negate_bad.imp
* shuffle_bad.imp
* xor_bad.imp