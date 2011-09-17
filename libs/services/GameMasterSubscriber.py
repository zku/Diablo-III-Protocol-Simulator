#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class GameMasterSubscriber(BaseService):
  def __init__(self):
    super(GameMasterSubscriber, self).__init__('GameMasterSubscriber', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyFactoryUpdate

  def NotifyFactoryUpdate(self, packet):
    request = Utils.LoadRequest(game_master.FactoryUpdateNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)