#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class PartyService(BaseService):
  def __init__(self):
    super(PartyService, self).__init__('PartyService', 0xdeadbeef)
    self.rpc[0x01] = self.CreateChannel
    self.rpc[0x02] = self.JoinChannel
    self.rpc[0x03] = self.GetChannelInfo

  def CreateChannel(self, packet):
    request = Utils.LoadRequest(channel_types.CreateChannelRequest(), packet)
    response = channel_types.CreateChannelResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def JoinChannel(self, packet):
    request = Utils.LoadRequest(channel_types.JoinChannelRequest(), packet)
    response = channel_types.JoinChannelResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def GetChannelInfo(self, packet):
    request = Utils.LoadRequest(channel_types.GetChannelInfoRequest(), packet)
    response = channel_types.GetChannelInfoResponse()
    return self.PerformRpc(0x03, request, response, packet)