import selectors
import socket
from enum import Enum, IntEnum, auto
from string import digits, ascii_letters
import re
import hashlib
from typing import List, Callable
from string import ascii_letters, digits
from random import choices


class HandshakeError(Exception):
    """Raised when there is an error with the handshake.
    """
    def __init__(self, errno: int, reason: str) -> None:
        super().__init__(reason)
        self.errno = errno
    
    def __str__(self):
        return f"E{self.errno}: {super().__str__()}"


class HandshakeStage(Enum):
    """Handshake stage for HandshakeProtocol."""
    INITIAL_STAGE = auto() 

    # non-gps device, and has not received any device names yet.
    DEVICE_NAMES_EXPECTED = auto() 
    # non-gps device. Have subscribed to at least one device.
    DEVICE_NAMES_OR_BEGIN_EXPECTED = auto() 

    # gps-device
    DEVICE_NAME_RECEIVED = auto() 
    # gps-device
    SESSION_ID_RECEIVED = auto() 
    BEGIN_RECEIVED = auto() # Finalize handshake and begin transmission.


class ProtocolErrorCode(IntEnum):
    WRONG_CHALLENGE_OR_INVALID_DEVICE_NAME = auto()
    INVALID_DEVICE_NAME = auto()
    CODE_TOOK_UNEXPECTED_EXECUTION_PATH = auto()
    INVALID_SESSION_ID = auto()  # Does not match regex?


