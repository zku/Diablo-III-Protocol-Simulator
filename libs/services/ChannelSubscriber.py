#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ChannelSubscriber(BaseService):
  def __init__(self):
    super(ChannelSubscriber, self).__init__('ChannelSubscriber', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyAdd
    self.rpc[0x02] = self.NotifyJoin
    self.rpc[0x03] = self.NotifyRemove
    self.rpc[0x04] = self.NotifyLeave
    self.rpc[0x05] = self.NotifySendMessage
    self.rpc[0x06] = self.NotifyUpdateChannelState
    self.rpc[0x07] = self.NotifyUpdateMemberState

  def NotifyAdd(self, packet):
    request = Utils.LoadRequest(channel.AddNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)

  def NotifyJoin(self, packet):
    request = Utils.LoadRequest(channel.JoinNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)

  def NotifyRemove(self, packet):
    request = Utils.LoadRequest(channel.RemoveNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x03, request, response, packet)

  def NotifyLeave(self, packet):
    request = Utils.LoadRequest(channel.LeaveNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x04, request, response, packet)

  def NotifySendMessage(self, packet):
    request = Utils.LoadRequest(channel.SendMessageNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x05, request, response, packet)

  def NotifyUpdateChannelState(self, packet):
    request = Utils.LoadRequest(channel.UpdateChannelStateNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x06, request, response, packet)

  def NotifyUpdateMemberState(self, packet):
    request = Utils.LoadRequest(channel.UpdateMemberStateNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x07, request, response, packet)