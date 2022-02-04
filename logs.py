from member import member
import functools


def get_mean_system_time(mems: list[member]):
    print("Mean system time: ")
    ls = list(map(lambda x: x.get_system_time(), mems))
    print(sum(ls) / len(ls))
    pass


def get_mean_system_time_per_priority(mems: list[member]):
    print("Mean system time per priority: ")
    mm1ls: list[member] = member.get_priority1_ls(mems)
    ls = list(map(lambda x: x.get_system_time(), mm1ls))
    print("type1", sum(ls) / len(ls))

    mm2ls: list[member] = member.get_priority2_ls(mems)
    ls = list(map(lambda x: x.get_system_time(), mm2ls))
    print("type2", sum(ls) / len(ls))
    pass


def get_mean_waiting_time(mems: list[member]):
    print("Mean waiting time: ")
    ls = list(map(lambda x: x.get_queue_time(), mems))
    print(sum(ls) / len(ls))
    pass


def get_mean_waiting_time_per_priority(mems: list[member]):
    print("Mean waiting time per priority: ")
    mm1ls: list[member] = member.get_priority1_ls(mems)
    ls = list(map(lambda x: x.get_queue_time(), mm1ls))
    print("type1", sum(ls) / len(ls))

    mm2ls: list[member] = member.get_priority2_ls(mems)
    ls = list(map(lambda x: x.get_queue_time(), mm2ls))
    print("type2", sum(ls) / len(ls))
    pass


def get_percent_of_dead_tasks(mems: list[member]):
    print("Percent of dead tasks: ")
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mems, 0) / len(mems)
    print(podt*100)
    pass


def get_percent_of_dead_tasks_per_priority(mems: list[member]):
    print("Percent of dead tasks per priority: ")

    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mems, 0) / len(mems)
    print(podt*100)

    mm1ls: list[member] = member.get_priority1_ls(mems)
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mm1ls, 0) / len(mm1ls)
    print("type1", podt*100)
    mm2ls: list[member] = member.get_priority1_ls(mems)
    podt = functools.reduce(
        lambda a, b: a + 1 if b.isDead else a, mm2ls, 0) / len(mm2ls)
    print("type1", podt*100)
    pass


def mean_queue_length_scheduler(mems: list[member]):
    print("Mean queue length scheduler: ")
    pass


def mean_queue_length_server(mems: list[member]):
    print("Mean queue length server: ")
    pass
