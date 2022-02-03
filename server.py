from wls import WLS
from core import CORE
import cfg
from member import member


class server():
    def __init__(self, rates: list, id: int):
        self.rates = rates
        self.id = id
        self.__init_method()

    def __init_method(self):
        self.cores: list[CORE] = []
        self.queue = WLS()
        for rate in self.rates:
            self.cores.append(CORE(rate))

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

    def time_to_idle_0Excluding(self):
        idxTimeLs = self.time_to_idle()
        return list(filter(lambda x: x[1] != 0, idxTimeLs))

    def run_server(self):
        idxTimeLs = self.time_to_idle()
        idx, Time = idxTimeLs[0]
        if Time > 0:
            cfg.current_time += Time
            self.cores[idx].end_work()
        elif Time == 0:
            member = self.queue.leave()
            if member != None:
                self.cores[idx].start_work(member)
            else:
                # idle core and is_empty wls
                try:
                    idx, Time = self.time_to_idle_0Excluding()[0]
                    cfg.current_time += Time
                    self.cores[idx].end_work()
                except:
                    if cfg.log:
                        print("Failed to run Server!!")
                    pass


if __name__ == "__main__":
    import random
    s = server([1, 1, 1], 1)
    members = [member(40, random.choice([1, 2, 2, 2, 2])) for _ in range(5)]
    for mem in members:
        s.arrive(mem)
    while True:
        s.run_server()
