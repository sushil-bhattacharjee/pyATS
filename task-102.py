from genie.testbed import load
from pprint import pprint
import logging

# Suppress Unicon CLI and logging outputs
logging.getLogger('unicon').setLevel(logging.CRITICAL)

# Load the testbed file
testbed = load('testbed-chapter-10.yml')

# Connect all devices without printing logs
testbed.connect(log_standout=False)

# For each device in the testbed
for device in testbed.devices.values():
    #Learn the Platform information
    platform = device.learn('platform')
    
    # Extract required field details
    hostname = device.name
    version = platform.version
    issu_state = platform.issu_rollback_timer_state
    
    # Print the result
    print(f"{hostname} {version} {issu_state}")