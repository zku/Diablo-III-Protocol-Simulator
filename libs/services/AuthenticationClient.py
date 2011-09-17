#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class AuthenticationClient(BaseService):
  def __init__(self):
    super(AuthenticationClient, self).__init__('AuthenticationClient', 0xdeadbeef)
    self.rpc[0x01] = self.ModuleLoad
    self.rpc[0x02] = self.ModuleMessage

  def ModuleLoad(self, packet):
    request = Utils.LoadRequest(authentication.ModuleLoadRequest(), packet)
    response = authentication.ModuleLoadResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def ModuleMessage(self, packet):
    request = Utils.LoadRequest(authentication.ModuleMessageRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)