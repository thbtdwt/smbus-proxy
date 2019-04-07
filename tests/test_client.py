# -*- coding: utf-8 -*-

from smbus_proxy import proxy_client
import time

import unittest

class test_client(unittest.TestCase):
    """
    Tests of client part
    """
    def test_instantiation(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)

    def test_write_read_byte(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)
        client.write_byte(0x50, 0xfe)
        self.assertEqual(client.read_byte(0x50), 0xfe)

    def test_write_read_byte_data(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)
        client.write_byte_data(0x50, 0x1, 0x3)
        self.assertEqual(client.read_byte_data(0x50, 0x1), 0x3)

    def test_write_read_word_data(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)
        client.write_word_data(0x60, 0x2, 0x1025)
        self.assertEqual(client.read_word_data(0x60, 0x2), 0x1025)

    def test_write_read_i2c_block_data(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)
        client.write_i2c_block_data(0x50, 0, bytes([0x10, 0x45, 0x17]))
        self.assertEqual(client.read_i2c_block_data(0x50, 0), bytes([0x10, 0x45, 0x17]))

    def test_error_instantiation(self):
        with self.assertRaises(Exception):
            client = proxy_client.ProxyClient('localhost:50050', 1)

    def test_error_read_byte(self):
        client = proxy_client.ProxyClient('localhost:50051', 1)
        with self.assertRaises(Exception):
            client.read_byte(0x90)


if __name__ == '__main__':
    unittest.main()

