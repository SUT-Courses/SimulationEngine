def MY_GEN():
    n = 0
    while True:
        n += 1
        yield n


current_time = 0
MY_GEN = MY_GEN()
NotValuedYet = -1
log = True