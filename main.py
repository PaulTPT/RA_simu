from multiprocessing import Pool
PROCESSES_NB = None # The number of processes will be the number of cores available on the system

def f(x):
     return x*x


if __name__ == '__main__':
     pool=Pool(processes=PROCESSES_NB)

     result = pool.apply_async(f, (10,))    # evaluate "f(10)" asynchronously
     print result.get(timeout=1)           # prints "100" unless your computer is *very* slow

     print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"

     it = pool.imap(f, range(10))
     print it.next()                       # prints "0"
     print it.next()                       # prints "1"
     print it.next(timeout=1)              # prints "4" unless your computer is *very* slow
     