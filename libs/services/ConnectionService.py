#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ConnectionService(BaseService):
  def __init__(self):
    super(ConnectionService, self).__init__('ConnectionService', 0xdeadbeef)
    self.rpc[0x01] = self.Connect
    self.rpc[0x02] = self.Bind
    self.rpc[0x03] = self.Echo
    self.rpc[0x04] = self.ForceDisconnect
    self.rpc[0x05] = self.Null
    self.rpc[0x06] = self.Encrypt
    self.rpc[0x07] = self.RequestDisconnect

  def Connect(self, packet):
    request = Utils.LoadRequest(connection.ConnectRequest(), packet)
    response = connection.ConnectResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def Bind(self, packet):
    request = Utils.LoadRequest(connection.BindRequest(), packet)
    response = connection.BindResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def Echo(self, packet):
    request = Utils.LoadRequest(connection.EchoRequest(), packet)
    response = connection.EchoResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def ForceDisconnect(self, packet):
    request = Utils.LoadRequest(connection.DisconnectNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x04, request, response, packet)

  def Null(self, packet):
    request = Utils.LoadRequest(connection.NullRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x05, request, response, packet)

  def Encrypt(self, packet):
    request = Utils.LoadRequest(connection.EncryptRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x06, request, response, packet)

  def RequestDisconnect(self, packet):
    request = Utils.LoadRequest(connection.DisconnectRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x07, request, response, packet)