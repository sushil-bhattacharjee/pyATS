import logging
from pyats import aetest 
#from genie.testbed import load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HelloWorldSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup1(self, testbed):
        testbed.connect()
        logger.info("Welcome to hiTech007 Automation")

@aetest.loop(color=["RED", "GREEN", "BLUE"])     
class HelloWorldTest(aetest.Testcase):
    @aetest.test
    def test1(self, testbed, color):
        logger.info(f"Hello {color} world from Test 1")
        assert "A" == "A"

        
    @aetest.test
    def test2(self, testbed):
        assert "A" == "B"
        
    @aetest.test.loop(word_length=[3, 4, 5, 6])
    def test3(self, testbed, color, word_length):
        assert len(color) == word_length
        
    @aetest.test 
    def test4(self, testbed, color, steps):
        for letter in ["A", "B", "C", "D", "E"]:
            with steps.start(f"Is the letter {letter} in {color}", continue_=True):
                assert letter in color


#aetest.main(testbed=load('testbed.yml'))