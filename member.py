import re
from globals import *


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

    @staticmethod
    def get_id():
        return next(MY_GEN)

    def __init_method(self):
        self.time_status = {1: NotValuedYet, 2: NotValuedYet, 3: NotValuedYet,
                            4: NotValuedYet, 5: NotValuedYet, 6: NotValuedYet}
        self._id = member.get_id()
        self.begin_queue()
        self.time_to_work = NotValuedYet

    def set_status(self, status):
        self.status = status
        self.time_status[status] = current_time

    def begin_work(self, time_to_work):
        if self.is_dead():
            self.set_status(STATUS.DEAD)
            return False

        self.set_status(self.status + 1)
        self.time_to_work = time_to_work
        return True

    def begin_queue(self):
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
        return self.status < STATUS.SERVE_2 and current_time - self.time_status[STATUS.WAIT_1] > self.time_limit

    def is_served(self):
        return self.status == STATUS.SERVE_1 or self.status == STATUS.SERVE_2

    def is_waited(self):
        return self.status == STATUS.WAIT_1 or self.status == STATUS.WAIT_2

    def is_to_be_waited(self):
        return self.is_served() and self.time_to_work \
            <= current_time - self.time_status[self.status]


def __test_member(a):
    global current_time
    a.begin_work(3)
    current_time += 3
    a.begin_queue()
    current_time += 1
    a.begin_work(3)
    current_time += 4


if __name__ == '__main__':
    a = member(10, 1)
    __test_member(a)
