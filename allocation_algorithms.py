import random

def random_algo(tasks,queues):
	num_process=len(queues)-1
	for task in tasks:
		pr_num=random.randint(0,num_process-1)
		queues[pr_num].put(task)
		task['process']=pr_num

def roundRobin_algo(tasks,queues,process_list):
	num_process=len(queues)-1
	i=0
	for task in tasks:
		pr_num=i%4
		i+=1
		queues[pr_num].put(task)
		task['process']=pr_num
		process=process_list[pr_num]
		process.setCharge(compute_charge(tasks,task,process))

	for process in process_list:
		print str(process.get_id()) +' : ' +str(process.getCharge())

def maxMin_algo(tasks,BOTS,queues,process_list):
	for task in tasks:
			task['Done']=False


	for BOT_tasks in BOTS :

		nbr_task=len(BOT_tasks)

		for i in xrange(0,nbr_task):
				larger_task={'charge_min':0}
				for task in [task for task in BOT_tasks if task['Done']==False]:
					task['charge_min']=float('inf')
					task['best_process']=None
					for process in process_list:
						charge=compute_charge(tasks,task,process)
						if charge<task['charge_min']:
							task['charge_min']=charge
							task['best_process']=process
					if task['charge_min']>=larger_task['charge_min']:
						larger_task=task
				larger_task['Done']=True
				larger_task['best_process'].setCharge(larger_task['charge_min'])
				larger_task['process']=larger_task['best_process'].get_id()
				larger_task['best_process']=None
		for task in BOT_tasks:	
			queues[task['process']].put(task)

	for process in process_list:
		print str(process.get_id()) +' : ' +str(process.getCharge())

def compute_charge(tasks,task,process):
	charge=process.getCharge()+task['duration']

	for dependancy in task['dependancies']:
		dependancy_process=next(dep_task['process'] for dep_task in tasks if dep_task['name']== dependancy )
		if dependancy_process != None:
			process_delay=process.get_delays()[dependancy_process]
			charge+=process_delay
	return charge
