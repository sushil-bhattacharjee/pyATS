import logging
from pyats import aetest
from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup1(self, testbed):
        testbed.connect()
        logger.info("Welcome to hiTech007 Automation")
        
class Testcase(aetest.Testcase):        
    @aetest.test
    def test1(self, testbed):
        connection_count = 0
        for device_name, device in testbed.devices.items():
            if device.is_connected():
                connection_count += 1
        assert connection_count == 2

aetest.main(testbed=load('testbed-chapter-10.yml'))