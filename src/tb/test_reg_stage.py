import os 

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_tools.runner import get_runner

import pytest

from tools.test_utils.bits_math import BitsMath
from tools.test_utils.expect_queue import ExpectQueue
from tools.test_utils.interfaces.valid_interface import ValidDriver, ValidMonitor

import logging

log = logging.getLogger("cocotb")

@cocotb.test()
async def reg_stage(dut):
    clock = Clock(dut.clk_i, 10)
    cocotb.start_soon(clock.start(start_high=False))

    monitor = ValidMonitor(dut)
    driver = ValidDriver(dut)
    expect_queue = ExpectQueue()
    cocotb.start_soon(monitor.monitor(expect_queue))
    await RisingEdge(dut.clk_i)

    for _ in range(200):
        # Every cycle send a new valid value and expect to receive it later on the monitor. 
        stim = BitsMath.random(dut.DATA_WIDTH.value)
        expect_queue.expect(stim)
        await driver.drive(stim)

    for _ in range(2): await RisingEdge(dut.clk_i) # Wait for all events to come out of the DUT

    expect_queue.teardown() # Call teardown to make sure the queue is empty after each iteration

@pytest.mark.parametrize(
    "parameters", [
        {"DATA_WIDTH": "1"},
        {"DATA_WIDTH": "32"}
    ]
)
def test_reg_stage(parameters):
    proj_path = os.path.dirname(os.path.dirname(__file__))

    sources = [os.path.abspath(os.path.join(proj_path, "hdl", "reg_stage.vhd"))]

    runner = get_runner("ghdl")
    runner.build(
        sources=sources,
        build_args=["--std=08"],
        hdl_toplevel="reg_stage",
        always=True,
    )

    runner.test(
        hdl_toplevel="reg_stage",
        test_module="src.tb.test_reg_stage",
        test_args=["--std=08"],
        plusargs=[f"-g{k}={v}" for k, v in parameters.items()] + [f"--wave=test_reg_stage{''.join(e for e in f'{parameters}' if e.isalnum())}.ghw"]
    )

