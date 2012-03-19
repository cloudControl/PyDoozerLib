# -*- coding: utf-8 -*-
"""
    Copyright (c) 2012 cloudControl GmbH

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

"""
import socket
import struct
from msg_pb2 import Request, Response


#noinspection PyUnresolvedReferences
class PyDoozerLib(object):

    # STATUS CODES
    STATUS_OK = 127

    # Connection status
    is_connected = False

    def __init__(self, host, port, timeout=None):
        super(PyDoozerLib, self).__init__()
        self.connection = Connection(host=host, port=port, timeout=timeout)

    def connect(self):
        self.connection.connect()
        self.is_connected = True

    def disconnect(self):
        self.connection.disconnect()
        self.is_connected = False

    def rev(self):
        request = Request(verb=Request.REV)
        return self.connection.send(request)

    def delete(self, path, rev):
        request = Request(path=path, rev=rev, verb=Request.DEL)
        return self.connection.send(request)

    def get(self, path, rev=None):
        request = Request(path=path, verb=Request.GET)
        if rev:
            request.rev = rev
        return self.connection.send(request)

    def set(self, path, value):
        request = Request(
            path=path,
            value=value,
            rev=self.get(path).rev,
            verb=Request.SET
        )
        return self.connection.send(request)


class Connection(object):

    # Setting the default timeout to 60 seconds
    DEFAULT_TIMEOUT = 60.0

    def __init__(self, host, port, timeout=None):
        super(Connection, self).__init__()
        self.sock = None
        self.host = host
        self.port = port
        self.addr = (host, port)

        self.timeout = timeout
        if timeout is None:
            self.timeout = self.DEFAULT_TIMEOUT

    def connect(self):
        if self.sock:
            self.disconnect()

        self.sock = socket.socket()
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.addr)

    def disconnect(self):
        self.sock.close()
        self.sock = None

    def send_proto_request(self, request):
        if not self.sock:
            return None

        request.tag = 0
        data = request.SerializeToString()
        head = struct.pack(">I", len(data))
        packet = ''.join([head, data])
        try:
            rev = self.sock.send(packet)
        except IOError:
            self.disconnect()
            return None
        return rev

    #noinspection PyUnresolvedReferences
    def get_proto_response(self):
        if not self.sock:
            return None

        try:
            head = self.sock.recv(4)
            length = struct.unpack(">I", head)[0]
            data = self.sock.recv(length)
            response = Response()
            response.ParseFromString(data)
            return response
        except IOError:
            return None
        except struct.error:
            return None

    def send(self, request):
        rev = self.send_proto_request(request)
        if rev is None:
            return None
        return self.get_proto_response()
