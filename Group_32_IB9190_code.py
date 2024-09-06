#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 17:00:42 2024

@author: group_32
"""
from pyomo.environ import *
import pandas as pd
import numpy as np

#Reading the excel from the prepared excel 
file_name = "DataPreparation.xlsx"
dftc = pd.read_excel(file_name, "Sheet1", index_col=0)
dfsc = pd.read_excel(file_name, "Sheet2", index_col=0)


#Extracting the class names and student ids if needed 
class_names = dfsc.loc[dfsc.index[0], dfsc.columns[1:]].keys()
studentid =  dfsc.loc[dfsc.index[0:], dfsc.columns[0]].keys()

#Converting the student class dataframe to numpy array
dfsc_np = dfsc.to_numpy()
sc = dfsc_np[ 0:, 1:]

#Converting the time class dataframe to numpy array
dftc_np = dftc.to_numpy()
tc = dftc_np[ 4: , 2:]


roomcapacity =  dftc_np[ 3 , 2:]
excessroomcapacity = 96
time =  dftc_np[ 4:  , 1]


#Different parameters that can be changed 
social_dist_param = 2
M = 2
lamda = 0.5
myu = 0.2
bigV = 10000

# social_cap = np.ceil(roomcapacity / 11)
# numclasses = 2
# timelength = 20
# numstudents = 60


E = np.ceil(excessroomcapacity / social_dist_param)
social_cap = np.ceil(roomcapacity / social_dist_param )
numclasses = len(class_names)
timelength = len(time)
numstudents = len(studentid)


model = ConcreteModel()

#Defining the decision variables
model.x = Var(range(numstudents),range(M), domain=Binary)

#Defining the auxiliary variables as needed
model.TE = Var(range(numclasses),range(M), domain=NonNegativeReals)
model.TD = Var(range(numclasses),range(M), domain=NonNegativeReals)
model.sjt = Var(range(timelength), range(M), domain=NonNegativeReals)
model.s = Var(domain=NonNegativeReals)



#Defining the objective
def model_objective(model):
    TE = sum(model.TE[k, j] for k in range(numclasses) for j in range(M))
    TD = sum(model.TD[k,j] for k in range(numclasses) for j in range(M) )
    return (TE + lamda*TD + model.s )

model.obj = Objective(rule=model_objective, sense=minimize)

#Defining the rule for one student belonging to only one group
def onestudent_onegroup_rule(model, i):
    return (sum(model.x[i,j] for j in range(M)) == 1)

model.studentgroup = Constraint(range(numstudents), rule=onestudent_onegroup_rule)    


#constraints for the auxiliary variable for total excess
def TEcons(model, k, j):
    sum1 = 0
    sum2 = 0
    for i in range(numstudents):
        if(sc[i,k] == 1):
            sum2 += model.x[i,j]
    sum1 += (sum2 - social_cap[k]) 
    return(model.TE[k, j] >= sum1)

model.teconstraint = Constraint(range(numclasses), range(M), rule=TEcons)

# Constraints for the auxiliary variable for total deviation to get the absolute value when its positive
def TDconspos(model, k, j):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for i in range(numstudents):
        if(sc[i,k] == 1):
            sum1 += model.x[i,j]
            sum2 += sc[i,k]
    sum3 += sum1 - sum2/M        
    return(model.TD[k, j] >= sum3)

model.tdconstraintpos = Constraint(range(numclasses), range(M), rule=TDconspos)


# Constraints for the auxiliary variable for total deviation to get the absolute value when its negative 
def TDconsneg(model, k, j):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for i in range(numstudents):
        if(sc[i,k] == 1):
            sum1 += model.x[i,j]
            sum2 += sc[i,k]
    sum3 += sum1 - sum2/M         
       
    return(-1*model.TD[k, j] <= sum3)

model.tdconstraintneg = Constraint(range(numclasses), range(M), rule=TDconsneg)

# Constraints for the auxiliary variable for simultaneous excess
def sjtcons(model, t, j):
    sum1 = 0
    sum2 = 0
    for k in range(numclasses):
        if(tc[t, k] == 1):
            for i in range(numstudents):
                if(sc[i,k] == 1):
                    sum2 += model.x[i,j]
            sum1 += (sum2 - social_cap[k])
            sum2 = 0
    return ( model.sjt[t,j] >= sum1)

model.sjtconstraint = Constraint(range(timelength), range(M), rule=sjtcons)

# Constraints for the surplus simultaneous excess to be the max(SE - E)
def secons(model, t, j):
    return(model.s >= model.sjt[t, j] - E)

model.seconstraint = Constraint(range(timelength), range(M), rule=secons)



solver = SolverFactory('gurobi_direct')
results = solver.solve(model, tee=True)


if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    print('The minimised Objective is: ', model.obj())
 

if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    print("TE value is ", sum(model.TE[k, j]() for k in range(numclasses) for j in range(M)))
    print("TD value is ", sum(model.TD[k, j]() for k in range(numclasses) for j in range(M)))
    print("Surplus Simultaneous Excess is ", model.s())



if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    sumclass1 = [0] * M 
    for j in range(M):
        for i in range(numstudents):
            sumclass1[j] += model.x[i,j]()
        print("Number of students in group" , j+1 ,sumclass1[j])
        
        
# model.display()
