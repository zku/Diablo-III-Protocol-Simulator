#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class UserManagerService(BaseService):
  def __init__(self):
    super(UserManagerService, self).__init__('UserManagerService', 0xdeadbeef)
    self.rpc[0x01] = self.SubscribeToUserManager
    self.rpc[0x02] = self.ReportPlayer
    self.rpc[0x03] = self.BlockPlayer
    self.rpc[0x04] = self.RemovePlayerBlock
    self.rpc[0x05] = self.AddRecentPlayers
    self.rpc[0x06] = self.RemoveRecentPlayers

  def SubscribeToUserManager(self, packet):
    request = Utils.LoadRequest(user_manager.SubscribeToUserManagerRequest(), packet)
    response = user_manager.SubscribeToUserManagerResponse()
    return self.PerformRpc(0x01, request, response, packet)

  def ReportPlayer(self, packet):
    request = Utils.LoadRequest(user_manager.ReportPlayerRequest(), packet)
    response = user_manager.ReportPlayerResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def BlockPlayer(self, packet):
    request = Utils.LoadRequest(user_manager.BlockPlayerRequest(), packet)
    response = user_manager.BlockPlayerResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def RemovePlayerBlock(self, packet):
    request = Utils.LoadRequest(user_manager.RemovePlayerBlockRequest(), packet)
    response = user_manager.RemovePlayerBlockResponse()
    return self.PerformRpc(0x04, request, response, packet)

  def AddRecentPlayers(self, packet):
    request = Utils.LoadRequest(user_manager.AddRecentPlayersRequest(), packet)
    response = user_manager.AddRecentPlayersResponse()
    return self.PerformRpc(0x05, request, response, packet)

  def RemoveRecentPlayers(self, packet):
    request = Utils.LoadRequest(user_manager.RemoveRecentPlayersRequest(), packet)
    response = user_manager.RemoveRecentPlayersResponse()
    return self.PerformRpc(0x06, request, response, packet)