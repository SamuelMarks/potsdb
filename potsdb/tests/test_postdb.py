from potsdb import Client
from sys import argv, exit, _getframe
from random import randint
from time import time

from unittest import TestCase, main as unittest_main

if len(argv) < 3:
    print 'usage: {0} host port'.format(argv[0])
    exit()

HOST = argv[1]
PORT = argv[2]


class TestPostDB(TestCase):
    def _0_normal_test(self):
        print _getframe().f_code.co_name
        t = Client(HOST, port=PORT)
        for x in range(100):
            extratag = str(randint(0, 1000000))
            t.log('test.metric2', randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 100)

    def _1_slow_test(self):
        print _getframe().f_code.co_name
        t = Client(HOST, port=PORT, mps=1)
        for x in xrange(10):
            extratag = str(randint(0, 1000000))
            t.log('test.metric2', randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 10)

    def _2_duplicate_test(self):
        print _getframe().f_code.co_name
        t = Client(HOST, port=PORT)
        for x in range(10):
            t.log('test.metric2', 1, cheese='blue')
        t.wait()
        assert t.queued == 1  # should not queue duplicates

    def _3_invalid_metric_test(self):
        # Attempts to send a metric with invalid name (spaces)
        print _getframe().f_code.co_name
        t = Client(HOST, port=PORT)
        self.assertRaises(AssertionError, lambda: t.log('test.metric2 roflcopter!', 1, cheese='blue'))
        self.assertEquals(t.queued, 0)
        t.stop()

    def _4_timestamp_test(self):
        # sends many metrics while specifying the timestamp
        print _getframe().f_code.co_name
        t = Client(HOST, PORT)
        ts = int(time())
        for x in range(100):
            t.log('test.metric4', 20, tag1='timestamptest', timestamp=ts)
            ts -= 1
        self.assertEquals(t.queued, 100)
        t.wait()

    def _5_qsize_test(self, size=100):
        print _getframe().f_code.co_name
        t = Client(HOST, port=PORT, qsize=size)
        for x in range(5 * size):
            extratag = str(randint(0, 1000000))
            t.log('test.metric2', randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        print "qsize was %s, sent %s" % (size, t.queued)
        self.assertGreaterEqual(t.queued, size)

    @classmethod
    def tearDownClass(cls):
        print 'done'


if __name__ == '__main__':
    unittest_main()
