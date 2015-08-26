from os import path
from os import mkdir
import random
import sys

TASKS_NBR = 100 # Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task
DELAY_MIN =1 # Minimum delay
DELAY_MAX =10 # Miaximum delay
MAX_DEPENDANCY =5 # Miaximum dependancy

def generate_config (config_name, NUM_CPU):
	config_path="configs/"+str(config_name)

	try:
		mkdir(config_path)
	except  OSError:  
		print "This config already exists. Overweriting...\n"

	file_path_tasks= path.relpath(config_path+"/tasks.cfg")
	tasks_data=open(file_path_tasks,'w')

	for task in tasks_generator(TASKS_NBR):
		tasks_data.write(task['name']+' '+str(task['duration'])+' ')
		for dependancy in task['dependancies']:
			tasks_data.write(dependancy+' ')
		tasks_data.write('\n')

	tasks_data.close()

	file_path_delay= path.relpath(config_path+"/delays.cfg")
	delay_data=open(file_path_delay,'w')

	for delay_array in net_delay_generator(NUM_CPU):
		for delay in delay_array:
			delay_data.write(str(delay)+ ' ')
		delay_data.write('\n')


	delay_data.close()

	print "Config created succesfully !\n"



# Generator generating nbr tasks with a random execution time
def tasks_generator(nbr):
	for i in xrange(nbr):
		tasks_dependancy=[]
		for j in xrange(random.randint(0,MAX_DEPENDANCY)):
			task_nbr=random.randint(0,nbr-1)
			while task_nbr==i:
				task_nbr=random.randint(0,nbr-1)
			tasks_dependancy.append('Task'+str(task_nbr+1))
		yield {'name':"Task" + str(i+1), 'duration': random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX), 'dependancies':tasks_dependancy}


# Generator generating the communication delays between the different CPU (blades)
def net_delay_generator(nbr_cpu):
	for i in xrange(nbr_cpu):
		delays=[]
		for j in xrange(nbr_cpu):
			delays.append(random.randint(DELAY_MIN,DELAY_MAX))
		delays[i]=0
		yield delays
	

# Returns a list of the tasks
def load_tasks(config_name,NUM_CPU):
	config_path="configs/"+str(config_name)
	file_path_tasks= path.relpath(config_path+"/tasks.cfg")

	try:
		tasks_data=open(file_path_tasks,'r')
	except IOError:
		print ('Config does not exists. Generating it...'+'\n')	
		generate_config(config_name,NUM_CPU)
		return load_tasks(config_name,NUM_CPU)
		
	return parse_tasks_config(tasks_data)

def parse_tasks_config(tasks_data):
	tasks=[]
	for line in tasks_data:
		line_words=line.split()
		tasks.append({'name': line_words[0], 'duration': int(line_words[1]), 'dependancies': line_words[2:]})
	tasks_data.close()
	return tasks

# Returns a generator of the delays for each blade to the other blades
def load_delays(config_name):
	config_path="configs/"+str(config_name)
	file_path_delays= path.relpath(config_path+"/delays.cfg")

	try:
		delays_data=open(file_path_delays,'r')
	except IOError:
		print ('Config does not exists. Generating it...'+'\n')	
		generate_config(config_name,NUM_CPU)
		return load_delays(config_name,NUM_CPU)
		
	return parse_delays_config(delays_data)	


def parse_delays_config(delays_data):
	try:
		for line in delays_data:
			line_words=line.split()
			yield [int(word) for word in line_words]
	finally:
		delays_data.close()

