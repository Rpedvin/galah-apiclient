#!/usr/bin/env python

# internal
import galah.apiclient.lib.config2 as config2
import galah.apiclient.lib.config_options as config_options

# stdlib
import unittest
import sys

# Shorter names to make creating the expected results easier
class TestConfig(unittest.TestCase):
    def setUp(self):
        self.argparser = config2.create_argparser(config_options.get_actions())
        
        # argparser.parse_args will output a lot of stuff to stderr and I don't
        # want to go through the trouble of silencing it when this is a lot
        # simpler.
        print >> sys.stderr, "--next test starting, ignore output--"

    def test_host(self):
        bad_hosts = [
            "badness",
            "ftp://badness",
            "ftp://http://badness",
            "fireball",
            "htttp://cucumber",
            "http:/bad",
            "http://",
            "https://"
        ]
        for i in bad_hosts:
            self.assertRaises(SystemExit, self.argparser.parse_args,
                ["--host", i])
                
        good_hosts = [
            "http://h",
            "http://https",
            "https://www.google.com",
            "http://www.google.com",
            "http://hamster.destructionator.edu.slamm.applesauce",
            "https://destruction"
        ]
        for i in good_hosts:
            try:
                args = self.argparser.parse_args(["--host", i])
            except SystemExit:
                self.fail("Validation failure on good host '%s'." % (i, ))
            self.assertEquals(args.host, i)

if __name__ == '__main__':
    unittest.main()
