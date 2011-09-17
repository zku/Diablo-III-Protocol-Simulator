#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class GameMaster(BaseService):
  def __init__(self):
    super(GameMaster, self).__init__('GameMaster', 0xdeadbeef)
    self.rpc[0x01] = self.JoinGame
    self.rpc[0x02] = self.ListFactories
    self.rpc[0x03] = self.FindGame
    self.rpc[0x04] = self.CancelFindGame
    self.rpc[0x05] = self.GameEnded
    self.rpc[0x06] = self.PlayerLeft
    self.rpc[0x07] = self.RegisterServer
    self.rpc[0x08] = self.UnregisterServer
    self.rpc[0x09] = self.RegisterUtilities
    self.rpc[0x0a] = self.UnregisterUtilities
    self.rpc[0x0b] = self.Subscribe
    self.rpc[0x0c] = self.Unsubscribe
    self.rpc[0x0d] = self.ChangeGame
    self.rpc[0x0e] = self.GetFactoryInfo
    self.rpc[0x0f] = self.GetGameStats

  def JoinGame(self, packet):
    request = Utils.LoadRequest(game_master.JoinGameRequest(), packet)
    response = game_master.JoinGameResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def ListFactories(self, packet):
    request = Utils.LoadRequest(game_master.ListFactoriesRequest(), packet)
    response = game_master.ListFactoriesResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def FindGame(self, packet):
    request = Utils.LoadRequest(game_master.FindGameRequest(), packet)
    response = game_master.FindGameResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def CancelFindGame(self, packet):
    request = Utils.LoadRequest(game_master.CancelFindGameRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x04, request, response, packet)

  def GameEnded(self, packet):
    request = Utils.LoadRequest(game_master.GameEndedNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x05, request, response, packet)

  def PlayerLeft(self, packet):
    request = Utils.LoadRequest(game_master.PlayerLeftNotification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x06, request, response, packet)

  def RegisterServer(self, packet):
    request = Utils.LoadRequest(game_master.RegisterServerRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x07, request, response, packet)

  def UnregisterServer(self, packet):
    request = Utils.LoadRequest(game_master.UnregisterServerRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x08, request, response, packet)

  def RegisterUtilities(self, packet):
    request = Utils.LoadRequest(game_master.RegisterUtilitiesRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x09, request, response, packet)

  def UnregisterUtilities(self, packet):
    request = Utils.LoadRequest(game_master.UnregisterUtilitiesRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x0a, request, response, packet)

  def Subscribe(self, packet):
    request = Utils.LoadRequest(game_master.SubscribeRequest(), packet)
    response = game_master.SubscribeResponse()
    return self.PerformRpc(0x0b, request, response, packet)

  def Unsubscribe(self, packet):
    request = Utils.LoadRequest(game_master.UnsubscribeRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x0c, request, response, packet)

  def ChangeGame(self, packet):
    request = Utils.LoadRequest(game_master.ChangeGameRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x0d, request, response, packet)

  def GetFactoryInfo(self, packet):
    request = Utils.LoadRequest(game_master.GetFactoryInfoRequest(), packet)
    response = game_master.GetFactoryInfoResponse()
    return self.PerformRpc(0x0e, request, response, packet)

  def GetGameStats(self, packet):
    request = Utils.LoadRequest(game_master.GetGameStatsRequest(), packet)
    response = game_master.GetGameStatsResponse()
    return self.PerformRpc(0x0f, request, response, packet)