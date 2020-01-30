# sudoku_solver
WIP

Usage:
$python solver.py 9 0:1 5:9 80:4

9=size (can be 1,4,9,16,25...)

given format: x:y

x is the position starting with 0 in the top left and reading left to right top to bottom with 80 at the bottom right

y is the value of the given from 1-9

Mainly tested on 4x4 not 9x9.

can generate one solution if number of givens is >= minimum, or will generate multiple solution if < minimum.

Now functional for 4x4 and easy 9x9 but too slow for hard 9x9 (don't even try 16x16 or greater).

on 4x4 if can test ~100,000 possibilies in a couple of seconds I think.


todo:

check input to makes sure it is actually valid

naked/hidden pairs/triplets/quadruplets

multithreading
