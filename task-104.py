import logging
from pyats import aetest
from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup1(self, testbed):
        # Connect to all devices in the test bed
        testbed.connect()
        logger.info("Welcome to JamesBond World")
    
@aetest.loop(device_name=["CE-61", "CE-62"]) # <--loop over device names
class Testcase(aetest.Testcase):
    @aetest.test
    def verify_connection(self, testbed, device_name):
        # Check if the device is connected
        assert testbed.devices[device_name].is_connected(), f"{device_name} is not connected"
        logger.info(f"{device_name} is connected successfully.")
        
# Entry point
if __name__ == "__main__":
    aetest.main(testbed=load('testbed-chapter-10.yml'))