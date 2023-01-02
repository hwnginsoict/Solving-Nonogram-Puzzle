# import time
# start_time = time.time()

import sys
import math
import copy
import matplotlib.pyplot as plt
from IPython.display import clear_output

#define display
def display_board(board):
    plt.imshow(board, cmap='pink_r')
    plt.axis('off')
    plt.show()

#input
import copy
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
# print(row_list)
# print(col_list)

def inp():
  [m, n] = [int(x) for x in input().split()]
  row_list = [[int(x) for x in input().split()] for i in range(m)]
  col_list = [[int(x) for x in input().split()] for i in range(n)]
  return m, n, row_list, col_list

# m, n, row_list, col_list = inp()
board = [[0 for j in range(n)] for i in range(m)]    
bound = [[[[
           0 if k == 0 else sum(row_list[i][:k]) + k, n if k == \
           len(row_list[i]) else (n-1) - sum(row_list[i][k+1:]) - \
           (len(row_list[i])-k-1)
           ] for k in range(len(row_list[i]))
          ] for i in range(m)
         ], 
         [[[
           0 if k == 0 else sum(col_list[j][:k]) + k, m if k == \
           len(col_list[j]) else (m-1) - sum(col_list[j][k+1:]) - \
           (len(col_list[j])-k-1)
           ] for k in range(len(col_list[j]))
          ] for j in range(n)
         ]
        ]

