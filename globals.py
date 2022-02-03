def my_gen():
    n = 0
    while True:
        n += 1
        yield n


current_time = 0
MY_GEN = my_gen()
NotValuedYet = -1
log = True
