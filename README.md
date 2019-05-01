# smbus-proxy

The goal of this project is to facilitate the development of i2c driver from Raspberry. 

<pre>
+----------------+           +-------------+
|                |           |             |
|     Remote     | <-------> |  Raspberry  |
|    Computer    |           |             |
|                |    grpc   +------+------+
+----------------+                  ^
                                    | smbus
                                    |
                                    v
                               +----+----+
                               |         |
                               |   i2c   |
                               |  device |
                               |         |
                               +---------+
</pre>
A smbus proxy server has to run on the raspberry. A smbus proxy client module has to be used in your project. 
You can develop on a remote computer, the i2c calls (eg:read_data) will be transferred through grpc to the Rasberry that do the real i2c operations.


### Examples 

#### smbus proxy server
See tools/smbus_server.py
<pre>
$ python3 test_server3.py -i '127.0.0.1:50051'
2019-05-01 11:12:44,424 :: INFO :: Server started
2019-05-01 11:12:54,397 :: INFO :: New client(abf75ade7fa77409ad59cb43212b942b) requests bus 1
2019-05-01 11:12:56,439 :: INFO :: Client(abf75ade7fa77409ad59cb43212b942b) read_i2c_block_data at 0x10 register 0xa
2019-05-01 11:13:04,439 :: INFO :: No activity from client abf75ade7fa77409ad59cb43212b942b since 5 sec delete it
</pre>

#### smbus proxy client
See examples/Si4703.py
<pre>
$ python3 Si4703_proxy.py 
0x0A = 00 00
0x0B = 00 00
0x0C = 00 00
0x0D = 00 00
0x0E = 00 00
0x0F = 00 00
0x00 = 12 42
0x01 = 12 00
0x02 = 0a 00
0x03 = 00 00
0x04 = 00 00
0x05 = 00 00
0x06 = 00 00
0x07 = 01 00
0x08 = 00 00
0x09 = 00 00
</pre>

### Other

#### List of supported operation
    rpc read_byte
    rpc write_byte
    rpc read_byte_data
    rpc write_byte_data
    rpc read_word_data
    rpc write_word_data
    rpc read_i2c_block_data
    rpc write_i2c_block_data

#### To re-generate proto run
smbus-proxy/protos/build-proto.sh

#### To run the test
smbus-proxy/test/run_tests.sh
