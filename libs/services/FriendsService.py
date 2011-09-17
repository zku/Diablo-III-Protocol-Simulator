#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class FriendsService(BaseService):
  def __init__(self):
    super(FriendsService, self).__init__('FriendsService', 0xdeadbeef)
    self.rpc[0x01] = self.SubscribeToFriends
    self.rpc[0x02] = self.SendInvitation
    self.rpc[0x03] = self.AcceptInvitation
    self.rpc[0x04] = self.RevokeInvitation
    self.rpc[0x05] = self.DeclineInvitation
    self.rpc[0x06] = self.IgnoreInvitation
    self.rpc[0x07] = self.RemoveFriend
    self.rpc[0x08] = self.ViewFriends
    self.rpc[0x09] = self.UpdateFriendState
    self.rpc[0x0a] = self.UnsubscribeToFriends

  def SubscribeToFriends(self, packet):
    request = Utils.LoadRequest(friends.SubscribeToFriendsRequest(), packet)
    response = friends.SubscribeToFriendsResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def SendInvitation(self, packet):
    request = Utils.LoadRequest(invitation.SendInvitationRequest(), packet)
    response = invitation.SendInvitationResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def AcceptInvitation(self, packet):
    request = Utils.LoadRequest(invitation.GenericRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x03, request, response, packet)

  def RevokeInvitation(self, packet):
    request = Utils.LoadRequest(invitation.GenericRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x04, request, response, packet)

  def DeclineInvitation(self, packet):
    request = Utils.LoadRequest(invitation.GenericRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x05, request, response, packet)

  def IgnoreInvitation(self, packet):
    request = Utils.LoadRequest(invitation.GenericRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x06, request, response, packet)

  def RemoveFriend(self, packet):
    request = Utils.LoadRequest(friends.GenericFriendRequest(), packet)
    response = friends.GenericFriendResponse()
    return self.PerformRpc(0x07, request, response, packet)

  def ViewFriends(self, packet):
    request = Utils.LoadRequest(friends.ViewFriendsRequest(), packet)
    response = friends.ViewFriendsResponse()
    return self.PerformRpc(0x08, request, response, packet)

  def UpdateFriendState(self, packet):
    request = Utils.LoadRequest(friends.UpdateFriendStateRequest(), packet)
    response = friends.UpdateFriendStateResponse()
    return self.PerformRpc(0x09, request, response, packet)

  def UnsubscribeToFriends(self, packet):
    request = Utils.LoadRequest(friends.UnsubscribeToFriendsRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x0a, request, response, packet)