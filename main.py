from multiprocessing import cpu_count, Queue, Process, Lock
import random
import time
import sys

PROCESSES_NB = None # The number of processes will be the number of cores available on the system
TASKS_NBR = 1000 # Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task 
NUM_CPU = cpu_count() # The number of CPUs available on the machine

random.seed() # Generates a seed for the random generator

# Generator generating n tasks with a random execution time
def tasks_generator(nbr):
	for i in xrange(nbr):
		yield {'name':"Task" + str(i+1), 'duration':random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX)}

# The code running on each core
def tasks_handler(queue,process_nb,lock):
	while not queue.empty():
		task=queue.get() # We get on the queue one of the tasks allocated by the tasks allocator 
		lock.acquire()
		print 'Executing task ' + task['name'] + ' on process ' + str(process_nb)
		lock.release()
		time.sleep(task['duration']/1000) # Simulation of the execution time

# The function allocating tasks to the queues of the different cores
def tasks_allocator(tasks,queues):
		# Implement your ressource allocation algorithm here
		#
		# Exemple: Random allocation
		num_process=len(queues)-1
	   	for task in tasks:
	   		pr_num=random.randint(0,num_process-1)
	   		queues[pr_num].put(task)


if __name__ == '__main__':

	lock=Lock()
   	process_list=[]
   	queues_list=[]

   	# Initialisation of the processes and their queues
   	for i in range(0,NUM_CPU) :
   		queue=Queue()
   		queues_list.append(queue)
   		process=Process(target=tasks_handler,args=(queue,i,lock))
   		process_list.append(process)

   	startTime=time.time()

   	tasks=tasks_generator(TASKS_NBR)
   	tasks_allocator(tasks,queues_list)

   	for process in process_list:
   		process.start()

	for process in process_list:
		process.join()

   	endTime=time.time()

	#calculate the total time it took to complete the work
	workTime =  endTime - startTime

	print "The jobs took " + str(workTime) + " seconds to complete"
