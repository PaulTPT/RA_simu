from multiprocessing import Pool
import random
import time
import sys

PROCESSES_NB = None # The number of processes will be the number of cores available on the system
TASKS_NBR = 100 #Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task 

random.seed() # Generates a seed for the random generator

def tasks_generator(nbr):
	for i in xrange(nbr):
		yield {'name':"Task" + str(i+1), 'duration':random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX)}

if __name__ == '__main__':
     pool=Pool(processes=PROCESSES_NB)

     for task in tasks_generator(TASKS_NBR):
     	print task['name'],task['duration']


