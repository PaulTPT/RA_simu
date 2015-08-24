# import numpy
import random
from os import path
from os import mkdir

TASKS_NBR = 1000 # Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task 

random.seed() # Generates a seed for the random generator

def generate_config (config_name, NUM_CPU):
	try:
		mkdir("configs/"+str(config_name))
	except  OSError:
		print "This config already exists. Overweriting...\n"

	file_path= path.relpath("configs/"+str(config_name)+"/tasks.cfg")
	tasks_data=open(file_path,'w')

	for task in tasks_generator(TASKS_NBR):
		tasks_data.write(task['name']+' '+str(task['duration'])+'\n')

	print "Config created succesfully !\n"



# Generator generating n tasks with a random execution time
def tasks_generator(nbr):
	for i in xrange(nbr):
		yield {'name':"Task" + str(i+1), 'duration':random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX)}


