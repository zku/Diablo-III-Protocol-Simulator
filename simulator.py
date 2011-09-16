#! /usr/bin/env python

'''
author:             sku/thesku
description:        parses diablo3 tcp streams and
                    maps the packets to their respective
                    protobuf messages, simulates client
                    and server behaviour and keeps track
                    of bound services / responses etc.
credits:            shadow^dancer, TOM_RUS, #d3.dev
legal:              code posted to public domain by sku, no copyright
                    use at your own risk
'''

import sys
import util
import time

from d3packet import D3Packet
from bytestream import ByteStream

sys.path.append('proto/bin/py')
from lib.rpc.rpc_pb2 import *
from lib.rpc.connection_pb2 import *
from service.authentication.authentication_pb2 import *
from service.channel_invitation.definition.channel_invitation_pb2 import *
from service.followers.definition.followers_pb2 import *
from service.user_manager.user_manager_pb2 import *
from service.friends.definition.friends_pb2 import *
from service.exchange.exchange_pb2 import *
from service.game_master.game_master_pb2 import *
from service.game_master.game_master_types_pb2 import *
from service.toon.toon_pb2 import *
from service.toon.toon_external_pb2 import *
from service.channel.definition.channel_pb2 import *
from service.channel.channel_types_pb2 import *
from service.storage.storage_pb2 import *
from service.server_pool.server_pool_pb2 import *
from service.notification.notification_pb2 import *
from service.presence.presence_pb2 import *
from service.presence.presence_types_pb2 import *


class Simulator:
  def __init__(self):
    self.c = Entity('client')
    self.s = Entity('server')
    self.c.other = self.s
    self.s.other = self.c
    self.all = util.FileBytes('data/all.dat')
    self.c2s = util.FileBytes('data/c2s.dat')
    self.s2c = util.FileBytes('data/s2c.dat')
    
  def Run(self):
    print 'D3 client<->server protocol simulator by sku'
    print 'replaying real login protocol'
    allPackets = 0
    while len(self.all) > 0:
      allPacket = D3Packet(self.all, False)
      c2sPacket = None if len(self.c2s) == 0 else D3Packet(self.c2s, False)
      s2cPacket = None if len(self.s2c) == 0 else D3Packet(self.s2c, False)
      self.all = allPacket.Remainder()
      allPackets += 1
      if c2sPacket and c2sPacket.HeaderString() == allPacket.HeaderString():
        recipient = self.s
        self.c2s = c2sPacket.Remainder()
      elif s2cPacket and s2cPacket.HeaderString() == allPacket.HeaderString():
        recipient = self.c
        self.s2c = s2cPacket.Remainder()
      else:
        raise RuntimeError('who the fuck sent this packet?')
      recipient.Send(allPacket, allPackets)
    assert(len(self.all) == 0 and len(self.c2s) == 0 and len(self.s2c) == 0)
    
