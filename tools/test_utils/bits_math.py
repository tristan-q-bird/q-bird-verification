import random
from cocotb.types import LogicArray

class BitsMath:
    @classmethod
    def random(cls, len):
        return LogicArray("".join([random.choice(["0", "1"]) for _ in range(len)]))

    @classmethod
    def unknown(cls, len):
        return LogicArray("".join(["X" for _ in range(len)]))

    @classmethod
    def clear(cls, len):
        return LogicArray("".join(["0" for _ in range(len)]))

