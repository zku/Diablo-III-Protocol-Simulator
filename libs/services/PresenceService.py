#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class PresenceService(BaseService):
  def __init__(self):
    super(PresenceService, self).__init__('PresenceService', 0xdeadbeef)
    self.rpc[0x01] = self.Subscribe
    self.rpc[0x02] = self.Unsubscribe
    self.rpc[0x03] = self.Update
    self.rpc[0x04] = self.Query

  def Subscribe(self, packet):
    request = Utils.LoadRequest(presence.SubscribeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x01, request, response, packet)

  def Unsubscribe(self, packet):
    request = Utils.LoadRequest(presence.UnsubscribeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)

  def Update(self, packet):
    request = Utils.LoadRequest(presence.UpdateRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x03, request, response, packet)

  def Query(self, packet):
    request = Utils.LoadRequest(presence.QueryRequest(), packet)
    response = presence.QueryResponse()
    return self.PerformRpc(0x04, request, response, packet)