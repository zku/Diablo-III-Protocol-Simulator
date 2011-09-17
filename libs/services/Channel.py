#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class Channel(BaseService):
  def __init__(self):
    super(Channel, self).__init__('Channel', 0xdeadbeef)
    self.rpc[0x01] = self.AddMember
    self.rpc[0x02] = self.RemoveMember
    self.rpc[0x03] = self.SendMessage
    self.rpc[0x04] = self.UpdateChannelState
    self.rpc[0x05] = self.UpdateMemberState
    self.rpc[0x06] = self.Dissolve
    self.rpc[0x07] = self.SetRoles

  def AddMember(self, packet):
    request = Utils.LoadRequest(channel.AddMemberRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x01, request, response, packet)

  def RemoveMember(self, packet):
    request = Utils.LoadRequest(channel.RemoveMemberRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)

  def SendMessage(self, packet):
    request = Utils.LoadRequest(channel.SendMessageRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x03, request, response, packet)

  def UpdateChannelState(self, packet):
    request = Utils.LoadRequest(channel.UpdateChannelStateRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x04, request, response, packet)

  def UpdateMemberState(self, packet):
    request = Utils.LoadRequest(channel.UpdateMemberStateRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x05, request, response, packet)

  def Dissolve(self, packet):
    request = Utils.LoadRequest(channel.DissolveRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x06, request, response, packet)

  def SetRoles(self, packet):
    request = Utils.LoadRequest(channel.SetRolesRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x07, request, response, packet)