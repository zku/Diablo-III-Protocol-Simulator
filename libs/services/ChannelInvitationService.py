#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ChannelInvitationService(BaseService):
  def __init__(self):
    super(ChannelInvitationService, self).__init__('ChannelInvitationService', 0xdeadbeef)
    self.rpc[0x01] = self.Subscribe
    self.rpc[0x02] = self.Unsubscribe
    self.rpc[0x03] = self.SendInvitation
    self.rpc[0x04] = self.AcceptInvitation
    self.rpc[0x05] = self.DeclineInvitation
    self.rpc[0x06] = self.RevokeInvitation
    self.rpc[0x07] = self.SuggestInvitation

  def Subscribe(self, packet):
    request = Utils.LoadRequest(channel_invitation.SubscribeRequest(), packet)
    response = channel_invitation.SubscribeResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def Unsubscribe(self, packet):
    request = Utils.LoadRequest(channel_invitation.UnsubscribeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)

  def SendInvitation(self, packet):
    request = Utils.LoadRequest(invitation.SendInvitationRequest(), packet)
    response = invitation.SendInvitationResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def AcceptInvitation(self, packet):
    request = Utils.LoadRequest(channel_invitation.AcceptInvitationRequest(), packet)
    response = channel_invitation.AcceptInvitationResponse()
    return self.PerformRpc(0x04, request, response, packet)

  def DeclineInvitation(self, packet):
    request = Utils.LoadRequest(invitation.GenericRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x05, request, response, packet)

  def RevokeInvitation(self, packet):
    request = Utils.LoadRequest(channel_invitation.RevokeInvitationRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x06, request, response, packet)

  def SuggestInvitation(self, packet):
    request = Utils.LoadRequest(channel_invitation.SuggestInvitationRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x07, request, response, packet)