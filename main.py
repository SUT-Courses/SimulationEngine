import cfg
from server import server
from scheduler import scheduler
from member import member
import logs

################# initialization #################
member_arrival_time = 0
mmbrls = []
s = []

default_input = [[cfg.lmbda, cfg.alpha, cfg.mio]]
default_input.extend(
    [[1/15, 2/15, 1/15] for _ in range(cfg.SERV_COUNT)])

if not cfg.DEFAULT_INPUT:
    cfg.lmbda, cfg.alpha, cfg.mio = list(map(float, input().split()))
    if cfg.IN_MEAN:
        cfg.lmbda = 1 / cfg.lmbda
        cfg.mio = 1 / cfg.mio

    for i in range(1, cfg.SERV_COUNT+1):
        if not cfg.IN_MEAN:
            core1_rate, core2_rate, core3_rate = list(
                map(float, input().split()))
        else:
            core1_rate, core2_rate, core3_rate = list(
                map(lambda x: 1/float(x), input().split()))

        stmp = server([core1_rate, core2_rate, core3_rate], i)
        s.append(stmp)
else:
    cfg.lmbda, cfg.alpha, cfg.mio = default_input[0]

    for i in range(1, cfg.SERV_COUNT+1):
        core1_rate, core2_rate, core3_rate = default_input[i]
        stmp = server([core1_rate, core2_rate, core3_rate], i)
        s.append(stmp)

sch = scheduler(1, s)
member_count = cfg.MEM_COUNT
#########################################


def do_arrive_member():
    global member_arrival_time, member_count
    cfg.current_time = member_arrival_time
    member_count -= 1
    inter_arrival_time, mem = member.generate_member()
    mmbrls.append(mem)
    member_arrival_time = cfg.current_time + inter_arrival_time
    sch.arrive(mem)


def get_member_arrival_to_run():
    if member_count > 0:
        return 1, member_arrival_time - cfg.current_time
    return None, cfg.INF


def get_server_to_run():
    tt = cfg.INF
    idx = None
    for i, srvr in enumerate(s):
        if srvr.could_run_server():
            ttidle = srvr.time_to_idle()[0][1]
            if ttidle < tt:
                tt = ttidle
                idx = i
    return idx, tt


def get_scheduler_to_run():
    tt = cfg.INF
    idx = None
    if sch.could_run_scheduler():
        idx = 1
        tt = sch.time_to_idle()
    return idx, tt


def run():
    mt = cfg.INF
    toRun = None
    idxToRun: int = None

    mmbr_arrival = get_member_arrival_to_run()
    srvr_arrival = get_server_to_run()
    schd_arrival = get_scheduler_to_run()

    # if cfg.LOG:
    #     print("mmbr_arrival", mmbr_arrival, "srvr_arrival",
    #           srvr_arrival, "schd_arrival", schd_arrival)

    if mmbr_arrival[0] is not None and mmbr_arrival[1] < mt:
        mt = mmbr_arrival[1]
        toRun = "mmbr"

    if srvr_arrival[0] is not None and srvr_arrival[1] < mt:
        mt = srvr_arrival[1]
        toRun = "srvr"
        idxToRun = srvr_arrival[0]

    if schd_arrival[0] is not None and schd_arrival[1] < mt:
        mt = schd_arrival[1]
        toRun = "schd"

    if toRun == "mmbr":
        do_arrive_member()
    elif toRun == "schd":
        sch.run_scheduler()
    elif toRun == "srvr":
        s[idxToRun].run_server()
    else:
        return False
    return True


################# MAIN  #################
while run():
    if cfg.LOG:
        print("\nT:{:5.5f}".format(cfg.current_time) + "============="*6)
    pass

# for mmbr in mmbrls:
#     print(mmbr)


alive_only_mmbrls = list(filter(lambda mm: not mm.isDead, mmbrls))

if cfg.LOGS_FINAL:
    logs.get_mean_system_time(alive_only_mmbrls)
    logs.get_mean_system_time_per_priority(alive_only_mmbrls)
    logs.get_mean_waiting_time(alive_only_mmbrls)
    logs.get_mean_waiting_time_per_priority(alive_only_mmbrls)
    logs.get_percent_of_dead_tasks(mmbrls)
    logs.get_percent_of_dead_tasks_per_priority(mmbrls)
    logs.mean_queue_length_scheduler(alive_only_mmbrls)
    logs.mean_queue_length_server(alive_only_mmbrls)
