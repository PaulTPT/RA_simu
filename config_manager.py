# import numpy
import random
from os import path
from os import mkdir

TASKS_NBR = 1000 # Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task
DELAY_MIN =1 # Minimum delay
DELAY_MAX =10 # Miaximum delay

random.seed() # Generates a seed for the random generator

def generate_config (config_name, NUM_CPU):
	config_path="configs/"+str(config_name)

	try:
		mkdir(config_path)
	except  OSError:  
		print "This config already exists. Overweriting...\n"

	file_path_tasks= path.relpath(config_path+"/tasks.cfg")
	tasks_data=open(file_path_tasks,'w')

	for task in tasks_generator(TASKS_NBR):
		tasks_data.write(task['name']+' '+str(task['duration'])+'\n')

	tasks_data.close()

	file_path_delay= path.relpath(config_path+"/delays.cfg")
	delay_data=open(file_path_delay,'w')

	for delay_array in net_delay_generator(NUM_CPU):
		for delay in delay_array:
			delay_data.write(str(delay)+ ' ')
		delay_data.write('\n')


	delay_data.close()

	print "Config created succesfully !\n"



# Generator generating n tasks with a random execution time
def tasks_generator(nbr):
	for i in xrange(nbr):
		yield {'name':"Task" + str(i+1), 'duration':random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX)}

def net_delay_generator(nbr_cpu):
	for i in xrange(nbr_cpu):
		delays=[]
		for j in xrange(nbr_cpu):
			delays.append(random.randint(DELAY_MIN,DELAY_MAX))
		delays[i]=0
		yield delays
	

