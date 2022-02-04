from wls import WLS
from core import CORE
import cfg
from member import member
from FS import FREE_STAT

counter = 0


class server():
    def __init__(self, rates: list, _id: int):
        self.rates = rates
        self._id = _id
        self.__init_method()

    def __init_method(self):
        self.cores: list[CORE] = []
        self.queue = WLS()
        for rate in self.rates:
            self.cores.append(CORE(rate))

    def __get_idxRemainingTime(self, cores, idx, freedom_status):
        if cores[idx].isIdle() and (freedom_status == FREE_STAT.QUEUE_WORKING or
                                    freedom_status == FREE_STAT.QUEUE_AND_CORE_WORKING):
            return (idx, 0)
        elif cores[idx].isIdle():
            return (idx, cfg.INF)
        tmp_min = cores[idx].current_member.remaining_time_to_work()
        Min = (idx, tmp_min)
        return Min

    def get_freedom_status(self):
        if self.queue.is_empty():
            key = False
            for core in self.cores:
                if core.isBusy:
                    key = True
            if key:
                return (FREE_STAT.CORE_WORKING)
            return FREE_STAT.NO_WORKING
        key = False
        for core in self.cores:
            if core.isBusy:
                key = True
        if key:
            return (FREE_STAT.QUEUE_AND_CORE_WORKING)
        return FREE_STAT.QUEUE_WORKING

    def get_queue_length(self):
        return self.queue.get_length()

    def arrive(self, member):
        member.service_queue = self._id
        self.queue.arrive(member)

    def time_to_idle(self):
        freedom_status = self.get_freedom_status()
        cores = self.cores
        idxTimeLs = [self.__get_idxRemainingTime(cores, 0, freedom_status), self.__get_idxRemainingTime(
            cores, 1, freedom_status), self.__get_idxRemainingTime(cores, 2, freedom_status)]
        idxTimeLs.sort(key=lambda x: x[1])
        return idxTimeLs

    def time_to_idle_forServedOnly(self):
        idxTimeLs = self.time_to_idle()
        return list(filter(lambda x: self.cores[x[0]].is_serving(), idxTimeLs))

    def could_run_server(self):
        mins = self.time_to_idle_forServedOnly()
        if not self.queue.is_empty() or len(mins) > 0:
            return True
        return False

    def run_server(self):
        global counter
        counter += 1
        print(counter)
        idxTimeLs = self.time_to_idle()
        idx, Time = idxTimeLs[0]
        if self.cores[idx].is_serving():
            cfg.current_time += Time
            self.cores[idx].end_work()
        else:
            member = self.queue.leave()
            if member is not None:
                self.cores[idx].start_work(member)
            else:
                # idle core and is_empty wls
                ls = self.time_to_idle_forServedOnly()
                if len(ls) == 0:
                    return None
                idx, Time = ls[0]
                cfg.current_time += Time
                self.cores[idx].end_work()


def test_server():
    s = server([1, 1, 1], 1)
    mems = member.generate_members(5)
    for mem in mems:
        s.arrive(mem)
    while True:
        if cfg.LOG:
            print(f"T:{cfg.current_time}" + " ========="*6+"\n")
        if s.could_run_server():
            s.run_server()
        else:
            break


if __name__ == "__main__":
    import random
    test_server()
