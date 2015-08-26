import random

def random_algo(tasks,queues):
	num_process=len(queues)-1
	for task in tasks:
		pr_num=random.randint(0,num_process-1)
		queues[pr_num].put(task)
		task['process']=pr_num

def roundRobin_algo(tasks,queues):
	num_process=len(queues)-1
	i=0
	for task in tasks:
		pr_num=i%4
		i+=1
		queues[pr_num].put(task)
		task['process']=pr_num