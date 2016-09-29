from math import sqrt
from time import time
from random import uniform
import numpy as np

def dart_simple(darts):
    in_circle = 0
    start = time()
    for i in range(darts):
        x,y = uniform(0,1),uniform(0,1)
        if sqrt((x-0.5)**2 + (y-0.5)**2) <= 0.5:
            in_circle +=1
    end = time()
    execution_time = end-start
    pi = (4*in_circle)/float(darts)
    #print("Darts: ", darts)
    #print("Execution time: ", execution_time)
    #print("Sim time (darts/sec): ", darts/float(execution_time))
    #print("Pi: ", pi)
    return execution_time

Darts = []
for x in range(9):
    Darts.append(10**x)
    
def simple(darts):
    simple_times = []
    simple_sim = []
    for d in darts:
        t = dart_simple(d)
        simple_sim.append(d/float(t))
        simple_times.append(t)
    return simple_times, simple_sim


from multiprocessing import Pool 
def multi(darts):
    multi_times = []
    multi_sim = []
    pool = Pool(processes=4)             
    for i,x in enumerate(pool.map(dart_simple, darts)):
        multi_times.append(x)
        multi_sim.append(darts[i]/float(x))
    pool.terminate()
    del pool
    return multi_times, multi_sim


import dask.bag as db
def dask(darts):
    dask_times = []
    dask_sim = []
    b = db.from_sequence(darts)
    for i,x in enumerate(b.map(dart_simple).compute()):
        dask_times.append(x)
        dask_sim.append(darts[i]/float(x))
    return dask_times,dask_sim

SIMPLE = []
SIMPLE_SIM = []
MULTI = []
MULTI_SIM = []
DASK = []
DASK_SIM = []
num = 10
for i in range(num):
    print("Running program %d/%d" % (i,num-1))
    simple_time, simple_sim = simple(Darts)
    SIMPLE.append(simple_time)
    SIMPLE_SIM.append(simple_sim)
    multi_times, multi_sim = multi(Darts)
    MULTI.append(multi_times)
    MULTI_SIM.append(multi_sim)
    dask_times, dask_sim = dask(Darts)
    DASK.append(dask_times)
    DASK_SIM.append(dask_sim)

#Calculate mean and std dev
simple_mean = np.mean(SIMPLE,axis=0)
simple_std = np.std(SIMPLE,axis=0)
simple_mean_sim = np.mean(SIMPLE_SIM,axis=0)
dask_mean = np.mean(DASK,axis=0)
dask_std = np.std(DASK,axis=0)
dask_mean_sim = np.mean(DASK_SIM,axis=0)
multi_mean = np.mean(MULTI,axis=0)
multi_std = np.std(MULTI,axis=0)
multi_mean_sim = np.mean(MULTI_SIM,axis=0)

    
print('##PLOTTING##')

import matplotlib.pyplot as plt
f, ax1 = plt.subplots() 
ax1.plot(Darts,simple_mean,'-',label='simple')
ax1.fill_between(Darts,simple_mean-simple_std,simple_mean+simple_std,facecolor='blue',alpha=0.5)
ax1.plot(Darts,multi_mean,'-',label='multi')
ax1.fill_between(Darts,multi_mean-multi_std,multi_mean+multi_std,facecolor='green',alpha=0.5)
ax1.plot(Darts,dask_mean,'-',label='dask')
ax1.fill_between(Darts,dask_mean-dask_std,dask_mean+dask_std,facecolor='red',alpha=0.5)
ax1.set_xlabel("Number of Darts Thrown")
ax1.set_ylabel("Execution Time (sec) - solid")
ax1.semilogx()
ax1.semilogy()
ax1.set_xlim(10**1,max(Darts))
ax1.set_title("MacBook Pro 2.5 GHz Intel Core i5, 4 cores running")

ax2 = ax1.twinx()
ax2.plot(Darts,simple_mean_sim,'--',label='simple')
ax2.plot(Darts,multi_mean_sim,'--',label='multi')
ax2.plot(Darts,dask_mean_sim,'--',label='dask')
ax2.set_ylabel("Simulation Rate (Darts/sec) - dashed")
ax2.semilogy()
plt.legend(loc=4)
plt.show()
plt.savefig("MacBookPro_parallel_output.png")