def logical(board,bound):
  change = True
  while change:
    change =  False
    
    #display
    clear_output(wait=True)
    display_board(board)
    
    #check rows
    for i in range(m):
      for k in range(len(row_list[i])):
        previous_end = -1 if k == 0 else bound[0][i][k-1][1]
        forward_start = n if k == len(row_list[i])-1 else bound[0][i][k+1][0]
        #rule 2.1: block range must be strictly one after another
        if k > 0:
          if bound[0][i][k-1][0]+row_list[i][k-1]+1 > bound[0][i][k][0]:
            bound[0][i][k][0] = bound[0][i][k-1][0]+row_list[i][k-1]+1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
            change = True
        if k < len(row_list[i])-1:
          if bound[0][i][k+1][1]-row_list[i][k+1]-1 < bound[0][i][k][1]:
            bound[0][i][k][1] = bound[0][i][k+1][1]-row_list[i][k+1]-1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
            change = True
        
        #rule 2.2: the first/last cell of a black run range becomes out of range
        if bound[0][i][k][0] > 0 and board[i][bound[0][i][k][0]-1] == 1:
          bound[0][i][k][0] += 1
          if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
          change = True
        if bound[0][i][k][1] < n-1 and board[i][bound[0][i][k][1]+1] == 1:
          bound[0][i][k][1] -= 1
          if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
          change = True
        
        #rule 1.1: overlapping: using a black range to fill cells in the middle
        for j in range(bound[0][i][k][1]-row_list[i][k]+1, \
                       bound[0][i][k][0]+row_list[i][k]):
          if (j < bound[0][i][k][0] or j > bound[0][i][k][1]) or \
              board[i][j] == -1:
            return False
          elif board[i][j] == 0:           
            board[i][j] = 1
            change = True
        
        #rule 3.1: color cells between 2 black cells out of the previous and behind black range and update current black range
        s = e = n
        for j in range(previous_end+1, forward_start):
          if board[i][j] == 1:
            s = j
            break
        if s != n:
          for j in range(forward_start-1, previous_end, -1):
            if board[i][j] == 1:
              e = j
              break
          for j in range(s+1, e):
            if board[i][j] == -1:
              return False
            elif board[i][j] == 0:            
              board[i][j] = 1
              change = True
          if e-row_list[i][k]+1 > bound[0][i][k][0]:
            bound[0][i][k][0] = e-row_list[i][k]+1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
            change = True
          if s+row_list[i][k]-1 < bound[0][i][k][1]:
            bound[0][i][k][1] = s+row_list[i][k]-1
            if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
              return False
            change = True
        
        #rule 3.2: handle too short segments in a block range
        unknown_seg=0
        for j in range(bound[0][i][k][0], bound[0][i][k][1]+2):
          if j == bound[0][i][k][1]+1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
              if j-unknown_seg > bound[0][i][k][0]:
                bound[0][i][k][0] = j-unknown_seg
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                  return False
                change = True
              break
            unknown_seg = 0
            continue
          unknown_seg += 1
        unknown_seg = 0
        for j in range(bound[0][i][k][1], bound[0][i][k][0]-2, -1):
          if j == bound[0][i][k][0]-1 or board[i][j] == -1:
            if unknown_seg >= row_list[i][k]:
              if j+unknown_seg < bound[0][i][k][1]:
                bound[0][i][k][1] = j+unknown_seg
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                  return False
                change = True
              break
            unknown_seg = 0
            continue
          unknown_seg += 1
        unknown_seg = 0
        for j in range(bound[0][i][k][0], bound[0][i][k][1]+2):
          if j == bound[0][i][k][1]+1 or board[i][j] == -1:
            if unknown_seg < row_list[i][k]:
              for jj in range(j-unknown_seg, j):
                if jj > previous_end and jj < forward_start:
                  if board[i][jj] == 1:
                    return False
                  if board[i][jj] == 0:
                    board[i][jj] = -1
                    change = True
            unknown_seg = 0
            continue
          unknown_seg += 1
        
        if bound[0][i][k][0] > previous_end:
          #rule 3.3.1: complete a black run with the first cell in range being 1 and update
          if board[i][bound[0][i][k][0]] == 1:
            for j in range(bound[0][i][k][0]+1, bound[0][i][k][0]+row_list[i][k]):
              if board[i][j] == -1:
                return False
              if board[i][j] == 0:
                board[i][j] = 1
                change = True
            if bound[0][i][k][0]+row_list[i][k]-1 < bound[0][i][k][1]:
              bound[0][i][k][1] = bound[0][i][k][0]+row_list[i][k]-1
              if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False
              change = True
            if k < len(row_list[i])-1:
              if bound[0][i][k][0]+row_list[i][k]+1 > bound[0][i][k+1][0]:
                bound[0][i][k+1][0] = bound[0][i][k][0]+row_list[i][k]+1
                if bound[0][i][k+1][1] - bound[0][i][k+1][0] + 1 < row_list[i][k+1]:
                  return False
                change = True
            if k > 0 and bound[0][i][k-1][1] == bound[0][i][k][0]-1:
              bound[0][i][k-1][1] -= 1
              if bound[0][i][k-1][1] - bound[0][i][k-1][0] + 1 < row_list[i][k-1]:
                return False
              change = True
          
          #rule 3.3.2: update a block range if it's restricted by a blank cell
          #rule 3.3.3: restrict a block range when it includes some black segments
          first_black = -1
          seg_len = 0
          for j in range(bound[0][i][k][0], bound[0][i][k][1]+1):
            if board[i][j] == 1:
              seg_len += 1
              if first_black < 0:
                first_black = j              
              if j == bound[0][i][k][1] or board[i][j+1] != 1:
                if j-first_black+1 > row_list[i][k]:
                  if j-seg_len-1 < bound[0][i][k][1]:
                    bound[0][i][k][1] = j-seg_len-1
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                      return False
                    change = True
                  break
                seg_len = 0
            elif board[i][j] == -1 and first_black >= 0:
              if j-1 < bound[0][i][k][1]:
                bound[0][i][k][1] = j-1
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                  return False
                change = True
              break

        if bound[0][i][k][1] < forward_start:
          #rule 3.3.1: complete a black run with the last cell in range being 1 and update
          if board[i][bound[0][i][k][1]] == 1:
            for j in range(bound[0][i][k][1]-1, bound[0][i][k][1]-row_list[i][k], -1):
              if board[i][j] == -1:
                return False
              if board[i][j] == 0:
                board[i][j] = 1
                change = True
            if bound[0][i][k][1]-row_list[i][k]+1 > bound[0][i][k][0]:
              bound[0][i][k][0] = bound[0][i][k][1]-row_list[i][k]+1
              if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                return False
              change = True
            if k > 0:
              if bound[0][i][k][1]-row_list[i][k]-1 < bound[0][i][k-1][1]:
                bound[0][i][k-1][1] = bound[0][i][k][1]-row_list[i][k]-1
                if bound[0][i][k-1][1] - bound[0][i][k-1][0] + 1 < row_list[i][k-1]:
                  return False
                change = True
            if k < len(row_list[i])-1 and bound[0][i][k+1][0] == bound[0][i][k][1]+1:
              bound[0][i][k+1][0] += 1
              if bound[0][i][k+1][1] - bound[0][i][k+1][0] + 1 < row_list[i][k+1]:
                return False
              change = True
          
          #rule 3.3.2: update a block range if it's restricted by a blank cell
          #rule 3.3.3: restrict a block range when it includes some black segments
          first_black = n
          seg_len = 0
          for j in range(bound[0][i][k][1], bound[0][i][k][0]-1):
            if board[i][j] == 1:
              seg_len += 1
              if first_black > n:
                first_black = j              
              if j == bound[0][i][k][0] or board[i][j-1] != 1:
                if first_black-j+1 > row_list[i][k]:
                  if j+seg_len+1 > bound[0][i][k][0]:
                    bound[0][i][k][0] = j+seg_len+1
                    if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                      return False
                    change = True
                  break
            elif board[i][j] == -1 and first_black < n:
              if j+1 > bound[0][i][k][0]:
                bound[0][i][k][0] = j+1
                if bound[0][i][k][1] - bound[0][i][k][0] + 1 < row_list[i][k]:
                  return False
                change = True
              break
            
        #rule 1.1: overlapping: using a black range to fill cells in the middle
        for j in range(bound[0][i][k][1]-row_list[i][k]+1, \
                       bound[0][i][k][0]+row_list[i][k]):
          if (j < bound[0][i][k][0] or j > bound[0][i][k][1]) or \
              board[i][j] == -1:
            return False
          elif board[i][j] == 0:            
            board[i][j] = 1
            change = True

      fb = 0
      lb = -1
      seg = 0
      last_blank = -1
      for j in range(n):
        #rule 1.3: all current black runs have size 1 at the start of a block range
        if lb < len(row_list[i])-1 and j == bound[0][i][lb+1][0]:
          if board[i][j] == 1:
            if j>0:
              check1_3 = True
              for k in range(fb, lb+1):
                if row_list[i][k] != 1:
                  check1_3 = False
                  break
              if check1_3:
                if board[i][j-1] == 1:
                  return False
                elif board[i][j-1] == 0:
                  board[i][j-1] = -1
                  change = True
          lb += 1

        min_run = n if fb <= lb else 0
        max_run = 0
        for k in range(fb, lb+1):
          min_run = min(min_run, row_list[i][k])
          max_run = max(max_run, row_list[i][k])

        if board[i][j] == -1:
          last_blank = j

        if board[i][j] == 1:          
          #rule 1.5.1-3: an blank cell acts as a wall causing overlapping(1.1)
          blank_ahead = [n, True]
          for jj in range(j+1, min(n, j+min_run)):
            if jj < last_blank+min_run:
              if board[i][jj] == -1:
                return False
              elif board[i][jj] == 0:
                board[i][jj] = 1
                change = True
            else:
              if not blank_ahead[1]:
                break
            if board[i][jj] == -1 and blank_ahead[1]:
              blank_ahead[0] = jj
              blank_ahead[1] = False
              if jj >= last_blank+min_run:
                break
          for jj in range(j-1, blank_ahead[0]-min_run-1, -1):
            if board[i][jj] == -1:
                return False
            elif board[i][jj] == 0:
              board[i][jj] = 1
              change = True
          
          seg += 1
          if j == n-1 or board[i][j+1] != 1:
            #rule 1.5.4: 2 blank cells at 2 endpoints of a black segment if all blocks in range have following equal length 
            if min_run == max_run and min_run == seg:
              if j-seg >= 0:
                if board[i][j-seg] == 1:
                  return False
                elif board[i][j-seg] == 0:
                  board[i][j-seg] = -1
                  change = True
              if j+1 < n:
                if board[i][j+1] == 1:
                  return False
                elif board[i][j+1] == 0:
                  board[i][j+1] = -1
                  change = True

            #rule 2.3: update block range to the front/back of a black segment
            for k in range(fb, lb+1):
              if row_list[i][k] >= seg:
                for kk in range(fb, k):
                  if j-seg-1 < bound[0][i][kk][1]:
                    bound[0][i][kk][1] = j-seg-1
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                      return False
                    change = True
                break
            for k in range(lb, fb-1, -1):
              if row_list[i][k] >= seg:
                for kk in range(lb, k, -1):
                  if j+2 > bound[0][i][kk][0]:
                    bound[0][i][kk][0] = j+2
                    if bound[0][i][kk][1] - bound[0][i][kk][0] + 1 < row_list[i][kk]:
                      return False
                    change = True
                break
            seg = 0

        #rule 1.2+1.4: if this cell being 1 create a bigger black run than all possiible ones then it has to be -1
        if board[i][j] != 1:
          l = j
          while l > 0 and board[i][l-1] == 1:
            l -= 1
          r = j
          while r < n-1 and board[i][r+1] == 1:
            r += 1
          if r-l+1 > max_run:
            if board[i][j] == 1:
              return False
            if board[i][j] == 0:
              board[i][j] = -1
              change = True

        #rule 1.3: all current black runs have size 1 at the end of a block range
        if fb < len(row_list[i]) and j == bound[0][i][fb][1]:
          fb+=1
          if board[i][j] == 1:
            if j < n-1:
              check1_3 = True
              for k in range(fb, lb+1):
                if row_list[i][k] != 1:
                  check1_3 = False
                  break
              if check1_3:
                if board[i][j+1] == 1:
                  return False
                elif board[i][j+1] == 0:
                  board[i][j+1] = -1
                  change = True

    #check columns
    for j in range(n):
      for k in range(len(col_list[j])):
        previous_end = -1 if k == 0 else bound[1][j][k-1][1]
        forward_start = m if k == len(col_list[j])-1 else bound[1][j][k+1][0]
        #rule 2.1: block range must be strictly one after another
        if k > 0:
          if bound[1][j][k-1][0]+col_list[j][k-1]+1 > bound[1][j][k][0]:
            bound[1][j][k][0] = bound[1][j][k-1][0]+col_list[j][k-1]+1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
              return False
            change = True
        if k < len(col_list[j])-1:
          if bound[1][j][k+1][1]-col_list[j][k+1]-1 < bound[1][j][k][1]:
            bound[1][j][k][1] = bound[1][j][k+1][1]-col_list[j][k+1]-1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
              return False
            change = True
        
        #rule 2.2: the first/last cell of a black run range becomes out of range
        if bound[1][j][k][0] > 0 and board[bound[1][j][k][0]-1][j] == 1:
          bound[1][j][k][0] += 1
          if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False
          change = True
        if bound[1][j][k][1] < m-1 and board[bound[1][j][k][1]+1][j] == 1:
          bound[1][j][k][1] -= 1
          if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
            return False
          change = True
        
        #rule 1.1: overlapping: using a black range to fill cells in the middle
        for i in range(bound[1][j][k][1]-col_list[j][k]+1, \
                       bound[1][j][k][0]+col_list[j][k]):
          if (i < bound[1][j][k][0] or i > bound[1][j][k][1]) and \
              board[i][j] == -1:
            return False
          elif board[i][j] == 0:
            board[i][j] = 1
            change = True
        
        #rule 3.1: color cells between 2 black cells out of the previous and behind black range and update current black range
        s = e = m
        for i in range(previous_end+1, forward_start):
          if board[i][j] == 1:
            s = i
            break
        if s != m:
          for i in range(forward_start-1, previous_end, -1):
            if board[i][j] == 1:
              e = i
              break
          for i in range(s+1, e):
            if board[i][j] == -1: #or not check_row(board, i, j, 1):
              print(14)
              return False
            elif board[i][j] == 0:
              board[i][j] = 1
              change = True
          if e-col_list[j][k]+1 > bound[1][j][k][0]:
            bound[1][j][k][0] = e-col_list[j][k]+1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
              return False
            change = True
          if s+col_list[j][k]-1 < bound[1][j][k][1]:
            bound[1][j][k][1] = s+col_list[j][k]-1
            if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
              return False
            change = True
        
        #rule 3.2: handle too short segments in a block range
        unknown_seg=0
        for i in range(bound[1][j][k][0], bound[1][j][k][1]+2):
          if i == bound[1][j][k][1]+1 or board[i][j] == -1:
            if unknown_seg >= col_list[j][k]:
              if i-unknown_seg > bound[1][j][k][0]:
                bound[1][j][k][0] = i-unknown_seg
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                  return False
                change = True
              break
            unknown_seg = 0
            continue
          unknown_seg += 1
        unknown_seg = 0
        for i in range(bound[1][j][k][1], bound[1][j][k][0]-2, -1):
          if i == bound[1][j][k][0]-1 or board[i][j] == -1:
            if unknown_seg >= col_list[j][k]:
              if i+unknown_seg < bound[1][j][k][1]:
                bound[1][j][k][1] = i+unknown_seg
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                  return False
                change = True
              break
            unknown_seg = 0
            continue
          unknown_seg += 1
        unknown_seg = 0
        for i in range(bound[1][j][k][0], bound[1][j][k][1]+2):
          if i == bound[1][j][k][1]+1 or board[i][j] == -1:
            if unknown_seg < col_list[j][k]:
              for ii in range(i-unknown_seg, i):
                if ii > previous_end and ii < forward_start:
                  if board[ii][j] == 1:
                    return False
                  if board[ii][j] == 0:
                    board[ii][j] = -1
                    change = True
            unknown_seg = 0
            continue
          unknown_seg += 1  
        
        if bound[1][j][k][0] > previous_end:
          #rule 3.3.1: complete a black run with the first cell in range being 1 and update
          if board[bound[1][j][k][0]][j] == 1:
            for i in range(bound[1][j][k][0]+1, bound[1][j][k][0]+col_list[j][k]):
              if board[i][j] == -1:
                return False
              if board[i][j] == 0:
                board[i][j] = 1
                change = True
            if bound[1][j][k][0]+col_list[j][k]-1 < bound[1][j][k][1]:
              bound[1][j][k][1] = bound[1][j][k][0]+col_list[j][k]-1
              if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False
              change = True
            if k < len(col_list[j])-1:
              if bound[1][j][k][0]+col_list[j][k]+1 > bound[1][j][k+1][0]:
                bound[1][j][k+1][0] = bound[1][j][k][0]+col_list[j][k]+1
                if bound[1][j][k+1][1] - bound[1][j][k+1][0] + 1 < col_list[j][k+1]:
                  return False
                change = True
            if k > 0 and bound[1][j][k-1][1] == bound[1][j][k][0]-1:
              bound[1][j][k-1][1] -= 1
              if bound[1][j][k-1][1] - bound[1][j][k-1][0] + 1 < col_list[j][k-1]:
                return False
              change = True
          
          #rule 3.3.2: update a block range if it's restricted by a blank cell
          #rule 3.3.3: restrict a block range when it includes some black segments
          first_black = -1
          seg_len = 0
          for i in range(bound[1][j][k][0], bound[1][j][k][1]+1):
            if board[i][j] == 1:
              seg_len += 1
              if first_black < 0:
                first_black = i              
              if i == bound[1][j][k][1] or board[i+1][j] != 1:
                if i-first_black+1 > col_list[j][k]:
                  if i-seg_len-1 < bound[1][j][k][1]:
                    bound[1][j][k][1] = i-seg_len-1
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                      return False
                    change = True
                  break
                seg_len = 0
            elif board[i][j] == -1 and first_black >= 0:
              if i-1 < bound[1][j][k][1]:
                bound[1][j][k][1] = i-1
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                  return False
                change = True
              break

        if bound[1][j][k][1] < forward_start:
          #rule 3.3.1: complete a black run with the last cell in range being 1 and update
          if board[bound[1][j][k][1]][j] == 1:
            for i in range(bound[1][j][k][1]-1, bound[1][j][k][1]-col_list[j][k], -1):
              if board[i][j] == -1:
                return False
              if board[i][j] == 0:
                board[i][j] = 1
                change = True
            if bound[1][j][k][1]-col_list[j][k]+1 > bound[1][j][k][0]:
              bound[1][j][k][0] = bound[1][j][k][1]-col_list[j][k]+1
              if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                return False
              change = True
            if k > 0:
              if bound[1][j][k][1]-col_list[j][k]-1 < bound[1][j][k-1][1]:
                bound[1][j][k-1][1] = bound[1][j][k][1]-col_list[j][k]-1
                if bound[1][j][k-1][1] - bound[1][j][k-1][0] + 1 < col_list[j][k-1]:
                  return False
                change = True
            if k < len(col_list[j])-1 and bound[1][j][k+1][0] == bound[1][j][k][1]+1:
              bound[1][j][k+1][0] += 1
              if bound[1][j][k+1][1] - bound[1][j][k+1][0] + 1 < col_list[j][k+1]:
                return False
              change = True
          
          #rule 3.3.2: update a block range if it's restricted by a blank cell
          #rule 3.3.3: restrict a block range when it includes some black segments
          first_black = m
          seg_len = 0
          for i in range(bound[1][j][k][1], bound[1][j][k][0]-1):
            if board[i][j] == 1:
              seg_len += 1
              if first_black > m:
                first_black = i              
              if i == bound[1][j][k][0] or board[i-1][j] != 1:
                if first_black-i+1 > col_list[j][k]:
                  if i+seg_len+1 > bound[1][j][k][0]:
                    bound[1][j][k][0] = i+seg_len+1
                    if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                      return False
                    change = True
                  break
            elif board[i][j] == -1 and first_black < m:
              if i+1 > bound[1][j][k][0]:
                bound[1][j][k][0] = i+1
                if bound[1][j][k][1] - bound[1][j][k][0] + 1 < col_list[j][k]:
                  return False
                change = True
              break
        
        #rule 1.1: overlapping: using a black range to fill cells in the middle
        for i in range(bound[1][j][k][1]-col_list[j][k]+1, \
                       bound[1][j][k][0]+col_list[j][k]):
          if (i < bound[1][j][k][0] or i > bound[1][j][k][1]) or \
              board[i][j] == -1:
            return False
          elif board[i][j] == 0:
            board[i][j] = 1
            change = True

      fb = 0
      lb = -1
      seg = 0
      last_blank = -1
      for i in range(m):
        #rule 1.3: all current black runs have size 1 at the start of a block range
        if lb < len(col_list[j])-1 and i == bound[1][j][lb+1][0]:
          if board[i][j] == 1:
            if i>0:
              check1_3 = True
              for k in range(fb, lb+1):
                if col_list[j][k] != 1:
                  check1_3 = False
                  break
              if check1_3:
                if board[i-1][j] == 1:
                  return False
                elif board[i-1][j] == 0:
                  board[i-1][j] = -1
                  change = True
          lb += 1

        min_run = m if lb >= fb else 0
        max_run = 0
        for k in range(fb, lb+1):
          min_run = min(min_run, col_list[j][k])
          max_run = max(max_run, col_list[j][k])

        if board[i][j] == -1:
          last_blank = i

        if board[i][j] == 1:          
          #rule 1.5.1-3: an blank cell acts as a wall causing overlapping(1.1)
          blank_ahead = [m, True]
          for ii in range(i+1, min(m, i+min_run)):
            if ii < last_blank+min_run:
              if board[ii][j] == -1:
                return False
              elif board[ii][j] == 0:
                board[ii][j] = 1
                change = True
            else:
              if not blank_ahead[1]:
                break
            if board[ii][j] == -1 and blank_ahead[1]:
              blank_ahead[0] = ii
              blank_ahead[1] = False
              if ii >= last_blank+min_run:
                break
          for ii in range(i-1, blank_ahead[0]-min_run-1, -1):
            if board[ii][j] == -1:
                return False
            elif board[ii][j] == 0:
              board[ii][j] = 1
              change = True
          
          seg += 1
          if i == m-1 or board[i+1][j] != 1:
            #rule 1.5.4: 2 blank cells at 2 endpoints of a black segment if all blocks in range have following equal length 
            if min_run == max_run and min_run == seg:
              if i-seg >= 0:
                if board[i-seg][j] == 1:
                  return False
                elif board[i-seg][j] == 0:
                  board[i-seg][j] = -1
                  change = True
              if i+1 < m:
                if board[i+1][j] == 1:
                  return False
                elif board[i+1][j] == 0:
                  board[i+1][j] = -1
                  change = True

            #rule 2.3: update block range to the front/back of a black segment
            for k in range(fb, lb+1):
              if col_list[j][k] >= seg:
                for kk in range(fb, k):
                  if i-seg-1 < bound[1][j][kk][1]:
                    bound[1][j][kk][1] = i-seg-1
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                      return False
                    change = True
                break
            for k in range(lb, fb-1, -1):
              if col_list[j][k] >= seg:
                for kk in range(lb, k, -1):
                  if i+2 > bound[1][j][kk][0]:
                    bound[1][j][kk][0] = i+2
                    if bound[1][j][kk][1] - bound[1][j][kk][0] + 1 < col_list[j][kk]:
                      return False
                    change = True
                break
            seg = 0

        #rule 1.2+1.4: if this cell being 1 create a bigger black run than all possiible ones then it has to be -1
        if board[i][j] != 1:
          l = i
          while l > 0 and board[l-1][j] == 1:
            l -= 1
          r = i
          while r < m-1 and board[r+1][j] == 1:
            r += 1
          if r-l+1 > max_run:
            if board[i][j] == 1:
              return False
            if board[i][j] == 0:
              board[i][j] = -1
              change = True

        #rule 1.3: all current black runs have size 1 at the end of a block range
        if fb < len(col_list[j]) and i == bound[1][j][fb][1]:
          fb+=1
          if board[i][j] == 1:
            if i < m-1:
              check1_3 = True
              for k in range(fb, lb+1):
                if col_list[j][k] != 1:
                  check1_3 = False
                  break
              if check1_3:
                if board[i+1][j] == 1:
                  return False
                elif board[i+1][j] == 0:
                  board[i+1][j] = -1
                  change = True
  return True  

