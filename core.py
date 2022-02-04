import numpy as np
from member import member
import cfg


class CORE(object):
    def __init__(self, rate):
        self.rate = rate
        self.__init_method()

    def __init_method(self):
        self.isBusy = False
        self.current_member: member = None

    def __change_work_status(self):
        self.isBusy = not(self.isBusy)

    def isIdle(self,):
        return not(self.isBusy)

    def start_work(self, member: member):
        self.__change_work_status()
        self.current_member = member
        time_to_work = self.__get_time_to_work()
        if cfg.LOG:
            print(
                f"\t==> time to work [at core] for ID={member._id} : {time_to_work}")
        b = self.current_member.begin_work(time_to_work)
        if not b:
            self.__change_work_status()
            self.current_member = None

    def __get_time_to_work(self):
        time_to_work = np.random.exponential(1/self.rate)
        if cfg.TRACE:
            # return 1
            time_to_work = 1/self.rate
        return time_to_work

    def end_work(self):
        self.__change_work_status()
        self.current_member.begin_queue()
        self.current_member = None

    def is_serving(self):
        return self.current_member != None
