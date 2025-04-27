import logging
from pyats import aetest 
from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HelloWorldSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup1(self, testbed):
        testbed.connect()
        logger.info("Welcome to hiTech007 Automation")
        
class HelloWorldTest(aetest.Testcase):
    @aetest.test
    def test1(self, testbed):
        arp = testbed.devices['CE-61'].parse("show ip arp")
        assert "192.168.61.51" in arp['interfaces']['GigabitEthernet4']['ipv4']['neighbors']
        
    @aetest.test
    def test2(self, testbed):
        ip_route = testbed.devices['CE-61'].parse("show ip route")
        assert "192.168.168.62/32" in ip_route['vrf']['default']['address_family']['ipv4']['routes']

aetest.main(testbed=load('testbed.yml'))