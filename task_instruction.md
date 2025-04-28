Task 10.4: Testcase loop
Objective: Use class-based looping

Create a Python test script with the filename task-104.py.

Add two new empty classes that inherit from aetest.CommonSetup and aetest. Testcase respectively.
Any function that is added to these classes later must have the parameters 'self' and 'testbed' passed to them.

Inside your CommonSetup-inherited class, create a new function and decorate it with aetest.subsection. This
function must connect to all devices in the testbed.

In your Testcase-inherited class, create a new function and decorate it with aetest.test.

This aetest.test function should verify that connections are established to specific devices, using the
@aetest.loop decorator for the aetest.Testcase-inherited class and pass the list device_name = ['Router1',
'Router2']
The device_name variable should then be received in the aetest.test-decorated method (function). Use the
device_name in each iteration of the loop to verify that the specific device is connected.

Run the script like this:
$ python3 task-104.py

Verify that the pyATS report output shows the connection-status as individual tests.

Hints:
.
.
assert testbed.devices[device_name].is_connected
· testbed.connect()
. @aetest.loop(device_name=['Router1','Router2'])

pyATS documentations: https://pubhub.devnetcloud.com/media/pyats/docs/index.html
pyATS docs -> AEtest - Test Infrastructure - > Looping Sections - Loop Parameters

🛠 Solution Structure for task-104.py

import logging
from pyats import aetest
from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_devices(self, testbed):
        # Connect to all devices
        testbed.connect()
        logger.info("Connected to all devices.")

@aetest.loop(device_name=['Router1', 'Router2'])  # <-- loop over device names
class Testcase(aetest.Testcase):

    @aetest.test
    def verify_connection(self, testbed, device_name):
        # Check if device is connected
        assert testbed.devices[device_name].is_connected(), f"{device_name} is not connected"
        logger.info(f"{device_name} is connected successfully.")

# Entry point
if __name__ == "__main__":
    aetest.main(testbed=load('testbed-chapter-10.yml'))

🔥 Important Points:
Item | Details
CommonSetup | Connects to all devices at the start
@aetest.loop | Automatically runs verify_connection() once for each device (Router1, Router2)
device_name | Passed into verify_connection() each time
assert | Ensures the device is connected
logger.info() | Logs success message cleanly


################################################
Task 10.5: test loop, step
Objective: Run nested loops and steps for testing

Create a copy of your test script from task 10.4 and give it the filename task-105.py

Add a new function and decorate it with the aetest.test.loop decorator and pass it the list following list:
ping_dst=['192.168.255.1', '192.168.255.2', '192.168.255.53']

In the test function, create a for-loop and loop through the MTU sizes ['2000', '1500', '1000'] (in that order!)
Start a new section step for each MTU size, and ping the destination IP addresses using the following method:

with steps.start(f"MTU size {mtu}") as step:
testbed.devices[device_name].ping(addr=ping_dst, count=1, size=mtu, df_bit="y")

Run the script like this:
$ python3 task-105.py

It is expected that the destination 192.168.255.2 should fail for every MTU size.
The two other destinations 192.168.255.1 and 192.168.255.53 however, are supposed to fail only with MTU size
2000.

You will notice that each test iteration stops when the first failure occurs (ERRORED). This is due to the
exception thrown when the ping times out.
If you catch the Exception and manually fail the step, the result will change to FAILED.

A FAILED step will also stop the entire test function, but you can use the parameter "continue_" in the step.start()
method to modify this behavior so your report output becomes similar to the following (including all FAILED and
PASSED results)

✅ Corrected and clean version of your task-105.py:
import logging
from pyats import aetest
from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def func1(self, testbed):
        # Connect to all devices in the test bed
        testbed.connect()
        logger.info("Welcome to JamesBond World")

@aetest.loop(device_name=["CE-61", "CE-62"])
class Testcase(aetest.Testcase):

    @aetest.test
    def verify_connection(self, testbed, device_name):
        assert testbed.devices[device_name].is_connected(), f"{device_name} is not connected"
        logger.info(f"{device_name} is connected successfully.")

    @aetest.test.loop(ping_dst=['10.1.10.61', '10.1.10.62', '10.1.10.63', '10.1.10.61'])
    def ping_mtu(self, testbed, steps, device_name, ping_dst):
        for mtu in ['2000', '1500', '1000']:
            with steps.start(f"MTU size {mtu}", continue_=True) as step:
                try:
                    testbed.devices[device_name].ping(
                        addr=ping_dst,
                        count=1,
                        size=int(mtu),
                        df_bit="y"
                    )
                    logger.info(f"Ping succeeded for {ping_dst} with MTU {mtu}")
                except Exception as e:
                    logger.error(f"Ping failed for {ping_dst} with MTU {mtu}: {e}")
                    step.failed(f"Ping failed for {ping_dst} with MTU {mtu}")

