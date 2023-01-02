#function to read information from text file(dai ca minh)
#WORK PERFECT
with open('nngram.txt') as f:
    size = f.readline()
    values = f.readlines()
(m, n) = size.strip().split(' ')
m = int(m)
n = int(n)
v_rows = values[:m]
v_cols = values[m:m+n]
row_list = list()
for i in v_rows:
    row_list.append([int(j) for j in i.strip().split()])
col_list = list()
for i in v_cols:
    col_list.append([int(j) for j in i.strip().split()])


#Logical Backtracking
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt 
from IPython.display import clear_output
class Nonogram:
    def __init__(self, ROWS_VALUES=[[3], [2], [1], [1, 2], [3, 1]], COLS_VALUES=[[2], [1, 1], [2, 1], [2, 1], [3]]):
        self.ROWS_VALUES = ROWS_VALUES
        self.no_of_rows = len(ROWS_VALUES)
        #self.rows_changed = [0] * self.no_of_rows
        self.rows_done = [0] * self.no_of_rows

        self.COLS_VALUES = COLS_VALUES
        self.no_of_cols = len(COLS_VALUES)
        #self.cols_changed = [0] * self.no_of_cols
        self.cols_done = [0] * self.no_of_cols

        self.solved = False
        #self.shape = (self.no_of_rows, self.no_of_cols)
        self.board = [[0 for c in range(self.no_of_cols)] for r in range(self.no_of_rows)]

        #step 1: define all possible solution 
        self.rows_possible = self.create_possibilities(ROWS_VALUES, self.no_of_cols)
        self.cols_possible = self.create_possibilities(COLS_VALUES, self.no_of_rows)
        #[[[1, 1, 1, -1, -1], ...], ...]]
        #step 2: order by the easiest(minimum possibilites(ways), 1 is the best)
        self.no_of_ways_rows = self.all_no_ways(self.rows_possible, True)
        self.no_of_ways_cols = self.all_no_ways(self.cols_possible, False)
        self.ordered_ascending_ways = sorted(self.no_of_ways_rows + self.no_of_ways_cols, key = lambda element: element[1])
        #[(4, 1, True), ..., (2, 3, False), ...]
        #step 3: fill in board with the easiest to the hardest
        while not self.solved:
            for ind1, _, row_check in self.ordered_ascending_ways:
                if not self.check_done(row_check, ind1):
                    if row_check:
                        values = self.rows_possible[ind1]
                    else:
                        values = self.cols_possible[ind1]
                    res_surely = self.get_only_one_option(values)
                    #[(2,1)] or [(3,-1)] or [(...), (...), ...]
                    for ind2, val in res_surely:
                        if row_check:
                            ri, ci = ind1, ind2
                        else:
                            ci, ri = ind1, ind2
                        if self.board[ri][ci] == 0:
                            self.board[ri][ci] = val
                            if row_check:
                                self.cols_possible[ci] = self.remove_possibilities(self.cols_possible[ci], ri, val)
                            else:
                                self.rows_possible[ri] = self.remove_possibilities(self.rows_possible[ri], ci, val)
                            clear_output(wait=True)
                            self.display_board()
                    self.update_done(row_check, ind1)
                self.check_solved()
    def create_possibilities(self, values, no_of_other):
        possibilities = []
        for v in values:
            groups = len(v)
            no_empty = no_of_other-sum(v)-groups+1
            ones = [[1]*x for x in v]
            res = self._create_possibilities(no_empty, groups, ones)
            possibilities.append(res)  
        return possibilities
    def _create_possibilities(self, no_empty, groups, ones):
        res_opts = []
        for p in combinations(range(groups+no_empty), groups):
            selected = [-1]*(groups+no_empty)
            ones_ind = 0
            for val in p:
                selected[val] = ones_ind
                ones_ind += 1
            res_opt = [ones[val]+[-1] if val > -1 else [-1] for val in selected]
            res_opt = [item for sublist in res_opt for item in sublist][:-1]
            res_opts.append(res_opt)
        return res_opts
    def all_no_ways(self, possibilities, row_check):
        s = [len(i) for i in possibilities]
        if row_check:
            return [(i, n, row_check) for i, n in enumerate(s) if self.rows_done[i] == 0]
        else:
            return [(i, n, row_check) for i, n in enumerate(s) if self.cols_done[i] == 0]
    def get_only_one_option(self, values):
        return [(n, np.unique(i)[0]) for n, i in enumerate(np.array(values).T) if len(np.unique(i)) == 1]
    def remove_possibilities(self, possibilities, i, val):
        return [p for p in possibilities if p[i] == val]
    def update_done(self, row_check, ind):
        if row_check:
            vals = self.board[ind]
        else: 
            vals = [row[ind] for row in self.board]
        if 0 not in vals:
            if row_check: 
                self.rows_done[ind] = 1
            else: 
                self.cols_done[ind] = 1 
    def check_done(self, row_check, ind):
        if row_check: 
            return self.rows_done[ind]
        else: 
            return self.cols_done[ind]
    def check_solved(self):
        if 0 not in self.rows_done and 0 not in self.cols_done:
            self.solved = True
    def display_board(self):
        plt.imshow(self.board, cmap='pink_r')
        plt.axis('off')
        plt.show()
        
Nonogram([[1, 1, 8],
 [1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1],
 [1, 2, 1, 1],
 [1, 1, 1, 1],
 [6],
 [4],
 [4],
 [2, 2],
 [15],
 [13, 3],
 [1, 2, 2, 2],
 [4, 5, 4],
 [4, 4, 2, 4],
 [4, 5, 1, 4],
 [4, 7, 4],
 [4, 7, 4],
 [4, 5, 4],
 [5, 5],
 [15]], [[1, 1, 9],
 [1, 2, 8],
 [1, 1, 2, 8],
 [12],
 [4, 2],
 [2, 4, 1],
 [2, 6, 1],
 [2, 6, 1],
 [5, 2, 6, 1],
 [1, 1, 2, 1, 4, 1],
 [1, 3, 2, 2, 3, 1],
 [1, 6, 4, 1],
 [1, 1, 7, 2],
 [1, 2, 3, 1, 9],
 [1, 1, 2, 8],
 [5, 11],
 [9],
 [1, 1],
 [1],
 [1, 1]]).board
 #WORK QUITE GOOD, 20x20 within a second, but no working with mutilple cases