#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class StorageService(BaseService):
  def __init__(self):
    super(StorageService, self).__init__('StorageService', 0xdeadbeef)
    self.rpc[0x01] = self.Execute
    self.rpc[0x02] = self.OpenTable
    self.rpc[0x03] = self.OpenColumn

  def Execute(self, packet):
    request = Utils.LoadRequest(storage.ExecuteRequest(), packet)
    response = storage.ExecuteResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def OpenTable(self, packet):
    request = Utils.LoadRequest(storage.OpenTableRequest(), packet)
    response = storage.OpenTableResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def OpenColumn(self, packet):
    request = Utils.LoadRequest(storage.OpenColumnRequest(), packet)
    response = storage.OpenColumnResponse()
    return self.PerformRpc(0x03, request, response, packet)