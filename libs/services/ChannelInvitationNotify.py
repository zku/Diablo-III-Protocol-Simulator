#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ChannelInvitationNotify(BaseService):
  def __init__(self):
    super(ChannelInvitationNotify, self).__init__('ChannelInvitationNotify', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyReceivedInvitationAdded
    self.rpc[0x02] = self.NotifyReceivedInvitationRemoved
    self.rpc[0x03] = self.NotifyReceivedSuggestionAdded
    self.rpc[0x04] = self.HasRoomForInvitation

  def NotifyReceivedInvitationAdded(self, packet):
    request = Utils.LoadRequest(channel_invitation.InvitationAddedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)

  def NotifyReceivedInvitationRemoved(self, packet):
    request = Utils.LoadRequest(channel_invitation.InvitationRemovedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)

  def NotifyReceivedSuggestionAdded(self, packet):
    request = Utils.LoadRequest(channel_invitation.SuggestionAddedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x03, request, response, packet)

  def HasRoomForInvitation(self, packet):
    request = Utils.LoadRequest(channel_invitation.HasRoomForInvitationRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x04, request, response, packet)