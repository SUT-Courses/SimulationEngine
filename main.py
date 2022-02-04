import cfg
from server import server
from scheduler import scheduler
from member import member

member_arrival_time = 0


s1 = server([1, 1, 1], 1)
s2 = server([2, 2, 2], 2)
s3 = server([3, 3, 3], 3)
s4 = server([4, 4, 4], 4)
s5 = server([5, 5, 5], 5)
s: list[server] = [s1, s2, s3, s4, s5]
sch = scheduler(1, s)
member_count = 10


def do_arrive_member():
    global member_arrival_time, member_count
    cfg.current_time = member_arrival_time
    member_count -= 1
    inter_arrival_time, mem = member.generate_member()
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


while run():
    print(f"T:{cfg.current_time}" + " ========="*6+"\n")
    pass
