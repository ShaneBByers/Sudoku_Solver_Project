import time

def sudoku_cells():
    return_list = []
    for i in range(9):
        for j in range(9):
            return_list.append((i, j))
    return return_list
    pass


def sudoku_arcs():
    return_list = []

    cells = sudoku_cells()
    for (i, j) in cells:
        for (a, b) in cells:
            if i == a or j == b or (i/3 == a/3 and j/3 == b/3):
                return_list.append(((i, j), (a, b)))

    return return_list
    pass


def read_board(path):

    in_file = open(path)

    board = []

    for i in range(9):
        row = []
        for j in range(9):
            num = in_file.read(1)
            row.append(num)
        in_file.read(2)
        board.append(row)

    in_file.close()

    return board

    pass


def board_to_dict(board):
    return_dict = {}

    possible_values = []

    for i in range(9):
        possible_values.append(i + 1)

    for (i, row) in enumerate(board):
        for (j, col) in enumerate(board[i]):
            possibilities = []
            if board[i][j] == '*':
                possibilities = set(possible_values)
            else:
                possibilities.append(int(board[i][j]))
            return_dict[(i, j)] = set(possibilities)

    return return_dict


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    board = {}

    def __init__(self, board):
        self.board = board
        pass

    def get_board(self):
        _board = []

        for i in range(9):
            row = []
            for j in range(9):
                num = list(self.get_values((i, j)))[0]
                row.append(num)
            _board.append(row)

        return _board
        pass

    def get_values(self, cell):
        return self.board[cell]
        pass

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) not in self.ARCS:
            return False
        else:
            new_values = []
            found_inconsistency = False

            if len(self.board[cell1]) != 1:
                if len(self.board[cell2]) == 1:
                    for i in self.board[cell1]:
                        if i not in self.board[cell2]:
                            new_values.append(i)
                        else:
                            found_inconsistency = True

            new_set = set(new_values)

            if found_inconsistency:
                self.board[cell1] = new_set
                return True
            else:
                return False

        pass

    def infer_ac3(self):

        something_changed = False
        changed_cells = self.CELLS
        while len(changed_cells) != 0:
            new_changed_cells = []
            for (changed_cell, needs_updated_cell) in self.ARCS:
                if changed_cell in changed_cells:
                    if self.remove_inconsistent_values(needs_updated_cell, changed_cell):
                        something_changed = True
                        if needs_updated_cell not in new_changed_cells:
                            new_changed_cells.append(needs_updated_cell)
            changed_cells = new_changed_cells

        return something_changed
        pass

    def infer_improved(self):
        something_changed = True

        while something_changed:

            something_changed = self.infer_ac3()

            for cell in self.CELLS:
                found_single_value = False
                single_value = -1
                row_list = []
                col_list = []
                sqr_list = []
                for compare_cell in self.CELLS:
                    if cell != compare_cell:
                        if cell[0] == compare_cell[0]:
                            for num in self.board[compare_cell]:
                                row_list.append(num)

                        if cell[1] == compare_cell[1]:
                            for num in self.board[compare_cell]:
                                col_list.append(num)

                        if cell[0]/3 == compare_cell[0]/3 and cell[1]/3 == compare_cell[1]/3:
                            for num in self.board[compare_cell]:
                                sqr_list.append(num)

                for value in self.board[cell]:
                    if not found_single_value:
                        if value not in row_list or value not in col_list or value not in sqr_list:
                            found_single_value = True
                            single_value = value
                if found_single_value and len(self.board[cell]) != 1:
                    new_value = [single_value]
                    new_set = set(new_value)
                    self.board[cell] = new_set
                    something_changed = True
        pass

    def check_solved(self):
        for (i, j) in self.ARCS:
            if i != j and self.board[i] == self.board[j]:
                return False

        return True
        pass

    def infer_with_guessing_helper(self, board):

        all_single_values = True

        for cell in self.CELLS:
            self.board[cell] = board[cell]
            if len(board[cell]) != 1:
                all_single_values = False

        if all_single_values and self.check_solved():
            return True
        elif all_single_values:
            return False

        min_len = 10

        min_len_cell = (-1, -1)

        for cell in self.CELLS:
            curr_len = len(self.board[cell])
            if curr_len != 1:
                if len(self.board[cell]) < min_len:
                    min_len_cell = cell
                    min_len = len(self.board[cell])

        min_cell_values = self.board[min_len_cell]

        for value in min_cell_values:
            new_list = [value]
            new_set = set(new_list)
            self.board[min_len_cell] = new_set
            self.infer_improved()
            copy_board = {}
            for copy_cell in self.CELLS:
                copy_board[copy_cell] = self.board[copy_cell]
            solved = self.infer_with_guessing_helper(copy_board)
            if solved:
                return True
            else:
                for reset_cell in self.CELLS:
                    self.board[reset_cell] = board[reset_cell]
                for replace_value in min_cell_values:
                    if replace_value != value:
                        replace_list = [replace_value]
                        replace_set = set(replace_list)
                        self.board[min_len_cell] = replace_set
        pass

    def infer_with_guessing(self):

        self.infer_improved()

        copy_board = {}

        for copy_cell in self.CELLS:
            copy_board[copy_cell] = self.board[copy_cell]

        self.infer_with_guessing_helper(copy_board)

        pass


def print_board(board):
    for i in range(9):
        for j in range(9):
            print board[i][j],
            if (j+1)%3 == 0:
                print " ",
            if (j+1)%9 == 0:
                print
        print
        if (i+1)%3 == 0 and (i+1) != 9:
            print


def solve_board(path):

    board = read_board(path)

    print

    print_board(board)

    sudoku = Sudoku(board_to_dict(board))

    start = time.time()

    sudoku.infer_ac3()

    if sudoku.check_solved():
        end = time.time()
        total = end - start
        print "Easy puzzle solved in " + str(total) + " seconds."
        print
        print_board(sudoku.get_board())
        return

    sudoku.infer_improved()

    if sudoku.check_solved():
        end = time.time()
        total = end - start
        print "Medium puzzle solved in " + str(total) + " seconds."
        print
        print_board(sudoku.get_board())
        return

    sudoku.infer_with_guessing()

    if sudoku.check_solved():
        end = time.time()
        total = end - start
        print "Hard puzzle solved in " + str(total) + " seconds."
        print
        print_board(sudoku.get_board())
        return
