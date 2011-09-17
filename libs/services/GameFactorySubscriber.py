#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class GameFactorySubscriber(BaseService):
  def __init__(self):
    super(GameFactorySubscriber, self).__init__('GameFactorySubscriber', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyGameFound

  def NotifyGameFound(self, packet):
    request = Utils.LoadRequest(game_master.GameFoundNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)