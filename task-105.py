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
    
@aetest.loop(device_name=["CE-61", "CE-62"]) # <--loop over device names
class Testcase(aetest.Testcase):
    # @aetest.test
    # def verify_connection(self, testbed, device_name):
    #     # Check if the device is connected
    #     assert testbed.devices[device_name].is_connected(), f"{device_name} is not connected"
    #     logger.info(f"{device_name} is connected successfully.")
     
    @aetest.test.loop(ping_dst=['10.1.10.61', '10.1.10.62', '10.1.10.63', '10.1.10.64'])
    def func1(self, testbed, steps, device_name, ping_dst):
         for mtu in ['2000', '1500', '1000']:
             with steps.start(f"Ping {ping_dst} with {mtu}", continue_=True) as step:
                 try:
                     testbed.devices[device_name].ping(addr=ping_dst,
                                                       count=1,
                                                       size=int(mtu),
                                                       df_bit="y"
                                                       )
                     logger.info(f"Ping {ping_dst} with {mtu}")
                 except Exception as e:
                     logger.error(f"Ping {ping_dst} with {mtu}: {e}")
                     step.failed(f"Ping {ping_dst} with {mtu}")
# Entry point
if __name__ == "__main__":
    aetest.main(testbed=load('testbed-chapter-10.yml'))