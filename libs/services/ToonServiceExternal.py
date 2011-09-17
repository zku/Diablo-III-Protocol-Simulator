#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ToonServiceExternal(BaseService):
  def __init__(self):
    super(ToonServiceExternal, self).__init__('ToonServiceExternal', 0xdeadbeef)
    self.rpc[0x01] = self.ToonList
    self.rpc[0x02] = self.SelectToon
    self.rpc[0x03] = self.CreateToon
    self.rpc[0x04] = self.DeleteToon

  def ToonList(self, packet):
    request = Utils.LoadRequest(toon_external.ToonListRequest(), packet)
    response = toon_external.ToonListResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def SelectToon(self, packet):
    request = Utils.LoadRequest(toon_external.SelectToonRequest(), packet)
    response = toon_external.SelectToonResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def CreateToon(self, packet):
    request = Utils.LoadRequest(toon_external.CreateToonRequest(), packet)
    response = toon_external.CreateToonResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def DeleteToon(self, packet):
    request = Utils.LoadRequest(toon_external.DeleteToonRequest(), packet)
    response = toon_external.DeleteToonResponse()
    return self.PerformRpc(0x04, request, response, packet)