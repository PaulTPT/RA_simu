from multiprocessing import cpu_count, Queue, Process, Lock
import random
import time
import sys
import config_manager
import allocation_algorithms

random.seed() # Generates a seed for the random generator

PROCESSES_NB = None # The number of processes will be the number of cores available on the system
NUM_CPU = cpu_count() # The number of CPUs available on the machine

# The code running on each core
def tasks_handler(queue,process_nb,lock):
	while not queue.empty():
		task=queue.get() # We get on the queue one of the tasks allocated by the tasks allocator 
		lock.acquire()
		# print 'Executing task ' + task['name'] + ' on process ' + str(process_nb)
		lock.release()
		time.sleep(task['duration']/1000.0) # Simulation of the execution time

# The function allocating tasks to the queues of the different cores
def tasks_allocator(tasks,queues):
		# Implement your ressource allocation algorithm here
		allocation_algorithms.random_algo(tasks,queues)


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


   	# Initialisation of the processes and their queues
   	for i in range(0,NUM_CPU) :
   		queue=Queue()
   		queues_list.append(queue)
   		process=Process(target=tasks_handler,args=(queue,i,lock))
   		process_list.append(process)

   	startTime=time.time()

   	# tasks=tasks_generator(TASKS_NBR)
   	tasks=config_manager.load_tasks(config_name,NUM_CPU)
   	tasks_allocator(tasks,queues_list)

   	for process in process_list:
   		process.start()

	for process in process_list:
		process.join()

   	endTime=time.time()

	#calculate the total time it took to complete the work
	workTime =  endTime - startTime

	print "The jobs took " + str(workTime) + " seconds to complete"
