from multiprocessing import cpu_count, Queue, Process, Lock
import random
import time
import sys

PROCESSES_NB = None # The number of processes will be the number of cores available on the system
TASKS_NBR = 10000 #Number of tasks to allocate to the cores
TASK_CPTIME_MIN =1 # Minimum time to compute a task 
TASK_CPTIME_MAX =100 # Miaximum time to compute a task 
NUM_CPU = cpu_count() #The number of CPUs available on the machine

random.seed() # Generates a seed for the random generator

def tasks_generator(nbr):
	for i in xrange(nbr):
		yield {'name':"Task" + str(i+1), 'duration':random.randint(TASK_CPTIME_MIN,TASK_CPTIME_MAX)}

def tasks_handler(queue,process_nb,lock):
	while not queue.empty():
		task=queue.get()
		# lock.acquire()
		# print 'Executing task ' + task['name'] + ' on process ' + str(process_nb)
		# lock.release()
		time.sleep(task['duration']/1000)

if __name__ == '__main__':
	lock=Lock()
   	process_list=[]
   	queues_list=[]
   	for i in range(0,NUM_CPU) :
   		queue=Queue()
   		queues_list.append(queue)
   		process=Process(target=tasks_handler,args=(queue,i,lock))
   		process_list.append(process)

   	startTime=time.time()

   	for task in tasks_generator(TASKS_NBR):
   		pr_num=random.randint(0,NUM_CPU-1)
   		queues_list[pr_num].put(task)

   	for process in process_list:
   		process.start()

	for process in process_list:
		process.join()

   	endTime=time.time()
	#calculate the total time it took to complete the work
	workTime =  endTime - startTime
	print "The jobs took " + str(workTime) + " seconds to complete"
