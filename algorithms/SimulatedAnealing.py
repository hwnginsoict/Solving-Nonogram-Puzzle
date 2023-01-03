import sys
import math
import random
import copy
import matplotlib.pyplot as plt 

num = 0

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


#m, n, row_list, col_list = ip()
board = [[-1 for j in range(n)] for i in range(m)]
all_pos = [((x-1)//n, (x-1)%n) for x in range(n*m)]
s = [[0 for k in range(len(row_list[i]))] for i in range(m)]
e = [[0 for k in range(len(row_list[i]))] for i in range(m)]

def diff(cur, goal):
    #Manhattan distance
    x = copy.copy(cur)
    y = copy.copy(goal)
    ret = d = 0
    while len(x) < len(y):
        x.append(0)
        d += 1
    while len(y) < len(x):
        y.append(0)
        d += 1
    for i in range(len(x)):
        ret += abs(x[i]-y[i])
    DifVal = 0
    return ret + DifVal*d

    # #Euclidean distance
    # x = copy.copy(cur)
    # y = copy.copy(goal)
    # ret = d = 0
    # while len(x) < len(y):
    #     x.append(0)
    #     d += 1
    # while len(y) < len(x):
    #     y.append(0)
    #     d += 1
    # for i in range(len(x)):
    #     ret += (x[i]-y[i])**2
    # DifVal = 1
    # return ret**0.5

def cost(bboard):
    ret = 0
    for i in range(m):
        seq = []
        for j in range(n):
            if bboard[i][j] == 1:
                if j == 0 or bboard[i][j-1] == -1:
                    seq.append(0)
                seq[len(seq)-1] += 1
        goal = row_list[i]
        ret += diff(seq,goal)
    for j in range(n):
        seq = []
        for i in range(m):
            if bboard[i][j] == 1:
                if i==0 or bboard[i-1][j] == -1:
                    seq.append(0)
                seq[len(seq)-1] += 1
        goal = col_list[j]
        ret += diff(seq,goal)
    return ret

def better(y, x, T):
    probability = random.random()
    #print(probability)
    if y <= x or math.exp(-(y-x)/T) >= probability:
        return True 
    return False

def initial(board):
    #create the first state

    #first state 1: a random board with equally chance of any cell being 1 and -1
    for i in range(m):
        for j in range(n):
            board[i][j] = 1 if random.random() > 0.5 else -1

    # #first state 2: a random board with the right number of black and blank cell
    # global num
    # random.shuffle(all_pos)
    # for h in range(n*m):
    #     (i, j) = all_pos[h]
    #     board[i][j] = 1 if h < num else -1

    # #first state 3: a random board with row constraint satisfied
    # bound = [[0 for k in range(len(row_list[i]))] for i in range(m)]
    # for i in range(m):
    #     end = n+1
    #     for k in range(len(row_list[i])-1, -1, -1):
    #         end -= row_list[i][k]+1
    #         bound[i][k] = end
    #     start = 0
    #     for k in range(len(row_list[i])):
    #         s[i][k] = random.randint(start, bound[i][k])
    #         e[i][k] = s[i][k] + row_list[i][k] - 1
    #         for j in range(s[i][k], e[i][k]+1):
    #             board[i][j] = 1
    #         start = e[i][k]+2

def next(T):
    #neighbor 1: a random cell value is changed
    global board, currcost
    neighbor = copy.deepcopy(board)
    rr = random.randint(0, m-1)
    cr = random.randint(0, n-1)
    neighbor[rr][cr] *= -1 #the cell state is flipped

    newcost = cost(neighbor)
    #print(currcost, newcost, T)
    if newcost == 0:
        op(neighbor)
    if better(newcost, currcost, T):
        board = neighbor
        currcost = newcost
        #print('!')

    # #neighbor 2: swap a random black cell with a random white cell
    # global board, currcost
    # neighbor = copy.deepcopy(board)
    # black = random.randint(0, num-1)
    # white = random.randint(num, n*m-1)
    # (ib, jb) = all_pos[black]
    # (iw, jw) = all_pos[white]
    # neighbor[ib][jb] = -1
    # neighbor[iw][jw] = 1

    # newcost=cost(neighbor)
    # print(currcost, newcost, T)
    # if newcost == 0:
    #     op(neighbor)
    # if better(newcost,currcost,T):
    #     board = neighbor
    #     all_pos[black], all_pos[white] = all_pos[white], all_pos[black]
    #     currcost = newcost
    #     #print('!')

    # #neighbor 3: a random black block shift to the left or the right
    # rr = random.randint(0, m-1)
    # ir = random.randint(0, len(row_list[rr])-1)

    # l = 0
    # r = n - row_list[rr][ir]
    # if ir > 0:
    #     l = e[rr][ir-1] + 2
    # if ir < len(row_list[rr])-1:
    #     r = s[rr][ir+1] - row_list[rr][ir] - 1
    # if l == r:
    #     return
    # newl = random.randint(l,r)
    # newr = newl + row_list[rr][ir] - 1
    # for j in range(newl, s[rr][ir]):
    #     neighbor[rr][j] = 1
    # for j in range(s[rr][ir], newl):
    #     neighbor[rr][j] = -1
    # for j in range(e[rr][ir]+1, newr+1):
    #     neighbor[rr][ir] = 1
    # for j in range(newr+1, e[rr][ir]+1):
    #     neighbor[rr][ir] = -1
    # mr = random.choice([-1, 1])

    # # newl = l = s[rr][ir]
    # # newr = r = e[rr][ir]
    # # if mr == -1:
    # #     if l == 1 or (l > 0 and neighbor[rr][l-2] == 0):
    # #         neighbor[rr][l-1] = 1
    # #         neighbor[rr][r] = -1
    # #         newl -= 1
    # #         newr -= 1
    # #     else:
    # #         return
    # # elif mr == 1:
    # #     if r == len(neighbor[rr])-1 or (r < len(neighbor[rr])-2 and neighbor[rr][r+2]==0):
    # #         neighbor[rr][r+1] = 1
    # #         neighbor[rr][l] = -1
    # #         newl += 1
    # #         newr += 1
    # #     else:
    # #         return

    # newcost = cost(neighbor)
    # #print(currcost, newcost, T)
    # if newcost == 0:
    #     op(neighbor)
    # if better(newcost,currcost,T):
    #     board = neighbor
    #     s[rr][ir] = newl
    #     e[rr][ir] = newr
    #     currcost = newcost
    #     #print('!')

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

def op(board):
    display_board(board)
    sys.exit(0)
def display_board(board):
    plt.imshow(board, cmap='pink_r')
    plt.axis('off')
    plt.show()


def anneal(MaxOperation,currcost):
    # #Logarithmic Cooling
    # c = 100
    # for t in range(MaxOperation):
    #     T = c/(math.log(1+c))
    
    # #Geometrical Cooling
    # T = 100000
    # CoolingRate = 0.05
    # for t in range(MaxOperation):
    #     T *= (1-CoolingRate)
    #     next(T)

    #Linear Cooling
    for t in range(MaxOperation):
        T = 1 - (t/MaxOperation)
        next(T)

count = 0
while True:
    count += 1
    initial(board)
    currcost = cost(board)
    MaxOperation = 10000
    anneal(MaxOperation, currcost)

    if check(board):
        op(board)