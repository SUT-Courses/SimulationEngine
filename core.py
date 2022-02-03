import numpy as np
from member import member


class CORE(object):
    def __init__(self, rate):
        self.rate = rate
        self.__init_method()

    def __init_method(self):
        self.isBusy = False
        self.current_member: member = None

    def __change_work_status(self):
        self.isBusy = ~self.isBusy

    def isIdle(self,):
        return ~self.isBusy

    def start_work(self, member: member):
        self.__change_work_status()
        self.current_member = member
        time_to_work = np.random.exponential(1/self.rate)
        self.current_member.begin_work(time_to_work)

    def end_work(self):
        self.__change_work_status()
        self.current_member.begin_queue()
        self.current_member = None
