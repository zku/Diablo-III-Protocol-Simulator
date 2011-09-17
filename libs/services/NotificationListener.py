#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class NotificationListener(BaseService):
  def __init__(self):
    super(NotificationListener, self).__init__('NotificationListener', 0xdeadbeef)
    self.rpc[0x01] = self.OnNotificationReceived

  def OnNotificationReceived(self, packet):
    request = Utils.LoadRequest(notification.Notification(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)