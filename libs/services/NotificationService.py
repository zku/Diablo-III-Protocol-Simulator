#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class NotificationService(BaseService):
  def __init__(self):
    super(NotificationService, self).__init__('NotificationService', 0xdeadbeef)
    self.rpc[0x01] = self.SendNotification
    self.rpc[0x02] = self.RegisterClient
    self.rpc[0x03] = self.UnregisterClient
    self.rpc[0x04] = self.FindClient

  def SendNotification(self, packet):
    request = Utils.LoadRequest(notification.Notification(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x01, request, response, packet)

  def RegisterClient(self, packet):
    request = Utils.LoadRequest(notification.RegisterClientRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x02, request, response, packet)

  def UnregisterClient(self, packet):
    request = Utils.LoadRequest(notification.UnregisterClientRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x03, request, response, packet)

  def FindClient(self, packet):
    request = Utils.LoadRequest(notification.FindClientRequest(), packet)
    response = notification.FindClientResponse()
    return self.PerformRpc(0x04, request, response, packet)