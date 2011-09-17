#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class AuthenticationServer(BaseService):
  def __init__(self):
    super(AuthenticationServer, self).__init__('AuthenticationServer', 0xdeadbeef)
    self.rpc[0x01] = self.Logon
    self.rpc[0x02] = self.ModuleMessage

  def Logon(self, packet):
    request = Utils.LoadRequest(authentication.LogonRequest(), packet)
    response = authentication.LogonResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def ModuleMessage(self, packet):
    request = Utils.LoadRequest(authentication.ModuleMessageRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)