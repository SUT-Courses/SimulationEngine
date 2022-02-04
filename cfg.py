def MY_GEN():
    n = 0
    while True:
        n += 1
        yield n


DEFAULT_INPUT = True
TRACE = False
LOGS_FINAL = True
LOG = False
current_time = 0
MY_GEN = MY_GEN()
NotValuedYet = -1
mio = 1
alpha = 1000
lmbda = 1
INF = 1e10