class HandshakeProtocol:
    """Handshake
    
    Handshake starts by Client introducing itself with its device name. Device name is
    a string with maximum length of 12 characters. ASCII alphabet characters and numbers
    are OK. Server responds with `ok`, and Client can send the next line. That should be
    the session identifier. Session identifier is a 6 characters long string consisting
    of ASCII alphanumerics. It should be randomly generated every time on device boot up.
    Below is an example of starting a connection from gps device.
    S<- <Randomly generated string longer than maximum device name length>
    C-> device name
    S<- ok
    C-> ABC123
    S<- ok
    C-> begin
    S<- ok, waiting for GPS data.

    Device name is used to identify the device. Session id string should be generated
    every time a device boots up.

    That concludes the handshake for gps-device<->server. Should a problem occur, the
    server is responsible for returning a string describing the problem. Such message
    will begin with E<error_code> where error_code is an integer between 0-255.

    Handshake for non-gps device.

    S<- <Randomly generated string longer than maximum device name length>
    C-> <Calculating response string defined below>
    S<- ok, non-gps device connected
    C-> device_name1
    S<- ok
    C-> device_name2
    S<- ok
    C-> begin
    S<- beginning

    Calculating response string:
    Reply with MD5 checksum of the value. Crude, but it's a crude app.
    """

    session_identiefier_re = re.compile(r"[a-zA-Z0-9]{6}$")
    _legal_device_name_re = re.compile(r"[a-zA-Z0-9]{3,12}$")

    def __init__(self) -> None:
        self._challenge_s = "".join(choices(ascii_letters + digits, k=30))
        self._challenge_s_md5 = hashlib.md5(self._challenge_s.encode("utf-8")).hexdigest()
        self._device_name: None|str = None # For gps clients.
        self._subscribed_devices: List = []  # For computer clients.
        self._session_identifier: None|str = None # For gps clients, detect disconnects.
        self._is_gps: bool = True  # Assume gps unless client answers the challenge.
        self._state = HandshakeStage.INITIAL_STAGE

    def process(self, command="") -> str:
        match self._state:
            # Challenge phase.
            case HandshakeStage.INITIAL_STAGE:
                # No command means nothing has been sent yet, not even challenge string
                # to the client.
                if not command:
                    return self._challenge_s
                # Got reply to challenge or a device name if it's a gps-device.
                else:
                    self._check_challenge(command)
                    # It's a computer.
                    if self._state == HandshakeStage.DEVICE_NAMES_EXPECTED:
                        return "ok, non-gps device connected"
                    # It's a gps
                    else:
                        return "ok"
            case HandshakeStage.DEVICE_NAMES_EXPECTED:
                # It's a computer, and no subscribed device names have been inputted.
                self._device_names_expected(command)
                return "ok"
            case HandshakeStage.DEVICE_NAMES_OR_BEGIN_EXPECTED:
                self._device_names_or_begin_expected(command)
                return "beginning" if self._state == HandshakeStage.BEGIN_RECEIVED else "ok"
            case HandshakeStage.DEVICE_NAME_RECEIVED:
                # Session id expected.
                self._session_id_expected(command)
                return "ok" # No reply to given device name.
            case HandshakeStage.SESSION_ID_RECEIVED:
                # Begin expected.
                if command.lower() == "begin":
                    self._state = HandshakeStage.BEGIN_RECEIVED
                    return "ok, waiting for GPS data."
                return ""  # No reply to given session id.
            case HandshakeStage.BEGIN_RECEIVED:
                # Handshake is complete, do nothing.
                return "beginning"
            case _:
                raise HandshakeError(ProtocolErrorCode.CODE_TOOK_UNEXPECTED_EXECUTION_PATH,
                "It's a bug. Wee. Shit happens.")
    
    def _session_id_expected(self, command) -> HandshakeStage:
        """Client is gps. Set session_id internally, and await begin -command."""
        if self.session_identiefier_re.match(command):
            self._session_identifier = command
            self._state = HandshakeStage.SESSION_ID_RECEIVED
            return HandshakeStage.SESSION_ID_RECEIVED
        else:
            raise HandshakeError(ProtocolErrorCode.INVALID_SESSION_ID, "Session id must match regex '^[a-zA-Z0-9]{6}$'")

    def _check_challenge(self, challenge_response: str) -> HandshakeStage:
        """Return handshake state. If client is a desktop, then DEVICE_NAMES_EXPECTED
        is being returned. Otherwise return DEVICE_NAME_EXPECTED.
        """
        # It's a desktop or a phone app.
        if self._challenge_s_md5 == challenge_response:
            self._is_gps = False
            self._state = HandshakeStage.DEVICE_NAMES_EXPECTED
            return self._state
        # It's a gps device, and now a device name is expected.
        elif self._legal_device_name_re.match(challenge_response):
            self._state = HandshakeStage.DEVICE_NAME_RECEIVED
            return self._state
        # No valid device name was given.
        else:
            raise HandshakeError(
                ProtocolErrorCode.WRONG_CHALLENGE_OR_INVALID_DEVICE_NAME,
                "If you're a GPS, then your device name is invalid (3-12 chars, letters and numbers only.) Else your challenge was incorrect.")
    
    def _device_names_expected(self, command: str) -> HandshakeStage:
        """When no subscribed device names have been inputted yet.
        
        Computer client.
        """
        if self._legal_device_name_re.match(command):
            self._state = HandshakeStage.DEVICE_NAMES_OR_BEGIN_EXPECTED
            self._subscribed_devices.append(command)
            return self._state
        else:
            raise HandshakeError(ProtocolErrorCode.INVALID_DEVICE_NAME, "Invalid device name.")

    def _device_names_or_begin_expected(self, command: str) -> HandshakeStage:
        """When at least one subscribed device has been inputted.
        
        Computer client."""
        if command.lower() == "begin" and self._subscribed_devices:
            self._state = HandshakeStage.BEGIN_RECEIVED
            return self._state
        elif self._legal_device_name_re.match(command):
            self._subscribed_devices.append(command)
            return self._state
        else:
            raise HandshakeError(ProtocolErrorCode.INVALID_DEVICE_NAME, "Invalid device name.")
    


sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

def start_server(addr, port):
    sock = socket.socket()
    sock.bind((addr, port))
    sock.listen(5)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)
    print(f"Listening to {addr}:{port} ...")

    while True:
        events = sel.select()
        for key, mask in events:
            print(key)
            callback = key.data
            callback(key.fileobj, mask)
