#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class FriendsNotify(BaseService):
  def __init__(self):
    super(FriendsNotify, self).__init__('FriendsNotify', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyFriendAdded
    self.rpc[0x02] = self.NotifyFriendRemoved
    self.rpc[0x03] = self.NotifyReceivedInvitationAdded
    self.rpc[0x04] = self.NotifyReceivedInvitationRemoved
    self.rpc[0x05] = self.NotifySentInvitationRemoved

  def NotifyFriendAdded(self, packet):
    request = Utils.LoadRequest(friends.FriendNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)

  def NotifyFriendRemoved(self, packet):
    request = Utils.LoadRequest(friends.FriendNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)

  def NotifyReceivedInvitationAdded(self, packet):
    request = Utils.LoadRequest(friends.InvitationAddedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x03, request, response, packet)

  def NotifyReceivedInvitationRemoved(self, packet):
    request = Utils.LoadRequest(friends.InvitationRemovedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x04, request, response, packet)

  def NotifySentInvitationRemoved(self, packet):
    request = Utils.LoadRequest(friends.InvitationRemovedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x05, request, response, packet)