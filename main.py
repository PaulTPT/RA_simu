from multiprocessing import cpu_count, Queue, Lock, current_process
from Blade_Process import Process_delays as Process
import random
import time
import sys
import config_manager
import allocation_algorithms

random.seed() # Generates a seed for the random generator

PROCESSES_NB = None # The number of processes will be the number of cores available on the system
NUM_CPU = cpu_count() # The number of CPUs available on the machine

# The code running on each core
def tasks_handler(tasks,queue,lock):
	process=current_process()
	charge=0
	while not queue.empty():
		task=queue.get() # We get on the queue one of the tasks allocated by the tasks allocator 
		# lock.acquire()
		# print 'Executing task ' + task['name'] + ' on process ' + str(process.get_id())
		# lock.release()
		time.sleep(task['duration']/1000.0) # Simulation of the execution time
		charge+=task['duration']
		for dependancy in task['dependancies']:
			dependancy_process=next(task['process'] for task in tasks if task['name']== dependancy)
			process_delay=process.get_delays()[dependancy_process]
			time.sleep(process_delay/1000.0)
			charge+=process_delay
			# lock.acquire()
			# print 'Sleeping '+ str(process_delay) +' ms waiting for transfer from process '+ str(dependancy_process) + '\n'
			# lock.release()
	lock.acquire()
	print 'The jobs on process ' + str(process.get_id()) + ' took ' + str(charge) + ' ms to complete\n'
	lock.release()

# The function allocating tasks to the queues of the different cores
def tasks_allocator(tasks,BOTS,queues,process_list):
		startTimeTA=time.time()

		# Put your ressource allocation algorithm here
		# 
		# allocation_algorithms.maxMin_algo(tasks,BOTS,queues,process_list)
		# allocation_algorithms.random_algo(tasks,queues)
		allocation_algorithms.roundRobin_algo(tasks,queues,process_list)


		endTimeTA=time.time()

		#calculate the total time it took to allocate the tasks
		TATime =  endTimeTA - startTimeTA
		print 'The task allocation took ' +str(TATime) + " seconds to complete\n"


if __name__ == '__main__':

	lock=Lock()
   	process_list=[]
   	queues_list=[]
   	config_name=""


   	if len(sys.argv)==2:
   		config_name=sys.argv[1]
	elif len(sys.argv)==1:
		config_name=raw_input("Give a name to the new config:\n")
		config_manager.generate_config(config_name, NUM_CPU)
	else:
		print "Please enter the folder containing the config you weant to use or no argument if you want to generate a new one."
		sys.exit()


   	BOTS=config_manager.load_tasks(config_name,NUM_CPU)
   	tasks=[]
   	for task_bag in BOTS:
   		for task in task_bag:
   			tasks.append(task)


   	# Initialisation of the processes and their queues
   	for i in range(0,NUM_CPU) :
   		queue=Queue()
   		queues_list.append(queue)
   		process=Process(i,target=tasks_handler,args=(tasks,queue,lock))
   		process_list.append(process)

   	delays=config_manager.load_delays(config_name)

	for process in process_list:
		process.set_delays(delays.next())
   	
   	tasks_allocator(tasks,BOTS,queues_list,process_list)


   	startTime=time.time()

   	for process in process_list:
   		process.start()

	for process in process_list:
		process.join()

   	endTime=time.time()

	#calculate the total time it took to complete the work
	workTime =  endTime - startTime

	print "The jobs took " + str(workTime) + " seconds to complete\n"