def outp(board):
  for i in range(m):
    for j in range(n):
      if board[i][j] == 1:
        print('#', end='')
      elif board[i][j] == -1:
        print('.', end='')
    print()

def check(board):
    for j in range(n):
        i=r=0
        while (i<m):
            if board[i][j]==-1:
                i+=1
            else:
                if r>=len(col_list[j]) or i+col_list[j][r]>m:
                    return False
                for k in range(col_list[j][r]):
                    if board[i+k][j]!=1:
                        return False
                i+=col_list[j][r]
                if i<m:
                    if board[i][j]!=-1:
                        return False
                    i+=1
                r+=1
        if r<len(col_list[j]):
            return False
    for i in range(m):
        j=r=0
        while (j<n):
            if board[i][j]==-1:
                j+=1
            else:
                if r>=len(row_list[i]) or j+row_list[i][r]>n:
                    return False
                for k in range(row_list[i][r]):
                    if board[i][j+k]!=1:
                        return False
                j+=row_list[i][r]
                if j<n:
                    if board[i][j]!=-1:
                        return False
                    j+=1
                r+=1
        if r<len(row_list[i]):
            return False
    return True

def solution_found(board):
  global sol_count
  # outp(board)
  sol_count += 1

def backtrack(x, currboard, currbound):
  if not logical(currboard, currbound):
    return
  for i in range(m):
    for j in range(n):
      if currboard[i][j] == 0:
        newboard = copy.deepcopy(currboard)
        newbound = copy.deepcopy(currbound)
        newboard[i][j] = -1
        backtrack(x+1, newboard, newbound)
        newboard = copy.deepcopy(currboard)
        newbound = copy.deepcopy(currbound)
        newboard[i][j] = 1
        backtrack(x+1, newboard, newbound)
        return
  if check(currboard):
    solution_found(currboard)
sol_count = 0
backtrack(0, board, bound)
if sol_count == 0:
  print('the puzzle has no solution')
else:
  print(f'the puzzle has {sol_count} solution')

#display
# display_board(board)

# end_time = time.time()
# print("The time of execution of above program is :", (end_time-start_time) * 10**3, "ms")