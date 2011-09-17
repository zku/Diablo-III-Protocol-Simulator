#! /usr/bin/env python


import Utils
import proto.lib.rpc.rpc_pb2 as rpc
from services.BaseService import BaseService
from D3ProtoImports import *


class ExchangeService(BaseService):
  def __init__(self):
    super(ExchangeService, self).__init__('ExchangeService', 0xdeadbeef)
    self.rpc[0x02] = self.CreateOrderBook
    self.rpc[0x03] = self.PlaceOfferOnOrderBook
    self.rpc[0x04] = self.PlaceOfferCreateOrderBookIfNeeded
    self.rpc[0x05] = self.PlaceBidOnOrderBook
    self.rpc[0x06] = self.PlaceBidCreateOrderBookIfNeeded
    self.rpc[0x07] = self.QueryOffersByOrderBook
    self.rpc[0x08] = self.QueryBidsByOrderBook
    self.rpc[0x09] = self.QueryOffersByAccountForItem
    self.rpc[0x0a] = self.QueryBidsByAccountForItem
    self.rpc[0x0b] = self.QueryOrderBooksSummary
    self.rpc[0x0c] = self.QuerySettlementsByOrderBook
    self.rpc[0x0d] = self.ReportAuthorize
    self.rpc[0x0e] = self.ReportSettle
    self.rpc[0x0f] = self.ReportCancel
    self.rpc[0x10] = self.SubscribeOrderBookStatusChange
    self.rpc[0x11] = self.UnsubscribeOrderBookStatusChange
    self.rpc[0x12] = self.SubscribeOrderStatusChange
    self.rpc[0x13] = self.UnsubscribeOrderStatusChange
    self.rpc[0x14] = self.GetPaymentMethods
    self.rpc[0x15] = self.ClaimBidItem
    self.rpc[0x16] = self.ClaimBidMoney
    self.rpc[0x17] = self.ClaimOfferItem
    self.rpc[0x18] = self.ClaimOfferMoney
    self.rpc[0x19] = self.CancelBid
    self.rpc[0x1a] = self.CancelOffer
    self.rpc[0x1b] = self.GetConfiguration
    self.rpc[0x1c] = self.GetBidFeeEstimation
    self.rpc[0x1d] = self.GetOfferFeeEstimation

  def CreateOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.CreateOrderBookRequest(), packet)
    response = exchange.CreateOrderBookResponse()
    return self.PerformRpc(0x02, request, response, packet)

  def PlaceOfferOnOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.PlaceOfferOnOrderBookRequest(), packet)
    response = exchange.PlaceOfferOnOrderBookResponse()
    return self.PerformRpc(0x03, request, response, packet)

  def PlaceOfferCreateOrderBookIfNeeded(self, packet):
    request = Utils.LoadRequest(exchange.PlaceOfferCreateOrderBookIfNeededRequest(), packet)
    response = exchange.PlaceOfferCreateOrderBookIfNeededResponse()
    return self.PerformRpc(0x04, request, response, packet)

  def PlaceBidOnOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.PlaceBidOnOrderBookRequest(), packet)
    response = exchange.PlaceBidOnOrderBookResponse()
    return self.PerformRpc(0x05, request, response, packet)

  def PlaceBidCreateOrderBookIfNeeded(self, packet):
    request = Utils.LoadRequest(exchange.PlaceBidCreateOrderBookIfNeededRequest(), packet)
    response = exchange.PlaceBidCreateOrderBookIfNeededResponse()
    return self.PerformRpc(0x06, request, response, packet)

  def QueryOffersByOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.QueryOffersByOrderBookRequest(), packet)
    response = exchange.QueryOffersByOrderBookResponse()
    return self.PerformRpc(0x07, request, response, packet)

  def QueryBidsByOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.QueryBidsByOrderBookRequest(), packet)
    response = exchange.QueryBidsByOrderBookResponse()
    return self.PerformRpc(0x08, request, response, packet)

  def QueryOffersByAccountForItem(self, packet):
    request = Utils.LoadRequest(exchange.QueryOffersByAccountForItemRequest(), packet)
    response = exchange.QueryOffersByAccountForItemResponse()
    return self.PerformRpc(0x09, request, response, packet)

  def QueryBidsByAccountForItem(self, packet):
    request = Utils.LoadRequest(exchange.QueryBidsByAccountForItemRequest(), packet)
    response = exchange.QueryBidsByAccountForItemResponse()
    return self.PerformRpc(0x0a, request, response, packet)

  def QueryOrderBooksSummary(self, packet):
    request = Utils.LoadRequest(exchange.QueryOrderBooksSummaryRequest(), packet)
    response = exchange.QueryOrderBooksSummaryResponse()
    return self.PerformRpc(0x0b, request, response, packet)

  def QuerySettlementsByOrderBook(self, packet):
    request = Utils.LoadRequest(exchange.QuerySettlementsByOrderBookRequest(), packet)
    response = exchange.QuerySettlementsByOrderBookResponse()
    return self.PerformRpc(0x0c, request, response, packet)

  def ReportAuthorize(self, packet):
    request = Utils.LoadRequest(exchange_object_provider.ReportAuthorizeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x0d, request, response, packet)

  def ReportSettle(self, packet):
    request = Utils.LoadRequest(exchange_object_provider.ReportSettleRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x0e, request, response, packet)

  def ReportCancel(self, packet):
    request = Utils.LoadRequest(exchange_object_provider.ReportCancelRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x0f, request, response, packet)

  def SubscribeOrderBookStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.SubscribeOrderBookStatusChangeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x10, request, response, packet)

  def UnsubscribeOrderBookStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.UnsubscribeOrderBookStatusChangeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x11, request, response, packet)

  def SubscribeOrderStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.SubscribeOrderStatusChangeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x12, request, response, packet)

  def UnsubscribeOrderStatusChange(self, packet):
    request = Utils.LoadRequest(exchange.UnsubscribeOrderStatusChangeRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x13, request, response, packet)

  def GetPaymentMethods(self, packet):
    request = Utils.LoadRequest(exchange_object_provider.GetPaymentMethodsRequest(), packet)
    response = exchange_object_provider.GetPaymentMethodsResponse()
    return self.PerformRpc(0x14, request, response, packet)

  def ClaimBidItem(self, packet):
    request = Utils.LoadRequest(exchange.ClaimRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x15, request, response, packet)

  def ClaimBidMoney(self, packet):
    request = Utils.LoadRequest(exchange.ClaimRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x16, request, response, packet)

  def ClaimOfferItem(self, packet):
    request = Utils.LoadRequest(exchange.ClaimRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x17, request, response, packet)

  def ClaimOfferMoney(self, packet):
    request = Utils.LoadRequest(exchange.ClaimRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x18, request, response, packet)

  def CancelBid(self, packet):
    request = Utils.LoadRequest(exchange.CancelRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x19, request, response, packet)

  def CancelOffer(self, packet):
    request = Utils.LoadRequest(exchange.CancelRequest(), packet)
    response = rpc.NoData()
    return self.PerformRpc(0x1a, request, response, packet)

  def GetConfiguration(self, packet):
    request = Utils.LoadRequest(exchange.GetConfigurationRequest(), packet)
    response = exchange.GetConfigurationResponse()
    return self.PerformRpc(0x1b, request, response, packet)

  def GetBidFeeEstimation(self, packet):
    request = Utils.LoadRequest(exchange.GetBidFeeEstimationRequest(), packet)
    response = exchange.GetFeeEstimationResponse()
    return self.PerformRpc(0x1c, request, response, packet)

  def GetOfferFeeEstimation(self, packet):
    request = Utils.LoadRequest(exchange.GetOfferFeeEstimationRequest(), packet)
    response = exchange.GetFeeEstimationResponse()
    return self.PerformRpc(0x1d, request, response, packet)