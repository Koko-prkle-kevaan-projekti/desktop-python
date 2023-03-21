from hashlib import md5
import unittest
from tassu_tutka import socket_server

"""
    S<- <Randomly generated string longer than maximum device name length>
    C-> device name
    S<- ok
    C-> ABC123
    S<- ok
    C-> begin
    S<- ok, waiting for GPS data.
"""

"""
    S<- <Randomly generated string longer than maximum device name length>
    C-> <Calculating response string defined below>
    S<- ok, non-gps device connected
    C-> device_name1
    S<- ok
    C-> device_name2
    S<- ok
    C-> begin
    S<- beginning
"""

class TestProtocolHandshake(unittest.TestCase):

    def test_gps_client_normal_operation(self):
        """Test when everything should go OK."""
        instance = socket_server.HandshakeProtocol()
        
        # Get challenge and ignore it.
        var = instance.process()
        self.assertEqual(len(var), 30, msg=f"Not a challenge: {var}")

        # Feed device name. Should get back "ok"
        var = instance.process("apila")
        self.assertEqual(var, "ok", f"Unexpected response to device name: {var}")

        # Feed session name. Should get back "ok"
        var = instance.process("123456")
        self.assertEqual(var, "ok", f"Unexpected response to session id: {var}")

        # Feed begin
        var = instance.process("begin")
        self.assertEqual(var, "ok, waiting for GPS data.",
                         f"Unexpected response to begin for gps device: {var}")
    
    def test_computer_client_normal_operation(self):
        instance = socket_server.HandshakeProtocol()
        
        # Get challenge. Challenge len is tested by another test.
        var = instance.process()

        # Respond to challenge
        response = md5(var.encode('utf-8')).hexdigest()
        var = instance.process(response)
        self.assertEqual(var, "ok, non-gps device connected", "Responding to challenge went awry for computer client.")

        # subscribe to 3 imaginary device names.
        var = instance.process("FOO")
        self.assertEqual(var, "ok", "Subscribing to devices should produce ok on each entry.")

        var = instance.process("BAR")
        self.assertEqual(var, "ok", "Subscribing to devices should produce ok on each entry.")

        var = instance.process("BAZ")
        self.assertEqual(var, "ok", "Subscribing to devices should produce ok on each entry.")

        # Send begin and end the handshake.
        var = instance.process("begin")
        self.assertEqual(var, "beginning", "begin should start the transmission.")
