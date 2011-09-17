#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class FollowersNotify(BaseService):
  def __init__(self):
    super(FollowersNotify, self).__init__('FollowersNotify', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyFollowerRemoved

  def NotifyFollowerRemoved(self, packet):
    request = Utils.LoadRequest(followers.FollowerNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)