class Entity:
  def __init__(self, id):
    self.other = None
    self.id = id
    self.packets = 0
    self.hashToService = {}
    self.responses = {}
    self.exports = {}
    self.imports = {}
    self.pending = {}
    self.InitializeDefaultServices()
    self.InitializeHandlers()
    
  def InitializeDefaultServices(self):
    self.exports[0x00] = 0x00000000
    self.exports[0xfe] = 0xfffffffe
    self.imports[0x00] = 0x00000000
    self.imports[0xfe] = 0xfffffffe
    
  def InitializeHandlers(self):
    self.hashToService[0x00000000] = self.Hash_0x00000000_Handler # ConnectionService
    self.hashToService[0xfffffffe] = self.Hash_0xfffffffe_Handler # ResponseService
    self.hashToService[0x0decfc01] = self.Hash_0x0decfc01_Handler # AuthenticationServer
    self.hashToService[0x83040608] = self.Hash_0x83040608_Handler # ChannelInvitationService
    self.hashToService[0x4124c31b] = self.Hash_0x4124c31b_Handler # ToonServiceExternal
    self.hashToService[0xe5a11099] = self.Hash_0xe5a11099_Handler # FollowersService
    self.hashToService[0x3e19268a] = self.Hash_0x3e19268a_Handler # UserManagerService
    self.hashToService[0xa3ddb1bd] = self.Hash_0xa3ddb1bd_Handler # FriendsService
    self.hashToService[0xd750148b] = self.Hash_0xd750148b_Handler # ExchangeService
    self.hashToService[0xfa0796ff] = self.Hash_0xfa0796ff_Handler # PresenceService
    self.hashToService[0x810cb195] = self.Hash_0x810cb195_Handler # GameMaster
    self.hashToService[0xbf8c8094] = self.Hash_0xbf8c8094_Handler # ChannelSubscriber
    self.hashToService[0xb732db32] = self.Hash_0xb732db32_Handler # Channel
    self.hashToService[0x71240e35] = self.Hash_0x71240e35_Handler # AuthenticationClient
    self.hashToService[0x0cbe3c43] = self.Hash_0x0cbe3c43_Handler # NotificationService
    self.hashToService[0xe1cb2ea8] = self.Hash_0xe1cb2ea8_Handler # NotificationListener
    self.hashToService[0xf084fc20] = self.Hash_0xf084fc20_Handler # ChannelInvitationNotify
    self.hashToService[0x905cdf9f] = self.Hash_0x905cdf9f_Handler # FollowersNotify
    self.hashToService[0xbc872c22] = self.Hash_0xbc872c22_Handler # UserManagerNotify
    self.hashToService[0x6f259a13] = self.Hash_0x6f259a13_Handler # FriendsNotify
    self.hashToService[0xf4e7fa35] = self.Hash_0xf4e7fa35_Handler # PartyService
    self.hashToService[0x00d89ca9] = self.Hash_0x00d89ca9_Handler # ChatService
    self.hashToService[0x3fc1274d] = self.Hash_0x3fc1274d_Handler # GameUtilities
    self.hashToService[0x060ca08d] = self.Hash_0x060ca08d_Handler # ChannelOwner
    self.hashToService[0xc6f9ccc5] = self.Hash_0xc6f9ccc5_Handler # GameFactorySubscriber
    self.hashToService[0xda6e4bb9] = self.Hash_0xda6e4bb9_Handler # StorageService
    self.hashToService[0x166fe4a1] = self.Hash_0x166fe4a1_Handler # ExchangeNotify
    self.hashToService[0x0a24a291] = self.Hash_0x0a24a291_Handler # SearchService
    
  def Send(self, packet, allPackets):
    self.packets += 1
    print '\n\n*** %s received packet ***' % self.id
    print '> this is total packet 0x%04x' % allPackets
    print '> this is %s\'s 0x%04x-th received packet' % (self.id, self.packets)
    print '> packet header: %s' % packet.HeaderString()
    print '> packet payload/protobuffer:\n' + packet.PayloadString()
    if packet.service in self.exports:
      hash = self.exports[packet.service]
    else:
      raise RuntimeError('services messed up')
    handler = self.hashToService[hash]
    print '> packet received on service id 0x%02x with hash 0x%08x' % (packet.service, hash)
    handler(packet)
    
  def BuildResponsePacket(self, header, response, packet):
    payload = util.StringToBytes(response.SerializeToString())
    request = util.ValueToBytes(packet.request, 2)
    length = util.ValueToVarInt(len(payload))
    return header + request + length + payload

    
  # *** ConnectionService ***
  def Hash_0x00000000_Handler(self, packet):
    print 'handler 0x00000000 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleConnectRequest(packet)
    elif packet.method == 0x02: self.HandleBindRequest(packet)
    elif packet.method == 0x03: self.HandleEchoRequest(packet)
    elif packet.method == 0x04: self.HandleDisconnectNotification(packet)
    elif packet.method == 0x05: self.HandleNullRequest(packet)
    elif packet.method == 0x06: self.HandleEncryptRequest(packet)
    elif packet.method == 0x07: self.HandleDisconnectRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleConnectRequest(self, packet):
    print '>>> ConnectRequest'
    request = ConnectRequest()
    print request
    self.other.responses[packet.request] = ('ConnectResponse', ConnectResponse(), packet)
    
  def HandleBindRequest(self, packet):
    print '>>> BindRequest'
    request = BindRequest()
    request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('BindResponse', BindResponse(), packet)
    self.pending[packet.request] = []
    for hash in request.imported_service_hash:
      self.pending[packet.request] += [hash]
    for export in request.exported_service:
      self.imports[export.id] = export.hash
      self.other.exports[export.id] = export.hash
      
  def HandleEchoRequest(self, packet):
    print '>>> EchoRequest'
    request = EchoRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('EchoResponse', EchoResponse(), packet)
  
  def HandleDisconnectNotification(self, packet):
    print '>>> DisconnectNotification'
    request = DisconnectNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
  
  def HandleNullRequest(self, packet):
    print '>>> NullRequest'
    request = NullRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleEncryptRequest(self, packet):
    print '>>> EncryptRequest'
    request = EncryptRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)

  def HandleDisconnectRequest(self, packet):
    print '>>> DisconnectRequest'
    request = DisconnectRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
    
  # *** AuthenticationServer ***
  def Hash_0x0decfc01_Handler(self, packet): 
    print 'handler 0x0decfc01 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleLogonRequest(packet)
    elif packet.method == 0x02: self.HandleModuleMessageRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleLogonRequest(self, packet):
    print '>>> LogonRequest'
    request = LogonRequest()
    request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('LogonResponse', LogonResponse(), packet)
  
  def HandleModuleMessageRequest(self, packet):
    print '>>> ModuleMessageRequest'
    request = ModuleMessageRequest()
    request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
    
   # *** ChannelInvitationService ***
  def Hash_0x83040608_Handler(self, packet):
    print 'handler 0x83040608 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleSubscribeRequest_Invitation(packet)
    elif packet.method == 0x02: self.HandleUnsubscribeRequest_Invitation(packet)
    elif packet.method == 0x03: self.HandleSendInvitationRequest_Invitation(packet)
    elif packet.method == 0x04: self.HandleAcceptInvitationRequest_Invitation(packet)
    elif packet.method == 0x05: self.HandleGenericRequest_Invitation(packet)
    elif packet.method == 0x06: self.HandleRevokeInvitationRequest_Invitation(packet)
    elif packet.method == 0x07: self.HandleSuggestInvitationRequest_Invitation(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleSubscribeRequest_Invitation(self, packet):
    print '>>> SubscribeRequest_Invitation'
    request = service.channel_invitation.definition.channel_invitation_pb2.SubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SubscribeResponse_Invitation', service.channel_invitation.definition.channel_invitation_pb2.SubscribeResponse(), packet)

  def HandleUnsubscribeRequest_Invitation(self, packet):
    print '>>> UnsubscribeRequest'
    request = UnsubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleSendInvitationRequest_Invitation(self, packet):
    print '>>> SendInvitationRequest'
    request = SendInvitationRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SendInvitationResponse', SendInvitationResponse(), packet)
    
  def HandleAcceptInvitationRequest_Invitation(self, packet):
    print '>>> AcceptInvitationRequest'
    request = AcceptInvitationRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('AcceptInvitationResponse', AcceptInvitationResponse(), packet)
    
  def HandleGenericRequest_Invitation(self, packet):
    print '>>> GenericRequest'
    request = GenericRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleRevokeInvitationRequest_Invitation(self, packet):
    print '>>> RevokeInvitationRequest'
    request = RevokeInvitationRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleSuggestInvitationRequest_Invitation(self, packet):
    print '>>> SuggestInvitationRequest'
    request = SuggestInvitationRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
    
  # *** ToonServiceExternal ***
  def Hash_0x4124c31b_Handler(self, packet): 
    print 'handler 0x4124c31b called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleToonListRequest(packet)
    elif packet.method == 0x02: self.HandleSelectToonRequest(packet)
    elif packet.method == 0x03: self.HandleCreateToonRequest(packet)
    elif packet.method == 0x04: self.HandleDeleteToonRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleToonListRequest(self, packet):
    print '>>> ToonListRequest'
    request = ToonListRequest()
    print request
    self.other.responses[packet.request] = ('ToonListResponse', ToonListResponse(), packet)
    
  def HandleSelectToonRequest(self, packet):
    print '>>> SelectToonRequest'
    request = SelectToonRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SelectToonResponse', SelectToonResponse(), packet)
    
  def HandleCreateToonRequest(self, packet):
    print '>>> CreateToonRequest'
    request = CreateToonRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('CreateToonResponse', CreateToonResponse(), packet)
    
  def HandleDeleteToonRequest(self, packet):
    print '>>> DeleteToonRequest'
    request = DeleteToonRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('DeleteToonResponse', DeleteToonResponse(), packet)
    
    
  # *** FollowersService ***
  def Hash_0xe5a11099_Handler(self, packet): 
    print 'handler 0xe5a11099 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleSubscribeToFollowersRequest(packet)
    elif packet.method == 0x02: self.HandleStartFollowingRequest(packet)
    elif packet.method == 0x03: self.HandleStopFollowingRequest(packet)
    elif packet.method == 0x04: self.HandleUpdateFollowerStateRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleSubscribeToFollowersRequest(self, packet):
    print '>>> SubscribeToFollowersRequest'
    request = SubscribeToFollowersRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SubscribeToFollowersResponse', SubscribeToFollowersResponse(), packet)
    
  def HandleStartFollowingRequest(self, packet):
    print '>>> StartFollowingRequest'
    request = StartFollowingRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('StartFollowingResponse', StartFollowingResponse(), packet)
    
  def HandleStopFollowingRequest(self, packet):
    print '>>> StopFollowingRequest'
    request = StopFollowingRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('StopFollowingResponse', StopFollowingResponse(), packet)
    
  def HandleUpdateFollowerStateRequest(self, packet):
    print '>>> UpdateFollowerStateRequest'
    request = UpdateFollowerStateRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('UpdateFollowerStateResponse', UpdateFollowerStateResponse(), packet)
    
  # *** UserManagerService ***
  def Hash_0x3e19268a_Handler(self, packet): 
    print 'handler 0x3e19268a called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleSubscribeToUserManagerRequest(packet)
    elif packet.method == 0x02: self.HandleReportPlayerRequest(packet)
    elif packet.method == 0x03: self.HandleBlockPlayerRequest(packet)
    elif packet.method == 0x04: self.HandleRemovePlayerBlockRequest(packet)
    elif packet.method == 0x05: self.HandleAddRecentPlayersRequest(packet)
    elif packet.method == 0x06: self.HandleRemoveRecentPlayersRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleSubscribeToUserManagerRequest(self, packet):
    print '>>> SubscribeToUserManagerRequest'
    request = SubscribeToUserManagerRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SubscribeToUserManagerResponse', SubscribeToUserManagerResponse(), packet)
    
  def HandleReportPlayerRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleBlockPlayerRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleRemovePlayerBlockRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleAddRecentPlayersRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleRemoveRecentPlayersRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** FriendsService ***
  def Hash_0xa3ddb1bd_Handler(self, packet):
    print 'handler 0xa3ddb1bd called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleSubscribeToFriendsRequest(packet)
    elif packet.method == 0x02: self.HandleSendInvitationRequest_Invitation(packet)
    elif packet.method in range(0x03, 0x07): self.HandleGenericRequest_Invitation(packet)
    elif packet.method == 0x07: self.HandleGenericFriendRequest(packet)
    elif packet.method == 0x08: self.HandleViewFriendsRequest(packet)
    elif packet.method == 0x09: self.HandleUpdateFriendStateRequest(packet)
    elif packet.method == 0x0a: self.HandleUnsubscribeToFriendsRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleSubscribeToFriendsRequest(self, packet):
    print '>>> SubscribeToFriendsRequest'
    request = SubscribeToFriendsRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SubscribeToFriendsResponse', SubscribeToFriendsResponse(), packet)
    
  def HandleGenericFriendRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleViewFriendsRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleUpdateFriendStateRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleUnsubscribeToFriendsRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  # *** ExchangeService ***
  def Hash_0xd750148b_Handler(self, packet): 
    print 'handler 0xd750148b called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleCreateOrderBookRequest(packet)
    elif packet.method == 0x02: self.HandlePlaceOfferOnOrderBookRequest(packet)
    elif packet.method == 0x03: self.HandlePlaceOfferCreateOrderBookIfNeededRequest(packet)
    elif packet.method == 0x04: self.HandlePlaceBidOnOrderBookRequest(packet)
    elif packet.method == 0x05: self.HandlePlaceBidCreateOrderBookIfNeededRequest(packet)
    elif packet.method == 0x06: self.HandleQueryOffersByOrderBookRequest(packet)
    elif packet.method == 0x07: self.HandleQueryBidsByOrderBookRequest(packet)
    elif packet.method == 0x08: self.HandleQueryOffersByAccountForItemRequest(packet)
    elif packet.method == 0x09: self.HandleQueryBidsByAccountForItemRequest(packet)
    elif packet.method == 0x0a: self.HandleQueryOrderBooksSummaryRequest(packet)
    elif packet.method == 0x0b: self.HandleQuerySettlementsByOrderBookRequest(packet)
    elif packet.method == 0x0c: self.HandleReportAuthorizeRequest(packet)
    elif packet.method == 0x0d: self.HandleReportSettleRequest(packet)
    elif packet.method == 0x0e: self.HandleReportCancelRequest(packet)
    elif packet.method == 0x0f: self.HandleSubscribeOrderBookStatusChangeRequest(packet)
    elif packet.method == 0x10: self.HandleUnsubscribeOrderBookStatusChangeRequest(packet)
    elif packet.method == 0x11: self.HandleSubscribeOrderStatusChangeRequest(packet)
    elif packet.method == 0x12: self.HandleUnsubscribeOrderStatusChangeRequest(packet)
    elif packet.method == 0x13: self.HandleGetPaymentMethodsRequest(packet)
    elif packet.method == 0x14: self.HandleClaimRequest(packet)
    elif packet.method == 0x15: self.HandleClaimRequest(packet)
    elif packet.method == 0x16: self.HandleClaimRequest(packet)
    elif packet.method == 0x17: self.HandleClaimRequest(packet)
    elif packet.method == 0x18: self.HandleCancelRequest(packet)
    elif packet.method == 0x19: self.HandleCancelRequest(packet)
    elif packet.method == 0x1a: self.HandleGetConfigurationRequest(packet)
    elif packet.method == 0x1b: self.HandleGetBidFeeEstimationRequest(packet)
    elif packet.method == 0x1c: self.HandleGetOfferFeeEstimationRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleCreateOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePlaceOfferOnOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePlaceOfferCreateOrderBookIfNeededRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePlaceBidOnOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePlaceBidCreateOrderBookIfNeededRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQueryOffersByOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQueryBidsByOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQueryOffersByAccountForItemRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQueryBidsByAccountForItemRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQueryOrderBooksSummaryRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleQuerySettlementsByOrderBookRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleReportAuthorizeRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleReportSettleRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleReportCancelRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleSubscribeOrderBookStatusChangeRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleUnsubscribeOrderBookStatusChangeRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleSubscribeOrderStatusChangeRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleGetPaymentMethodsRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleClaimRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleCancelRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleGetBidFeeEstimationRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleGetOfferFeeEstimationRequest(self, packet):
    raise RuntimeError('implement me plz')

  def HandleUnsubscribeOrderStatusChangeRequest(self, packet):
    print '>>> UnsubscribeOrderStatusChangeRequest'
    request = UnsubscribeOrderStatusChangeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleGetConfigurationRequest(self, packet):
    print '>>> GetConfigurationRequest'
    request = GetConfigurationRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('GetConfigurationResponse', GetConfigurationResponse(), packet)

    
  # *** PresenceService ***
  def Hash_0xfa0796ff_Handler(self, packet): 
    print 'handler 0xfa0796ff called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleSubscribeRequest_Presence(packet)
    elif packet.method == 0x02: self.HandleUnsubscribeRequest_Presence(packet)
    elif packet.method == 0x03: self.HandleUpdateRequest_Presence(packet)
    elif packet.method == 0x04: self.HandleQueryRequest_Presence(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleSubscribeRequest_Presence(self, packet):
    print '>>> SubscribeRequest_Presence'
    request = service.presence.presence_pb2.SubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUnsubscribeRequest_Presence(self, packet):
    print '>>> UnsubscribeRequest_Presence'
    request = service.presence.presence_pb2.UnsubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUpdateRequest_Presence(self, packet):
    print '>>> UpdateRequest_Presence'
    request = service.presence.presence_pb2.UpdateRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleQueryRequest_Presence(self, packet):
    print '>>> QueryRequest_Presence'
    request = service.presence.presence_pb2.QueryRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('QueryResponse', service.presence.presence_pb2.QueryResponse(), packet)

    
  # *** GameMaster ***
  def Hash_0x810cb195_Handler(self, packet):
    print 'handler 0x810cb195 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleJoinGameRequest(packet)
    elif packet.method == 0x02: self.HandleListFactoriesRequest(packet)
    elif packet.method == 0x03: self.HandleFindGameRequest(packet)
    elif packet.method == 0x04: self.HandleCancelFindGameRequest(packet)
    elif packet.method == 0x05: self.HandleGameEndedNotification(packet)
    elif packet.method == 0x06: self.HandlePlayerLeftNotification(packet)
    elif packet.method == 0x07: self.HandleRegisterServerRequest(packet)
    elif packet.method == 0x08: self.HandleUnregisterServerRequest(packet)
    elif packet.method == 0x09: self.HandleRegisterUtilitiesRequest(packet)
    elif packet.method == 0x0a: self.HandleUnregisterUtilitiesRequest(packet)
    elif packet.method == 0x0b: self.HandleSubscribeRequest_GameMaster(packet)
    elif packet.method == 0x0c: self.HandleUnsubscribeRequest_GameMaster(packet)
    elif packet.method == 0x0d: self.HandleChangeGameRequest(packet)
    elif packet.method == 0x0e: self.HandleGetFactoryInfoRequest(packet)
    elif packet.method == 0x0f: self.HandleGetGameStatsRequest(packet)
    else: raise RuntimeError('unknown method') 

  def HandleJoinGameRequest(self, packet):
    print '>>> JoinGameRequest'
    request = JoinGameRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('JoinGameResponse', JoinGameResponse(), packet)
    
  def HandleListFactoriesRequest(self, packet):
    print '>>> ListFactoriesRequest'
    request = ListFactoriesRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('ListFactoriesResponse', ListFactoriesResponse(), packet)

  def HandleFindGameRequest(self, packet):
    print '>>> FindGameRequest'
    request = FindGameRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('FindGameResponse', FindGameResponse(), packet)
    
  def HandleCancelFindGameRequest(self, packet):
    print '>>> CancelFindGameRequest'
    request = CancelFindGameRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleGameEndedNotification(self, packet):
    print '>>> GameEndedNotification'
    request = GameEndedNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandlePlayerLeftNotification(self, packet):
    print '>>> PlayerLeftNotification'
    request = PlayerLeftNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleRegisterServerRequest(self, packet):
    print '>>> RegisterServerRequest'
    request = RegisterServerRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUnregisterServerRequest(self, packet):
    print '>>> UnregisterServerRequest'
    request = UnregisterServerRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleRegisterUtilitiesRequest(self, packet):
    print '>>> RegisterUtilitiesRequest'
    request = RegisterUtilitiesRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUnregisterUtilitiesRequest(self, packet):
    print '>>> UnregisterUtilitiesRequest'
    request = UnregisterUtilitiesRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleSubscribeRequest(self, packet):
    print '>>> SubscribeRequest'
    request = SubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('SubscribeResponse', SubscribeResponse(), packet)
    
  def HandleUnsubscribeRequest(self, packet):
    print '>>> UnsubscribeRequest'
    request = UnsubscribeRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleChangeGameRequest(self, packet):
    print '>>> ChangeGameRequest'
    request = ChangeGameRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleGetFactoryInfoRequest(self, packet):
    print '>>> GetFactoryInfoRequest'
    request = GetFactoryInfoRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('GetFactoryInfoResponse', GetFactoryInfoResponse(), packet)
    
  def HandleGetGameStatsRequest(self, packet):
    print '>>> GetGameStatsRequest'
    request = GetGameStatsRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('GetGameStatsResponse', GetGameStatsResponse(), packet)
    
  # *** ChannelSubscriber ***
  def Hash_0xbf8c8094_Handler(self, packet): 
    print 'handler 0xbf8c8094 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleAddNotification(packet)
    elif packet.method == 0x02: self.HandleJoinNotification(packet)
    elif packet.method == 0x03: self.HandleRemoveNotification(packet)
    elif packet.method == 0x04: self.HandleLeaveNotification(packet)
    elif packet.method == 0x05: self.HandleSendMessageNotification(packet)
    elif packet.method == 0x06: self.HandleUpdateChannelStateNotification(packet)
    elif packet.method == 0x07: self.HandleUpdateMemberStateNotification(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleAddNotification(self, packet):
    print '>>> AddNotification'
    request = AddNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)

  def HandleJoinNotification(self, packet):
    print '>>> JoinNotification'
    request = JoinNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleRemoveNotification(self, packet):
    print '>>> RemoveNotification'
    request = RemoveNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
     
  def HandleLeaveNotification(self, packet):
    print '>>> LeaveNotification'
    request = LeaveNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleSendMessageNotification(self, packet):
    print '>>> SendMessageNotification'
    request = SendMessageNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleUpdateChannelStateNotification(self, packet):
    print '>>> UpdateChannelStateNotification'
    request = UpdateChannelStateNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
  def HandleUpdateMemberStateNotification(self, packet):
    print '>>> UpdateMemberStateNotification'
    request = UpdateMemberStateNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)

  # *** Channel ***
  def Hash_0xb732db32_Handler(self, packet):
    print 'handler 0xb732db32 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleAddMemberRequest(packet)
    elif packet.method == 0x02: self.HandleRemoveMemberRequest(packet)
    elif packet.method == 0x03: self.HandleSendMessageRequest(packet)
    elif packet.method == 0x04: self.HandleUpdateChannelStateRequest(packet)
    elif packet.method == 0x05: self.HandleUpdateMemberStateRequest(packet)
    elif packet.method == 0x06: self.HandleDissolveRequest(packet)
    elif packet.method == 0x07: self.HandleSetRolesRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleAddMemberRequest(self, packet):
    print '>>> AddMemberRequest'
    request = AddMemberRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleRemoveMemberRequest(self, packet):
    print '>>> RemoveMemberRequest'
    request = RemoveMemberRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleSendMessageRequest(self, packet):
    print '>>> SendMessageRequest'
    request = SendMessageRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUpdateChannelStateRequest(self, packet):
    print '>>> UpdateChannelStateRequest'
    request = UpdateChannelStateRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleUpdateMemberStateRequest(self, packet):
    print '>>> UpdateMemberStateRequest'
    request = UpdateMemberStateRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleDissolveRequest(self, packet):
    print '>>> DissolveRequest'
    request = DissolveRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
  def HandleSetRolesRequest(self, packet):
    print '>>> SetRolesRequest'
    request = SetRolesRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NoData', NoData(), packet)
    
    
  # *** AuthenticationClient ***
  def Hash_0x71240e35_Handler(self, packet): 
    print 'handler 0x71240e35 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleModuleLoadRequest(packet)
    elif packet.method == 0x02: self.HandleModuleMessageRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleModuleLoadRequest(self, packet):
    print '>>> ModuleLoadRequest'
    request = ModuleLoadRequest()
    request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('ModuleLoadResponse', ModuleLoadResponse(), packet)

    
  # *** NotificationService ***
  def Hash_0x0cbe3c43_Handler(self, packet):
    print 'handler 0x0cbe3c43 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleNotification(packet)
    elif packet.method == 0x02: self.HandleRegisterClientRequest(packet)
    elif packet.method == 0x03: self.HandleUnregisterClientRequest(packet)
    elif packet.method == 0x04: self.HandleFindClientRequest(packet)
    else:raise RuntimeError('unknown method')
    
  def HandleNotification(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleRegisterClientRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleUnregisterClientRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleFindClientRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** NotificationListener ***
  def Hash_0xe1cb2ea8_Handler(self, packet): 
    print 'handler 0xe1cb2ea8 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleNotification(packet)
    else: raise RuntimeError('unknown method')
    
    
  # *** ChannelInvitationNotify ***
  def Hash_0xf084fc20_Handler(self, packet): 
    print 'handler 0xf084fc20 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleInvitationAddedNotification(packet)
    elif packet.method == 0x02: self.HandleInvitationRemovedNotification(packet)
    elif packet.method == 0x03: self.HandleSuggestionAddedNotification(packet)
    elif packet.method == 0x04: self.HandleHasRoomForInvitationRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleInvitationAddedNotification(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleInvitationRemovedNotification(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleSuggestionAddedNotification(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleHasRoomForInvitationRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** FollowersNotify ***
  def Hash_0x905cdf9f_Handler(self, packet):
    print 'handler 0x905cdf9f called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleFollowerNotification(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleFollowerNotification(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** UserManagerNotify ***
  def Hash_0xbc872c22_Handler(self, packet):
    print 'handler 0xbc872c22 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method in range(0x01, 0x03): self.HandleBlockedPlayerNotification(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleBlockedPlayerNotification(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** FriendsNotify ***
  def Hash_0x6f259a13_Handler(self, packet):
    print 'handler 0x6f259a13 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method in range(0x01, 0x03): self.HandleFriendNotification(packet)
    elif packet.method == 0x03: self.HandleInvitationAddedNotification(packet)
    elif packet.method in range(0x04, 0x06): self.HandleInvitationRemovedNotification(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleFriendNotification(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** PartyService ***
  def Hash_0xf4e7fa35_Handler(self, packet):
    print 'handler 0xf4e7fa35 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleCreateChannelRequest(packet)
    elif packet.method == 0x02: self.HandleJoinChannelRequest(packet)
    elif packet.method == 0x03: self.HandleGetChannelInfoRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleCreateChannelRequest(self, packet):  
    print '>>> CreateChannelRequest'
    request = CreateChannelRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('CreateChannelResponse', CreateChannelResponse(), packet)
  
  def HandleJoinChannelRequest(self, packet):
    print '>>> JoinChannelRequest'
    request = JoinChannelRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('JoinChannelResponse', JoinChannelResponse(), packet)

  def HandleGetChannelInfoRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** ChatService ***
  def Hash_0x00d89ca9_Handler(self, packet): 
    print 'handler 0x00d89ca9 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleFindChannelRequest(packet)
    elif packet.method == 0x02: self.HandleCreateChannelRequest(packet)
    elif packet.method == 0x03: self.HandleJoinChannelRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleFindChannelRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** GameUtilities ***
  def Hash_0x3fc1274d_Handler(self, packet):
    print 'handler 0x3fc1274d called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleClientRequest(packet)
    elif packet.method == 0x02: self.HandleCreateToonRequest(packet)
    elif packet.method == 0x03: self.HandleDeleteToonRequest(packet)
    elif packet.method == 0x04: self.HandleTransferToonRequest(packet)
    elif packet.method == 0x05: self.HandleSelectToonRequest(packet)
    elif packet.method == 0x06: self.HandlePresenceChannelCreatedRequest(packet)
    elif packet.method == 0x07: self.HandlePlayerVariablesRequest(packet)
    elif packet.method == 0x08: self.HandleGameVariablesRequest(packet)
    elif packet.method == 0x09: self.HandleGetLoadRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleClientRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleTransferToonRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePresenceChannelCreatedRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandlePlayerVariablesRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleGameVariablesRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleGetLoadRequest(self, packet):
    raise RuntimeError('implement me plz')
    

  # *** ChannelOwner ***
  def Hash_0x060ca08d_Handler(self, packet):
    print 'handler 0x060ca08d called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleGetChannelIdRequest(packet)
    elif packet.method == 0x02: self.HandleCreateChannelRequest(packet)
    elif packet.method == 0x03: self.HandleJoinChannelRequest(packet)
    elif packet.method == 0x04: self.HandleFindChannelRequest(packet)
    elif packet.method == 0x05: self.HandleGetChannelInfoRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleGetChannelIdRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** GameFactorySubscriber ***
  def Hash_0xc6f9ccc5_Handler(self, packet):
    print 'handler 0xc6f9ccc5 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleGameFoundNotification(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleGameFoundNotification(self, packet):
    print '>>> GameFoundNotification'
    request = GameFoundNotification()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('NO_RESPONSE', NO_RESPONSE(), packet)
    
    
  # *** StorageService ***
  def Hash_0xda6e4bb9_Handler(self, packet):
    print 'handler 0xda6e4bb9 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleExecuteRequest(packet)
    elif packet.method == 0x02: self.HandleOpenTableRequest(packet)
    elif packet.method == 0x03: self.HandleOpenColumnRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleExecuteRequest(self, packet):
    print '>>> ExecuteRequest'
    request = ExecuteRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('ExecuteResponse', ExecuteResponse(), packet)
    
  def HandleOpenTableRequest(self, packet):
    print '>>> OpenTableRequest'
    request = OpenTableRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('OpenTableResponse', OpenTableResponse(), packet)
    
  def HandleOpenColumnRequest(self, packet):
    print '>>> OpenColumnRequest'
    request = OpenColumnRequest()
    if packet.HasPayload():
      request.ParseFromString(packet.PayloadAsString())
    print request
    self.other.responses[packet.request] = ('OpenColumnResponse', OpenColumnResponse(), packet)
    
    
  # *** ExchangeNotify ***
  def Hash_0x166fe4a1_Handler(self, packet):
    print 'handler 0x166fe4a1 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleOrderBookNotificationRequest(packet)
    elif packet.method == 0x02: self.HandleOfferNotificationRequest(packet)
    elif packet.method == 0x03: self.HandleBidNotificationRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleOrderBookNotificationRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleOfferNotificationRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleBidNotificationRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** SearchService ***
  def Hash_0x0a24a291_Handler(self, packet):
    print 'handler 0x0a24a291 called, method: 0x%x (service id: 0x%02x)' % (packet.method, packet.service)
    if packet.method == 0x01: self.HandleFindMatchesRequest(packet)
    elif packet.method == 0x02: self.HandleSetObjectRequest(packet)
    elif packet.method == 0x03: self.HandleRemoveObjectsRequest(packet)
    else: raise RuntimeError('unknown method')
    
  def HandleFindMatchesRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleSetObjectRequest(self, packet):
    raise RuntimeError('implement me plz')
    
  def HandleRemoveObjectsRequest(self, packet):
    raise RuntimeError('implement me plz')
    
    
  # *** ResponseService ***
  def Hash_0xfffffffe_Handler(self, packet):
    print 'handler 0xfffffffe called, method: 0x%x, request:0x%04x (service id: 0x%02x)' % (packet.method, packet.request, packet.service)
    requestId = packet.request
    if not requestId in self.responses:
      print packet.Guess()
      raise RuntimeError('salkfjlksdslkfjsd')
    t = self.responses[requestId]
    print '>>> ' + t[0]
    response = t[1]
    if packet.HasPayload():
      response.ParseFromString(packet.PayloadAsString())
    print response
    if t[0] == 'BindResponse':
      requestPacket = t[2]
      assert(requestPacket.request == packet.request)
      ids = response.imported_service_id
      hashes = self.other.pending[packet.request]
      assert(len(ids) == len(hashes))
      i = 0
      while i < len(ids):
        self.imports[ids[i]] = hashes[i]
        self.other.exports[ids[i]] = hashes[i]
        i += 1
      self.other.pending[packet.request] = []
      assert(self.imports == self.other.exports)
      assert(self.exports == self.other.imports)
    
    
  # *** Misc ***
  def HandleGuess(self, packet):
    print '>>> GUESSING'
    guess = packet.Guess()
    print guess
    

# Wrooooooooooooooooom
s = Simulator()
s.Run()