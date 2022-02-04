from wls import WLS
from core import CORE
import cfg
from member import member
import numpy as np
from server import server
import random


class scheduler():
    def __init__(self, _id, servers):
        self._id = _id
        self.rate = cfg.mio
        self.__init_method(servers)

    def __init_method(self, servers):
        self.queue = WLS()
        self.current_member: member = None
        self.servers = []
        for _, srvr in enumerate(servers):
            self.servers.append(srvr)

    def __get_time_to_work(self):
        time_to_work = np.random.exponential(1/self.rate)
        if cfg.TRACE:
            return 1
        # time_to_work = 1
        return time_to_work

    def arrive(self, member):
        self.queue.arrive(member)

    def is_serving(self):
        return self.current_member != None

    def time_to_idle(self):
        if not self.is_serving():
            return 0
        return self.current_member.remaining_time_to_work()

    def start_work(self, member):
        self.current_member = member
        time_to_work = self.__get_time_to_work()
        if cfg.LOG:
            print(
                f"\t==> time to work [at scheduler] for ID={member._id} : {time_to_work}")
        b = self.current_member.begin_work(time_to_work)
        if not b:
            self.current_member = None

    def find_appropriate_server_to_push(self):
        return_idx, mn = 0, self.servers[0].get_queue_length()
        ls = list(range(len(self.servers)))
        random.shuffle(ls)
        for idx in ls:
            srvr = self.servers[idx]
            mntmp = srvr.get_queue_length()
            if mntmp <= mn:
                mn = mntmp
                return_idx = idx
        return return_idx

    def end_work(self):
        res = self.current_member.begin_queue()
        if not res:
            self.current_member = None
            return None
        idx = self.find_appropriate_server_to_push()
        self.servers[idx].arrive(self.current_member)
        self.current_member = None

    def could_run_scheduler(self):
        return not self.queue.is_empty() or self.is_serving()

    def get_queue_length(self):
        return self.queue.get_length()

    def run_scheduler(self):
        if self.is_serving():
            cfg.current_time += self.current_member.remaining_time_to_work()
            self.end_work()
        else:
            member = self.queue.leave()
            if member is not None:
                self.start_work(member)


if __name__ == "__main__":
    s1 = server([1, 1, 1], 1)
    s2 = server([2, 2, 2], 2)
    s = [s1, s2]
    sch = scheduler(1, 1, s)
    mems = member.generate_members(50)
    for mem in mems:
        sch.arrive(mem)
    while True:
        if cfg.LOG:
            print(f"T:{cfg.current_time}" + " ========="*6+"\n")
        if sch.could_run_scheduler():

            sch.run_scheduler()
        else:
            break
