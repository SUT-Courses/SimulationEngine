def MY_GEN():
    n = 0
    while True:
        n += 1
        yield n


IN_MEAN = False
DEFAULT_INPUT = False
TRACE = False
LOGS_FINAL = True
LOG = False
SERV_COUNT = 5
MEM_COUNT = 1_000_000
current_time = 0
MY_GEN = MY_GEN()
NotValuedYet = -1
mio = -1
alpha = -1
lmbda = -1
INF = 1e10
