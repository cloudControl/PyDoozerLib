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


class PyDoozerLib(object):

    def __init__(self, host, port):
        super(PyDoozerLib, self).__init__()
        self.sock = None

        self.host = host
        self.port = port
        self.addr = (host, port)

    def connect(self):
        if self.sock:
            self.disconnect()

        self.sock = socket.socket()
        self.sock.connect(self.addr)

    def disconnect(self):
        self.sock.close()
        self.sock = None

    #noinspection PyUnresolvedReferences
    def get(self, doozer_path):
        request = Request(path=doozer_path, verb=Request.GET)
        if not self.send_proto_request(request):
            return False

        return self.get_proto_response()

    def send_proto_request(self, request):
        if not self.sock:
            self.connect()

        request.tag = 0
        data = request.SerializeToString()
        head = struct.pack(">I", len(data))
        packet = ''.join([head, data])
        try:
            self.sock.send(packet)
        except IOError:
            return False
        return True

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
            return response.value
        except IOError:
            return None
        except struct.error:
            return None
        finally:
            self.sock.close()
