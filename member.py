from turtle import RawTurtle
from pandas import interval_range
import cfg
import random
import numpy as np


class STATUS:
    WAIT_1 = 1
    SERVE_1 = 2
    WAIT_2 = 3
    SERVE_2 = 4
    END = 5
    DEAD = 6


class member():
    def __init__(self, time_limit, priority):
        self.status = 0
        self.priority = priority
        self.time_limit = time_limit
        self.__init_method()

    def __str__(self):
        return "==> member\n" + \
            f"\tID: {self._id} | Status: {self.status} | Priority: {self.priority} | Time Limit: {self.time_limit*1000//1/1000} | isDead: {self.isDead} | Service Queue: {self.service_queue} \n" + \
            f"\tTime status: {self.time_status}\n"

    @staticmethod
    def get_id():
        return next(cfg.MY_GEN)

    @staticmethod
    def generate_members(n, tl=100):
        members = [member(tl, random.choice([1, 2, 2, 2, 2]))
                   for _ in range(n)]
        return members

    @staticmethod
    def generate_member():
        tl = member.get_time_limit()
        interarrival_time = member.get_interarrival()
        mem = member(tl, random.choice([1]+[2]*9))
        return interarrival_time, mem

    @staticmethod
    def get_interarrival():
        return np.random.exponential(cfg.lmbda)

    @staticmethod
    def get_time_limit():
        return np.random.exponential(cfg.alpha)

    @staticmethod
    def get_priority1_ls(mmls):
        return list(filter(lambda x: x.priority == 1, mmls))

    @staticmethod
    def get_priority2_ls(mmls):
        return list(filter(lambda x: x.priority == 2, mmls))

    def __init_method(self):
        self.service_queue = None
        self.isDead = False
        self.time_status = {1: cfg.NotValuedYet, 2: cfg.NotValuedYet, 3: cfg.NotValuedYet,
                            4: cfg.NotValuedYet, 5: cfg.NotValuedYet, 6: cfg.NotValuedYet}
        self._id = member.get_id()
        self.begin_queue()
        self.time_to_work = cfg.NotValuedYet

    def set_status(self, status):
        self.status = status
        self.time_status[status] = cfg.current_time

    def begin_work(self, time_to_work):
        if self.is_dead():
            self.set_status(STATUS.DEAD)
            return False

        # if cfg.log:
        #     print(f"begin_work ==> {self.status}")
        self.set_status(self.status + 1)
        self.time_to_work = time_to_work
        return True

    def begin_queue(self):
        if cfg.log:
            print(
                f"#begin_queue for ID={self._id} ==> status {self.status} | queue at {cfg.current_time}")
        if self.is_dead():
            self.set_status(STATUS.DEAD)
            return False
        if self.time_status[STATUS.SERVE_2] >= 0:
            self.set_status(STATUS.END)
            return True
        if self.time_status[STATUS.SERVE_1] >= 0 and not self.is_dead():
            self.set_status(STATUS.WAIT_2)
            return True
        self.set_status(STATUS.WAIT_1)

    def is_dead(self):
        if self.time_status[STATUS.WAIT_1] == -1:
            self.isDead = False
            return False
        isDead = self.status < STATUS.SERVE_2 and cfg.current_time - \
            self.time_status[STATUS.WAIT_1] > self.time_limit
        self.isDead = isDead
        return self.isDead

    def is_served(self):
        return self.status == STATUS.SERVE_1 or self.status == STATUS.SERVE_2

    def is_waited(self):
        return self.status == STATUS.WAIT_1 or self.status == STATUS.WAIT_2

    def is_to_be_waited(self):
        return self.is_served() and self.time_to_work \
            <= cfg.current_time - self.time_status[self.status]

    def time_from_begin_of_last_status(self):
        if cfg.log:
            # print(
            # f"Time from begin of last status ==> CT {cfg.current_time} || {self.time_status[self.status]}")
            pass
        return cfg.current_time - self.time_status[self.status]

    def remaining_time_to_work(self,):
        if cfg.log:
            print(
                f"Remaining time to work {self._id} ==> {self.time_to_work} - {self.time_from_begin_of_last_status()}")
        return self.time_to_work - self.time_from_begin_of_last_status()

    def get_queue1_time(self):
        return self.time_status[STATUS.SERVE_1] - self.time_status[STATUS.WAIT_1]

    def get_queue2_time(self):
        return self.time_status[STATUS.SERVE_2] - self.time_status[STATUS.WAIT_2]

    def get_queue2_id(self):
        return self.service_queue

    def get_system_time(self):
        return self.time_status[STATUS.END] - self.time_status[STATUS.WAIT_1]

    def get_queue_time(self):
        return self.get_queue1_time() + self.get_queue2_time()


def __test_member(a):
    a.begin_work(3)
    cfg.current_time += 3
    a.begin_queue()
    cfg.current_time += 1
    a.begin_work(3)
    cfg.current_time += 4


if __name__ == '__main__':
    a = member(10, 1)
    __test_member(a)
