Shane Byers

CMPSC 442 (Artificial Intelligence Course) Project 3: Implement a Sudoku solver to solve easy, medium, and hard difficulty puzzles.

10/13/2016

TO RUN: 
  python -i sudoku_solver.py
  >>> solve_board(path_to_text_file)

EXAMPLE:
  python -i sudoku_solver.py
  >>> solve_board("sudoku/medium1.txt")

This program uses three techniques to solve any solvable Sudoku puzzle.
They all stem from the arc consistency algorithm AC-3. Similar to how a person goes about solving a Sudoku puzzle.
This program first fills in all of the obvious unkown values, then it proceeds to fill in unknown values based on their dependencies on other unkown values. 
If the program cannot complete the puzzle using the above algorithm, it begins guessing one unkown value at a time until a solution is found.

There are a number of example unfinished Sudoku boards in the "sudoku" folder. You are also welcome to write your own boards for testing using the same layout as the provided examples. Simply write the numbers into a text document (with * in place of the unknown values), and run the program using the above instructions. The result of running the program will show you the starting board layout, the difficulty of the puzzle, the time it took to solve the puzzle, and the solution board layout.

KNOWN ISSUES:

The choice of which unknown to guess can be written slightly more efficiently to avoid wrong guesses. That change might shave off a second or so from the longer solution times.