# Entry point
if __name__ == "__main__":
    aetest.main(testbed=load('testbed-chapter-10.yml'))

✨ Explanation
Item | Meaning
@aetest.test.loop(ping_dst=[...]) | Loops for each destination IP
for mtu in [...] | Inside, we loop for each MTU size (2000, 1500, 1000)
with steps.start(f"MTU size {mtu}", continue_=True) | Marks each MTU test and continues even if failure
.ping() | Pings with MTU size and Don't Fragment bit set
except Exception: | Catches timeout/failure and marks step as FAILED, not ERROR
continue_=True | Very important to continue test steps even if one step fails

🧪 pyATS Test Report

2025-04-29T01:00:56: %AETEST-INFO: +------------------------------------------------------------------------------+
2025-04-29T01:00:56: %AETEST-INFO: |                               Detailed Results                               |
2025-04-29T01:00:56: %AETEST-INFO: +------------------------------------------------------------------------------+
2025-04-29T01:00:56: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2025-04-29T01:00:56: %AETEST-INFO: --------------------------------------------------------------------------------
2025-04-29T01:00:56: %AETEST-INFO: .
2025-04-29T01:00:56: %AETEST-INFO: |-- common_setup                                                          PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   `-- func1                                                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |-- Testcase[device_name=CE-61]                                           FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |-- func1[ping_dst=10.1.10.61]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 1: Ping 10.1.10.61 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 2: Ping 10.1.10.61 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   |   `-- Step 3: Ping 10.1.10.61 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   |-- func1[ping_dst=10.1.10.62]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 1: Ping 10.1.10.62 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 2: Ping 10.1.10.62 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   |   `-- Step 3: Ping 10.1.10.62 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   |-- func1[ping_dst=10.1.10.63]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 1: Ping 10.1.10.63 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO: |   |   |-- Step 2: Ping 10.1.10.63 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   |   `-- Step 3: Ping 10.1.10.63 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |   `-- func1[ping_dst=10.1.10.64]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO: |       |-- Step 1: Ping 10.1.10.64 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO: |       |-- Step 2: Ping 10.1.10.64 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: |       `-- Step 3: Ping 10.1.10.64 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: `-- Testcase[device_name=CE-62]                                           FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |-- func1[ping_dst=10.1.10.61]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 1: Ping 10.1.10.61 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 2: Ping 10.1.10.61 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     |   `-- Step 3: Ping 10.1.10.61 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     |-- func1[ping_dst=10.1.10.62]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 1: Ping 10.1.10.62 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 2: Ping 10.1.10.62 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     |   `-- Step 3: Ping 10.1.10.62 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     |-- func1[ping_dst=10.1.10.63]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 1: Ping 10.1.10.63 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO:     |   |-- Step 2: Ping 10.1.10.63 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     |   `-- Step 3: Ping 10.1.10.63 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:     `-- func1[ping_dst=10.1.10.64]                                        FAILED
2025-04-29T01:00:56: %AETEST-INFO:         |-- Step 1: Ping 10.1.10.64 with 2000                             FAILED
2025-04-29T01:00:56: %AETEST-INFO:         |-- Step 2: Ping 10.1.10.64 with 1500                             PASSED
2025-04-29T01:00:56: %AETEST-INFO:         `-- Step 3: Ping 10.1.10.64 with 1000                             PASSED
2025-04-29T01:00:56: %AETEST-INFO: +------------------------------------------------------------------------------+
2025-04-29T01:00:56: %AETEST-INFO: |                                   Summary                                    |
2025-04-29T01:00:56: %AETEST-INFO: +------------------------------------------------------------------------------+
2025-04-29T01:00:56: %AETEST-INFO:  Number of ABORTED                                                            0 
2025-04-29T01:00:56: %AETEST-INFO:  Number of BLOCKED                                                            0 
2025-04-29T01:00:56: %AETEST-INFO:  Number of ERRORED                                                            0 
2025-04-29T01:00:56: %AETEST-INFO:  Number of FAILED                                                             2 
2025-04-29T01:00:56: %AETEST-INFO:  Number of PASSED                                                             1 
2025-04-29T01:00:56: %AETEST-INFO:  Number of PASSX                                                              0 
2025-04-29T01:00:56: %AETEST-INFO:  Number of SKIPPED                                                            0 
2025-04-29T01:00:56: %AETEST-INFO:  Total Number                                                                 3 
2025-04-29T01:00:56: %AETEST-INFO:  Success Rate                                                             33.3% 
2025-04-29T01:00:56: %AETEST-INFO: --------------------------------------------------------------------------------
