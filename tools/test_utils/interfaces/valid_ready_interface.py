from tools.test_utils.metaclasses import MultipleMeta
from cocotb.handle import HierarchyObject, ValueObjectBase
from cocotb.triggers import RisingEdge, ReadOnly, NextTimeStep
from tools.test_utils.bits_math import BitsMath
import logging
import random

log = logging.getLogger("cocotb")

class ValidReadyDriver(metaclass=MultipleMeta):
    def __init__(self, clk:ValueObjectBase, data:ValueObjectBase, valid: ValueObjectBase, ready: ValueObjectBase, name:str="valid_driver"):
        self.clk = clk
        self.data = data
        self.valid = valid
        self.ready = ready
        self.name = name
        self.clear()

    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="valid_driver"):
        self.clk = getattr(dut, f"clk_i")
        self.data = getattr(dut, f"{prefix}data_i")
        self.valid = getattr(dut, f"{prefix}valid_i")
        self.ready = getattr(dut, f"{prefix}ready_o")
        self.name = name
        self.clear()

    def clear(self):
        self.data.value = BitsMath.random(len(self.data))
        self.valid.value = 0

    async def drive(self, stim):
        log.debug(f"{self.name}: driving {stim}")
        self.data.value = stim
        self.valid.value = 1
        await RisingEdge(self.clk)
        while not self.ready.value:
            await RisingEdge(self.clk)
        self.clear()

class ValidReadyMonitor(metaclass=MultipleMeta):
    def __init__(self, clk:ValueObjectBase, data:ValueObjectBase, valid: ValueObjectBase, ready: ValueObjectBase, name:str="valid_monitor"):
        self.clk = clk
        self.data = data
        self.valid = valid
        self.ready = ready
        self.name = name  
        self.clear()
 
    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="valid_monitor"):
        self.clk = getattr(dut, f"clk_i")
        self.data = getattr(dut, f"{prefix}data_o")
        self.valid = getattr(dut, f"{prefix}valid_o")
        self.ready = getattr(dut, f"{prefix}ready_i")
        self.name = name
        self.clear()

    def clear(self):
        self.ready.value = 0

    async def recv(self):
        log.debug(f"{self.name}: starting recv")
        while True:
            await ReadOnly()  # Wait to sample valid until the DUT has settled after the rising edge
            if self.valid.value:
                # Now we are in the ReadOnly phase so we need to wait for the NextTimeStep phase to set ready
                await NextTimeStep()
                for _ in range(random.randint(0, 3)):
                    await RisingEdge(self.clk)

                self.ready.value = 1

                log.debug(f"{self.name}: received {self.data.value} with type {type(self.data.value)}")
                yield self.data.value
            
            await RisingEdge(self.clk)
            self.clear()

    async def monitor(self, expect_queue):
        log.debug(f"{self.name}: starting monitor")
        async for actual in self.recv():
            expect_queue.check(actual)
