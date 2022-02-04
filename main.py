import cfg
from server import server
from scheduler import scheduler
from member import member

################# initialization #################
member_arrival_time = 0
mmbrls = []
s: list[server] = []

default_input = [[1, 1000, 1], [1, 1, 1], [
    2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]

if not cfg.DEFAULT_INPUT:
    cfg.lmbda, cfg.alpha, cfg.mio = list(map(float, input().split()))

    for i in range(1, 6):
        core1_rate, core2_rate, core3_rate = list(map(float, input().split()))
        stmp = server([core1_rate, core2_rate, core3_rate], i)
        s.append(stmp)
else:
    cfg.lmbda, cfg.alpha, cfg.mio = default_input[0]

    for i in range(1, 6):
        core1_rate, core2_rate, core3_rate = default_input[i]
        stmp = server([core1_rate, core2_rate, core3_rate], i)
        s.append(stmp)

sch = scheduler(1, s)
member_count = 1e3
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
    if cfg.log:
        print(f"T:{cfg.current_time}" + " ========="*6+"\n")
    pass

for mmbr in mmbrls:
    print(mmbr)
