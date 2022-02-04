from dataclasses import dataclass


@dataclass
class FREE_STAT:
    QUEUE_AND_CORE_WORKING = 0
    QUEUE_WORKING = 1
    CORE_WORKING = 2
    NO_WORKING = 3
