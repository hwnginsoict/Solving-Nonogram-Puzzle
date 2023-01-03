#DFS(Backtracking)

import matplotlib.pyplot as plt
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
exist=False
row_slot=[n-sum(row_list[i])+1 for i in range(m)]
board=[[-1 for j in range(n)] for i in range(m)]
it=cnt=0

def check(board): #check if the current board satisfy column constraints
    for j in range(n):
        i=r=0
        while(i<m):
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
    return True

def result():
      global board
#     for i in range(m):
#         print(*board[i])
      plt.imshow(board, cmap='pink_r')
      plt.axis('off')
      plt.show()
      global exist
      exist=True

def bt(x,y):
    global it,cnt
    if x>=m: #all cells have been filled
        if check(board):
            result()
            #quit()
        return
    if y>=row_slot[x]: #next line
        if x+1<m:
            cnt=0
            it=0
        bt(x+1,0)
        if x+1<m:
            cnt=len(row_list[x])
            it=n
    elif y+len(row_list[x])-cnt>=row_slot[x]: #the remaining cells of the row have to be 1
        for i in range(row_list[x][cnt]):
            board[x][it+i]=1
        it+=row_list[x][cnt]
        if cnt<len(row_list[x])-1:
            board[x][it]=-1
            it+=1
        cnt+=1
        bt(x,y+1)
        cnt-=1
        if cnt<len(row_list[x])-1:
            it-=1
        it-=row_list[x][cnt]
    elif cnt>=len(row_list[x]): #the remaining cells of the row have to be 0
        board[x][it]=-1
        it+=1
        bt(x,y+1)
        it-=1
    else:
        for i in range(2):
            board[x][it]=i*2-1
            it+=1
            if i==1:
                for j in range(row_list[x][cnt]-1):
                    board[x][it+j]=1
                it+=row_list[x][cnt]-1
                if cnt<len(row_list[x])-1:
                    board[x][it]=-1
                    it+=1
                cnt+=1
            bt(x,y+1)
            if i==1:
                cnt-=1
                if cnt<len(row_list[x])-1:
                    it-=1
                it-=row_list[x][cnt]-1
            it-=1

bt(0,0)
if not exist:
    print('No solution found')
