#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class UserManagerNotify(BaseService):
  def __init__(self):
    super(UserManagerNotify, self).__init__('UserManagerNotify', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyPlayerBlocked
    self.rpc[0x02] = self.NotifyPlayerBlockRemoved

  def NotifyPlayerBlocked(self, packet):
    request = Utils.LoadRequest(user_manager.BlockedPlayerNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)

  def NotifyPlayerBlockRemoved(self, packet):
    request = Utils.LoadRequest(user_manager.BlockedPlayerNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)