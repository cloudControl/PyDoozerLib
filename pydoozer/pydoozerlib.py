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

    def __init__(self, host, port):
        super(PyDoozerLib, self).__init__()
        self.connection = Connection(host, port)

    def connect(self):
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def rev(self):
        request = Request(verb=Request.REV)
        return self.connection.send(request)

    def delete(self, path, rev):
        request = Request(path=path, rev=rev, verb=Request.DEL)
        return self.connection.send(request)

    def get(self, path):
        request = Request(path=path, verb=Request.GET)
        return self.connection.send(request)

    def set(self, path, value, rev):
        if self.get(path) is not "":
            print "Not empty"
            print "DELETE: {0}".format(self.delete(path, (self.get(path))[1]))

        request = Request(path=path, value=value, rev=rev, verb=Request.SET)
        resp, rev = self.connection.send(request)
        print "RESP: {0}  -- REV: {1}".format(resp, rev)
        return resp


class Connection(object):
    def __init__(self, host, port):
        super(Connection, self).__init__()
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

    def send_proto_request(self, request):
        if not self.sock:
            return None

        request.tag = 0
        data = request.SerializeToString()
        head = struct.pack(">I", len(data))
        packet = ''.join([head, data])
        rev = None
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
            return response.value
        except IOError:
            return None
        except struct.error:
            return None

    def send(self, request):
        rev = self.send_proto_request(request)
        if rev is None:
            return None
        return self.get_proto_response(), rev