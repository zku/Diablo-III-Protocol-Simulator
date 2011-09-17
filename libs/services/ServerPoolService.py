#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ServerPoolService(BaseService):
  def __init__(self):
    super(ServerPoolService, self).__init__('ServerPoolService', 0xdeadbeef)
    self.rpc[0x01] = self.GetPoolState

  def GetPoolState(self, packet):
    request = Utils.LoadRequest(server_pool.PoolStateRequest(), packet)
    response = server_pool.PoolStateResponse()
    return self.PerformRpc(0x01, request, response, packet)