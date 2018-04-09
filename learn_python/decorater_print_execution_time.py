'''
Created on 20180409

@author: Huang
'''
#use decorater to print a function execution time
import time,functools
def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kw):
        start_time=time.time()
        fn(*args,**kw)
        end_time=time.time()
        time_cost=1000*(end_time-start_time)
        print('%s executed in %s ms' % (fn.__name__, time_cost))
        return fn(*args,**kw)
    return wrapper

@metric
def fast(x,y):
    time.sleep(0.0012)
    return x+y;
@metric
def slow(x,y,z):
    time.sleep(1.34)
    return x*y*z;
f=fast(11,22)
s=slow(11,22,33)

print f, s