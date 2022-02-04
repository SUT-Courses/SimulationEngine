from wls import WLS
from core import CORE
import cfg
from member import member


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

    def get_queue_length(self):
        return self.queue.get_length()

    def __get_idxRemainingTime(self, cores, idx):
        if cores[idx].isIdle():
            return (idx, 0)
        tmp_min = cores[idx].current_member.remaining_time_to_work()
        Min = (idx, tmp_min)
        return Min

    def arrive(self, member):
        self.queue.arrive(member)

    def time_to_idle(self):
        cores = self.cores
        idxTimeLs = [self.__get_idxRemainingTime(cores, 0), self.__get_idxRemainingTime(
            cores, 1), self.__get_idxRemainingTime(cores, 2)]
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
        idxTimeLs = self.time_to_idle()
        idx, Time = idxTimeLs[0]
        if self.cores[idx].is_serving():
            cfg.current_time += Time
            self.cores[idx].end_work()
        else:
            member = self.queue.leave()
            if member != None:
                self.cores[idx].start_work(member)
            else:
                # idle core and is_empty wls
                idx, Time = self.time_to_idle_forServedOnly()[0]
                cfg.current_time += Time
                self.cores[idx].end_work()


def test_server():
    s = server([1, 1, 1], 1)
    mems = member.generate_members(5)
    for mem in mems:
        s.arrive(mem)
    while True:
        if cfg.log:
            print(f" {cfg.current_time}" + "  ====  ===="*6)
        if s.could_run_server():
            s.run_server()
        else:
            break


if __name__ == "__main__":
    import random
    test_server()
