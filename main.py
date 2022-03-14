#!/bin/python
import json
import random
import subprocess
from os import getenv
from time import time

import yaml

task_index = getenv("TASK_INDEX")


# JSON Logging
def log(operation, msg=None):
    print(json.dumps({"time": time(), "task_index": task_index, "operation": operation, "msg": msg}))


# Use seed to make test reproducible
if task_index:
    random.seed(int(task_index))

# Eat from 10 to 60 GB memory
memory = random.randint(1, 6) * 10

# Process blocks of 300.000 CPU operations (approx 1 min process on 8CPU, 64GB machine)
bogo_blocks = random.randint(30, 90)
bogo_ops = bogo_blocks * 300000

log("start", {"memory": memory, "bogo_blocks": bogo_blocks, "bogo_ops": bogo_ops})

# Memory allocation
log("eating_memory")
junk = [bytearray(1024 * 1024 * 1000) for r in range(memory)]

# Start CPU processing
log("cpu_stress")
cpu_stresser = subprocess.check_output(
    ["stress-ng", "--quiet", "--cpu", "8", "--cpu-ops", str(bogo_ops), "--yaml", "out.yaml", "--abort"])

# Output results
log("writing_stats")
with open('out.yaml') as file:
    log("stress_stats", yaml.load(file, Loader=yaml.FullLoader))
