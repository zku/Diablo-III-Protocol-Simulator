#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class SearchService(BaseService):
  def __init__(self):
    super(SearchService, self).__init__('SearchService', 0xdeadbeef)
    self.rpc[0x01] = self.FindMatches
    self.rpc[0x02] = self.SetObject
    self.rpc[0x03] = self.RemoveObjects

  def FindMatches(self, packet):
    request = Utils.LoadRequest(search.FindMatchesRequest(), packet)
    response = search.FindMatchesResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def SetObject(self, packet):
    request = Utils.LoadRequest(search.SetObjectRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)

  def RemoveObjects(self, packet):
    request = Utils.LoadRequest(search.RemoveObjectsRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x03, request, response, packet)