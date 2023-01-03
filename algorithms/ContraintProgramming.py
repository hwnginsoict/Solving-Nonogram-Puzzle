#Constraint Programming
import numpy as np
with open('input.txt') as f:
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
    
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt 
from IPython.display import clear_output

def create_possibilities(values, no_of_other):
    possibilities = []
    for v in values:
        groups = len(v)
        no_empty = no_of_other-sum(v)-groups+1
        ones = [[1]*x for x in v]
        res = _create_possibilities(no_empty, groups, ones)
        possibilities.append(res)  
    return possibilities
def _create_possibilities(no_empty, groups, ones):
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
def all_no_ways(possibilities, row_check):
    s = [len(i) for i in possibilities]
    if row_check:
        return [(i, n, row_check) for i, n in enumerate(s) if rows_done[i] == 0]
    else:
        return [(i, n, row_check) for i, n in enumerate(s) if cols_done[i] == 0]
def get_only_one_option(values):
    return [(n, np.unique(i)[0]) for n, i in enumerate(np.array(values).T) if len(np.unique(i)) == 1]
def remove_possibilities(possibilities, i, val):
    return [p for p in possibilities if p[i] == val]
def update_done(row_check, ind, board):
    if row_check:
        vals = board[ind]
    else: 
        vals = [row[ind] for row in board]
    if 0 not in vals:
        if row_check: 
            rows_done[ind] = 1
        else: 
            cols_done[ind] = 1 
def check_done(row_check, ind):
    if row_check: 
        return rows_done[ind]
    else: 
        return cols_done[ind]
def check_solved(rows_done, cols_done):
    if 0 not in rows_done and 0 not in cols_done:
        global solved 
        solved = True 
    
def display_board(board):
    plt.imshow(board, cmap='pink_r')
    plt.axis('off')
    plt.show()

no_of_rows = len(row_list)
rows_done = [0] * no_of_rows

no_of_cols = len(col_list)
cols_done = [0] * no_of_cols

solved = False
board = [[0 for c in range(no_of_cols)] for r in range(no_of_rows)]

#step 1: define all possible solution 
rows_possible = create_possibilities(row_list, no_of_cols)
cols_possible = create_possibilities(col_list, no_of_rows)
#[[[1, 1, 1, -1, -1], ...], ...]]
#step 2: order by the easiest(minimum possibilites(ways), 1 is the best)
no_of_ways_rows = all_no_ways(rows_possible, True)
no_of_ways_cols = all_no_ways(cols_possible, False)
ordered_ascending_ways = sorted(no_of_ways_rows + no_of_ways_cols, key = lambda element: element[1])
#[(4, 1, True), ..., (2, 3, False), ...]
#step 3: fill in board with the easiest to the hardest
while not solved:
    for ind1, _, row_check in ordered_ascending_ways:
        if not check_done(row_check, ind1):
            if row_check:
                values = rows_possible[ind1]
            else:
                values = cols_possible[ind1]
            res_surely = get_only_one_option(values)
            #[(2,1)] or [(3,-1)] or [(...), (...), ...]
            for ind2, val in res_surely:
                if row_check:
                    ri, ci = ind1, ind2
                else:
                    ci, ri = ind1, ind2
                if board[ri][ci] == 0:
                    board[ri][ci] = val
                    if row_check:
                        cols_possible[ci] = remove_possibilities(cols_possible[ci], ri, val)
                    else:
                        rows_possible[ri] = remove_possibilities(rows_possible[ri], ci, val)
                    clear_output(wait=True)
                    display_board(board)
                update_done(row_check, ind1, board)
    check_solved(rows_done, cols_done)

