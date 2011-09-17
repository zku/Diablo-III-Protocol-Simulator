#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ChatService(BaseService):
  def __init__(self):
    super(ChatService, self).__init__('ChatService', 0xdeadbeef)
    self.rpc[0x01] = self.FindChannel
    self.rpc[0x02] = self.CreateChannel
    self.rpc[0x03] = self.JoinChannel

  def FindChannel(self, packet):
    request = Utils.LoadRequest(channel.FindChannelRequest(), packet)
    response = channel.FindChannelResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def CreateChannel(self, packet):
    request = Utils.LoadRequest(channel.CreateChannelRequest(), packet)
    response = channel.CreateChannelResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def JoinChannel(self, packet):
    request = Utils.LoadRequest(channel.JoinChannelRequest(), packet)
    response = channel.JoinChannelResponse()
    return self.PerformRpc(0x03, request, response, packet)