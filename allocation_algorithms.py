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

def maxMin_algo(tasks,queues,process_list):
	for task in tasks:
		task['Done']=False

	nbr_task=len(tasks)

	for i in xrange(0,nbr_task):
		larger_task={'charge_min':0}
		for task in [task for task in tasks if task['Done']==False]:
			task['charge_min']=float('inf')
			task['process']=None
			for process in process_list:
				charge=compute_charge(tasks,task,process)
				if charge<task['charge_min']:
					task['charge_min']=charge
					task['process']=process
			if task['charge_min']>=larger_task['charge_min']:
				larger_task=task
		larger_task['Done']=True
		larger_task['process'].addCharge(larger_task['duration'])
		larger_task['process']=larger_task['process'].get_id()
		queues[larger_task['process']].put(larger_task)

def compute_charge(tasks,task,process):
	charge=process.getCharge()+task['duration']

	for dependancy in task['dependancies']:
		dependancy_process=next(dep_task['process'] for dep_task in tasks if dep_task['name']== dependancy )
		if (type(dependancy_process) is int):
			process_delay=process.get_delays()[dependancy_process]
			charge+=process_delay
	return charge
