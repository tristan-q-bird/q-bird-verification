# Quickstart Guide

This repo contains VHDL examples and associated tests written in python with cocotb. It's intended to provide an environment for testing FPGA candidates.

## Step 1: Environment setup

This repo is intended to be run on some flavour of Linux or Unix.

### Python environment

* Create a new python venv: `python3 -m venv venv`
* Activate your new environment: `source venv/bin/activate`
* Install the required packages from `requirements.txt`: `pip install -r tools/requirements.txt`

### Install a simulator

* Install GHDL (an open source VHDL simulator) via whatever method you like (see https://ghdl.github.io/ghdl/getting.html or https://github.com/ghdl/ghdl?tab=readme-ov-file#getting-ghdl)
* Be careful when installing GHDL from package managers: you can get quite stale versions which could have missing features
* This guide was written and tested using GHDL version v5.1.1 installed via `brew install ghdl`

### Install a wave viewer

* The tests produce `.ghw` wave files in the `sim_build` folder.
* Install GTKWave (https://gtkwave.sourceforge.net/) which will allow you to view these `.ghw` files
* This guide was written and tested using GTKWave version v3.3.103 installed via a package manager

## Step 2: Run a test to validate your setup

The entry point for all tests is through `pytest` (https://docs.pytest.org/en/7.1.x/contents.html) which can be run from the top level of this repo. 

### Some useful `pytest` basics:

* `pytest --collect-only`: just find all the tests and print a list
* `pytest -k "<EXPRESSION>"`: run all tests whose name matches `EXPRESSION`. e.g. `pytest -k "pipe"`
* `pytest -s`: run all tests and output stdout to the terminal (normally stdout is suppressed). Can be used with `-k`

### Some useful `cocotb` extras:

* `COCOTB_LOG_LEVEL=DEBUG pytest -s`: run all tests with the loggers set to `DEBUG` level and output the results to stdout

### Run a test

Run `pytest -k "test_reg_stage"` to make sure your setup works. You should see a report like this:
```
examples/tb/test_reg_stage.py ..                                                                                                                                                                                                                   [100%]

============================================================================================================ 2 passed, 5 deselected in 2.77s =============================================================================================================
```

* Check that your wave viewer is set up correctly:
    * Run `gtkwave sim_build/test_pipeDATAWIDTH1PIPEDEPTH5.ghw` to open the GTKWave GUI with a wavefile loaded.
    * Right click on the `top` node in the `SST` window on the left of the GTKWave GUI and select `Recurse Import -> Insert` to add the waves to the wave viewer panel
    * Have a look through the waves and check that they look like a pipe with depth 5 and width 1

## Step 3: Create a new module and testbench

* Copy `valid_ready_passthrough.vhd` to `src/hdl/` and `test_valid_ready_passthrough.py` to `src/tb`. Give them names that reflect your new module's purpose, depending on the task you've been given by the tester.
* Update the name of the your new module in the `*.vhd` file you just copied. Make it the same as the filename, without the `.vhd` extension.
* Update the name of the test function and all the paths, DUT names, and module references in the `*.py` test file you just copied (just search for `valid_ready_passthrough` and you should find all the places that need to change)
* Run your new test on your new module to make sure all the plumbing is in place: `pytest -k "<your_test_name>"`
* Start implementing actual new functionality and tests!
