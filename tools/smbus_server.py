# -*- coding: utf-8 -*-
"""
This server uses smbus module.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from smbus_proxy import proxy_server
import time
import smbus
from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--ip', dest='ip_to_listen',
                      help='ip and port to listen: "ip:port"', )
    (options, args) = parser.parse_args()

    if not options.ip_to_listen:
        raise Exception('ip and port to listen are mandatory')

    try:
        server = proxy_server.ProxyServer(options.ip_to_listen, smbus.SMBus)
        server.serve()
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop()
