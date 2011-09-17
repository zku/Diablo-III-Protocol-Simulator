#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class FollowersService(BaseService):
  def __init__(self):
    super(FollowersService, self).__init__('FollowersService', 0xdeadbeef)
    self.rpc[0x01] = self.SubscribeToFollowers
    self.rpc[0x02] = self.StartFollowing
    self.rpc[0x03] = self.StopFollowing
    self.rpc[0x04] = self.UpdateFollowerState

  def SubscribeToFollowers(self, packet):
    request = Utils.LoadRequest(followers.SubscribeToFollowersRequest(), packet)
    response = followers.SubscribeToFollowersResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def StartFollowing(self, packet):
    request = Utils.LoadRequest(followers.StartFollowingRequest(), packet)
    response = followers.StartFollowingResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def StopFollowing(self, packet):
    request = Utils.LoadRequest(followers.StopFollowingRequest(), packet)
    response = followers.StopFollowingResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def UpdateFollowerState(self, packet):
    request = Utils.LoadRequest(followers.UpdateFollowerStateRequest(), packet)
    response = followers.UpdateFollowerStateResponse()
    return self.PerformRpc(0x04, request, response, packet)