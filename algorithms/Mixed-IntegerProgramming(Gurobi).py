import gurobipy as gp
from gurobipy import GRB

with open("test.txt", "r") as f:
    Firstline=f.readline()
    Secondline=f.readline()
    Thirdline=f.readline()
    Fourthline=f.readline()
    Fifthline=f.readline()
N,A,C=list(map(int,Firstline.split()))
c=list(map(int,Secondline.split()))
a=list(map(int,Thirdline.split()))
f=list(map(int,Fourthline.split()))
m=list(map(int,Fifthline.split()))

# Create a new model
M = gp.Model()

M.Params.OutputFlag = 0

# Create variables
for i in range(N):
    n[i] = M.addVar(lb = m[i], vtype=GRB.SEMIINT, name="n"+str(i))
# Set objective function
M.setObjective(gp.quicksum(f[i]*n[i] for i in range(N)), GRB.MAXIMIZE)

# Add constraints
M.addConstr(gp.quicksum(a[i]*n[i] for i in range(N)) <= A)
M.addConstr(gp.quicksum(c[i]*n[i] for i in range(N)) <= C)

# Solve it!
M.optimize()

print('Optimized Sotion is: ' + str(list(n[i].X for i in range(N))))
print(f"With the profit is: {M.objVal}")
