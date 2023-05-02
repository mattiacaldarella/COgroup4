import numpy as np
import matplotlib.pyplot as plt
import ReadInstance
from problem import ProblemData, Request, Tool
from gurobipy import Model, GRB, quicksum


file = 'C:\\Users\\Mattia\\Desktop\\20 Instances CO2023\\challenge_r200d15_4.txt'
problem_data = ReadInstance.read_instance(file)

#def vehicle_routing(problem_data: ProblemData):
n = len(problem_data.coordinates) #number of clients

xc = []
for i in range(problem_data.number_of_coordinates):
    xc.append(problem_data.coordinates[i][1]) #vector of x-coordinates

yc = []
for i in range(problem_data.number_of_coordinates):
    yc.append(problem_data.coordinates[i][2]) #vector of y-coordinates

# plot of the routing problem
plt.plot(xc[0], yc[0], c='r', marker='s')#plotting depot
plt.scatter(xc[1:], yc[1:], c='b')#plotting client locations
#plt.show()

N = [i for i in range(1, problem_data.number_of_coordinates)] #vector of the clients
V = [0] + N #vector of vertices
A = [(i, j) for i in V for j in V if i!=j] #vector of arcs
c = {(i, j): np.floor(np.hypot(xc[i]-xc[j], yc[i]-yc[j])) for i,j in A} #Euclidean distance between node i and j
# Value of c incorrect??
Q = problem_data.capacity #vehicle capacity
q = {i: problem_data.requests[i].tools_needed} #amount of tools that have to be delivered



# creating the model
mdl = Model('CVRP')
x = mdl.addVars(A, vtype=GRB.BINARY)
u = mdl.addVars(N, vtype=GRB.CONTINUOUS)


mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[a]*c[a]*problem_data.distance_cost for a in A)) #minimize the sum of all arcs * cost of the arc, for all the arcs in A


# set the constraints, stil need to add more contraints
mdl.addConstrs(quicksum(x[i,j] for j in V if j!=i)==1 for i in N)
mdl.addConstrs(quicksum(x[i,j] for i in V if i!=j)==1 for j in N)
#mdl.addConstrs((x[i, j] == 1) >> (u[i]+q[j] == u[j])
#               for i, j in A if i != 0 and j != 0)
#mdl.addConstrs(u[i] >=q[i] for i in N)
#mdl.addConstrs(u[i] <=Q for i in N)

mdl.optimize() #run the model


# plot the solution
active_arcs = [a for a in A if x[a].x==1]
for i,j in active_arcs:
    plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g')
    plt.plot(xc[0], yc[0], c='r', marker='s')
    plt.scatter(xc[1:], yc[1:], c='b')
plt.show()