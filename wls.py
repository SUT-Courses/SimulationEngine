import cfg


class WL():
    def __init__(self, priority):
        self.priority = priority
        self.wl = []

    def arrive(self, member):
        if member.priority == self.priority:
            self.wl.insert(0, member)
            return True
        return False

    def leave(self):
        if self.wl.__len__() == 0:
            return None
        mem = self.wl.pop()
        if mem.is_dead():
            if cfg.LOG:
                print(
                    f"(#leave for ID={mem._id} ==> status {mem.status} | queue at {cfg.current_time})")
            return self.leave()
        return mem

    def is_empty(self):
        return not self.wl

    def get_length(self):
        return len(self.wl)


class WLS():
    def __init__(self):
        self.Line1 = WL(1)
        self.Line2 = WL(2)

    def arrive(self, member):
        if self.Line1.arrive(member):
            return None
        self.Line2.arrive(member)

    def leave(self):
        if self.Line1.is_empty():
            return self.Line2.leave()
        return self.Line1.leave()

    def is_empty(self):
        return self.Line1.is_empty() and self.Line2.is_empty()

    def get_length(self):
        return self.Line1.get_length() + self.Line2.get_length()
