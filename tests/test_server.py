# -*- coding: utf-8 -*-

from smbus_proxy import proxy_server
import time
import array


class SMBus_test:
    """
    This class simulates i2c device
    """
    def __init__(self, bus):
        self.bus = bus
        self.hardware = dict({0x50: bytearray(b'\x00\x00\x00'), 0x60: array.array('L', [0, 0, 0])})
        print('SMBus_test: constructor')

    def read_byte(self, i2c_addr):
        print('SMBus_test: read_byte')
        if i2c_addr in self.hardware:
            return (self.hardware[i2c_addr])[0]
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def write_byte(self, i2c_addr, value):
        print('SMBus_test: write_byte')
        if i2c_addr in self.hardware:
            (self.hardware[i2c_addr])[0] = value & 0xff
        else:
            raise(Exception('addr 0x%02x doesn t exist'% i2c_addr))

    def read_byte_data(self, i2c_addr, register):
        print('SMBus_test: read_byte_data')
        if i2c_addr in self.hardware:
            return (self.hardware[i2c_addr])[register]
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def write_byte_data(self, i2c_addr, register, value):
        if i2c_addr in self.hardware:
            (self.hardware[i2c_addr])[register] = value & 0xff
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def read_word_data(self, i2c_addr, register):
        print('SMBus_test: read_word_data')
        if i2c_addr in self.hardware:
            return (self.hardware[i2c_addr])[register] & 0xffff
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def write_word_data(self, i2c_addr, register, value):
        print('SMBus_test: write_word_data')
        if i2c_addr in self.hardware:
            (self.hardware[i2c_addr])[register] = value & 0xffff
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def read_i2c_block_data(self, i2c_addr, register):
        print('SMBus_test: read_i2c_block_data')
        if i2c_addr in self.hardware:
            return self.hardware[i2c_addr]
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))

    def write_i2c_block_data(self, i2c_addr, register, data):
        print('SMBus_test: write_i2c_block_data')
        if i2c_addr in self.hardware:
                self.hardware[i2c_addr] = data
        else:
            raise (Exception('addr 0x%02x doesn t exist' % i2c_addr))


def test_server():
    """
    This function creates and runs a server
    :return:
    """
    server = proxy_server.ProxyServer('[::]:50051', SMBus_test, 5)
    server.serve()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop()

    print('Done')


if __name__ == '__main__':
    test_server()




