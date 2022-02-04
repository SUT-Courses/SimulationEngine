from member import member
import functools
import cfg


def get_mean_system_time(mems):
    print("Mean system time: ")
    ls = list(map(lambda x: x.get_system_time(), mems))
    print(sum(ls) / len(ls))
    pass


def get_mean_system_time_per_priority(mems):
    print("Mean system time per priority: ")
    mm1ls = member.get_priority1_ls(mems)
    ls = list(map(lambda x: x.get_system_time(), mm1ls))
    print("type1", sum(ls) / len(ls))

    mm2ls = member.get_priority2_ls(mems)
    ls = list(map(lambda x: x.get_system_time(), mm2ls))
    print("type2", sum(ls) / len(ls))
    pass


def get_mean_waiting_time(mems):
    print("Mean waiting time: ")
    ls = list(map(lambda x: x.get_queue_time(), mems))
    print(sum(ls) / len(ls))
    pass


def get_mean_waiting_time_per_priority(mems):
    print("Mean waiting time per priority: ")
    mm1ls = member.get_priority1_ls(mems)
    ls = list(map(lambda x: x.get_queue_time(), mm1ls))
    print("type1", sum(ls) / len(ls))

    mm2ls = member.get_priority2_ls(mems)
    ls = list(map(lambda x: x.get_queue_time(), mm2ls))
    print("type2", sum(ls) / len(ls))
    pass


def get_percent_of_dead_tasks(mems):
    print("Percent of dead tasks: ")
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mems, 0) / len(mems)
    print(podt*100)
    pass


def get_percent_of_dead_tasks_per_priority(mems):
    print("Percent of dead tasks per priority: ")

    mm1ls = member.get_priority1_ls(mems)
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mm1ls, 0) / len(mm1ls)
    print("type1", podt*100)
    mm2ls = member.get_priority2_ls(mems)
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mm2ls, 0) / len(mm2ls)
    print("type2", podt*100)
    pass


def mean_queue_length_scheduler(mems):
    print("Mean queue length scheduler: ")
    mean_len = functools.reduce(
        lambda a, b: a + b.get_queue1_time(), mems, 0) / cfg.current_time
    print(mean_len)
    pass


def mean_queue_length_server(mems):
    print("Mean queue length server: ")
    mems1 = list(filter(lambda x: x.service_queue == 1, mems))
    mems2 = list(filter(lambda x: x.service_queue == 2, mems))
    mems3 = list(filter(lambda x: x.service_queue == 3, mems))
    mems4 = list(filter(lambda x: x.service_queue == 4, mems))
    mems5 = list(filter(lambda x: x.service_queue == 5, mems))
    memsls = [mems1, mems2, mems3, mems4, mems5]
    for i in range(1, len(memsls)+1):
        mean_len = functools.reduce(
            lambda a, b: a + b.get_queue2_time(), memsls[i-1], 0) / cfg.current_time
        print(f"service{i}:", mean_len)
    pass
