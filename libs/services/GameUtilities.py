#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class GameUtilities(BaseService):
  def __init__(self):
    super(GameUtilities, self).__init__('GameUtilities', 0xdeadbeef)
    self.rpc[0x01] = self.ProcessClientRequest
    self.rpc[0x02] = self.CreateToon
    self.rpc[0x03] = self.DeleteToon
    self.rpc[0x04] = self.TransferToon
    self.rpc[0x05] = self.SelectToon
    self.rpc[0x06] = self.PresenceChannelCreated
    self.rpc[0x07] = self.GetPlayerVariables
    self.rpc[0x08] = self.GetGameVariables
    self.rpc[0x09] = self.GetLoad

  def ProcessClientRequest(self, packet):
    request = Utils.LoadRequest(game_utilities.ClientRequest(), packet)
    response = game_utilities.ClientResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def CreateToon(self, packet):
    request = Utils.LoadRequest(game_utilities.CreateToonRequest(), packet)
    response = game_utilities.CreateToonResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def DeleteToon(self, packet):
    request = Utils.LoadRequest(game_utilities.DeleteToonRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x03, request, response, packet)

  def TransferToon(self, packet):
    request = Utils.LoadRequest(game_utilities.TransferToonRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x04, request, response, packet)

  def SelectToon(self, packet):
    request = Utils.LoadRequest(game_utilities.SelectToonRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x05, request, response, packet)

  def PresenceChannelCreated(self, packet):
    request = Utils.LoadRequest(game_utilities.PresenceChannelCreatedRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x06, request, response, packet)

  def GetPlayerVariables(self, packet):
    request = Utils.LoadRequest(game_utilities.PlayerVariablesRequest(), packet)
    response = game_utilities.VariablesResponse()
    return self.PerformRpc(0x07, request, response, packet)

  def GetGameVariables(self, packet):
    request = Utils.LoadRequest(game_utilities.GameVariablesRequest(), packet)
    response = game_utilities.VariablesResponse()
    return self.PerformRpc(0x08, request, response, packet)

  def GetLoad(self, packet):
    request = Utils.LoadRequest(server_pool.GetLoadRequest(), packet)
    response = server_pool.ServerState()
    return self.PerformRpc(0x09, request, response, packet)