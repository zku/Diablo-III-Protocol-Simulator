#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ChannelOwner(BaseService):
  def __init__(self):
    super(ChannelOwner, self).__init__('ChannelOwner', 0xdeadbeef)
    self.rpc[0x01] = self.GetChannelId
    self.rpc[0x02] = self.CreateChannel
    self.rpc[0x03] = self.JoinChannel
    self.rpc[0x04] = self.FindChannel
    self.rpc[0x05] = self.GetChannelInfo

  def GetChannelId(self, packet):
    request = Utils.LoadRequest(channel_types.GetChannelIdRequest(), packet)
    response = channel_types.GetChannelIdResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def CreateChannel(self, packet):
    request = Utils.LoadRequest(channel_types.CreateChannelRequest(), packet)
    response = channel_types.CreateChannelResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def JoinChannel(self, packet):
    request = Utils.LoadRequest(channel_types.JoinChannelRequest(), packet)
    response = channel_types.JoinChannelResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def FindChannel(self, packet):
    request = Utils.LoadRequest(channel_types.FindChannelRequest(), packet)
    response = channel_types.FindChannelResponse()
    return self.PerformRpc(0x04, request, response, packet)

  def GetChannelInfo(self, packet):
    request = Utils.LoadRequest(channel_types.GetChannelInfoRequest(), packet)
    response = channel_types.GetChannelInfoResponse()
    return self.PerformRpc(0x05, request, response, packet)