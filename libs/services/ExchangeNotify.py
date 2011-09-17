#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ExchangeNotify(BaseService):
  def __init__(self):
    super(ExchangeNotify, self).__init__('ExchangeNotify', 0xdeadbeef)
    self.rpc[0x01] = self.NotifyOrderBookStatusChange
    self.rpc[0x02] = self.NotifyOfferStatusChange
    self.rpc[0x03] = self.NotifyBidStatusChange

  def NotifyOrderBookStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.OrderBookNotificationRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x01, request, response, packet)

  def NotifyOfferStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.OfferNotificationRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x02, request, response, packet)

  def NotifyBidStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.BidNotificationRequest(), packet)
    response = rpc.NO_RESPONSE()
    return self.PerformRpc(0x03, request, response, packet)