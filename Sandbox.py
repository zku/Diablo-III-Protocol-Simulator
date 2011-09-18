#! /usr/bin/env python

# NOTHIGN YET, GO AWAY.


import Utils
from D3Packet import D3Packet

import socket, select, time

# easier access to the protobuf files and the services
import sys
sys.path.append('./libs/')
sys.path.append('./libs/services/')
sys.path.append('./libs/proto/')
sys.path.append('./libs/proto/lib/')
sys.path.append('./libs/proto/service/')
sys.path.append('./libs/proto/google/')

from D3ProtoImports import *

# rpc services
from services.AuthenticationClient import AuthenticationClient
from services.AuthenticationServer import AuthenticationServer
from services.ResponseService import ResponseService
from services.Channel import Channel
from services.ChannelInvitationNotify import ChannelInvitationNotify
from services.ChannelInvitationService import ChannelInvitationService
from services.ChannelOwner import ChannelOwner
from services.ChannelSubscriber import ChannelSubscriber
from services.ChatService import ChatService
from services.ConnectionService import ConnectionService
from services.ExchangeNotify import ExchangeNotify
from services.ExchangeService import ExchangeService
from services.FollowersNotify import FollowersNotify
from services.FollowersService import FollowersService
from services.FriendsNotify import FriendsNotify
from services.FriendsService import FriendsService
from services.GameFactorySubscriber import GameFactorySubscriber
from services.GameMaster import GameMaster
from services.GameMasterSubscriber import GameMasterSubscriber
from services.GameUtilities import GameUtilities
from services.NotificationListener import NotificationListener
from services.NotificationService import NotificationService
from services.PartyService import PartyService
from services.PresenceService import PresenceService
from services.SearchService import SearchService
from services.ServerPoolService import ServerPoolService
from services.StorageService import StorageService
from services.ToonServiceExternal import ToonServiceExternal
from services.UserManagerNotify import UserManagerNotify
from services.UserManagerService import UserManagerService


class Server(socket.socket):
  def __init__(self, port):
    super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    self.lastRequest = (None, None)
    self.lastResponse = (None, None)
    self.bind(('127.0.0.1', port))
    self.listen(1)
    self.debugging = 1
    self.packets = 0
    self.services = {}
    self.responses = {}
    self.exports = {}
    self.imports = {}
    self.pending = {}
    self.exports[0x00] = self.imports[0x00] = 0x00000000
    self.exports[0xfe] = self.imports[0xfe] = 0xfffffffe
    self.CreateServices()
    self.SetServiceCallbacks()
    self.usedIds = [0x00]
    self.sendBuffer = []

  def CreateServices(self):
    self.services[0x00000000] = ConnectionService()
    self.services[0xfffffffe] = ResponseService()
    self.services[0x0decfc01] = AuthenticationServer()
    self.services[0x83040608] = ChannelInvitationService()
    self.services[0x4124c31b] = ToonServiceExternal()
    self.services[0xe5a11099] = FollowersService()
    self.services[0x3e19268a] = UserManagerService()
    self.services[0xa3ddb1bd] = FriendsService()
    self.services[0xd750148b] = ExchangeService()
    self.services[0xfa0796ff] = PresenceService()
    self.services[0x810cb195] = GameMaster()
    self.services[0xbf8c8094] = ChannelSubscriber()
    self.services[0xb732db32] = Channel()
    self.services[0x71240e35] = AuthenticationClient()
    self.services[0x0cbe3c43] = NotificationService()
    self.services[0xe1cb2ea8] = NotificationListener()
    self.services[0xf084fc20] = ChannelInvitationNotify()
    self.services[0x905cdf9f] = FollowersNotify()
    self.services[0xbc872c22] = UserManagerNotify()
    self.services[0x6f259a13] = FriendsNotify()
    self.services[0xf4e7fa35] = PartyService()
    self.services[0x00d89ca9] = ChatService()
    self.services[0x3fc1274d] = GameUtilities()
    self.services[0x060ca08d] = ChannelOwner()
    self.services[0xc6f9ccc5] = GameFactorySubscriber()
    self.services[0xda6e4bb9] = StorageService()
    self.services[0x166fe4a1] = ExchangeNotify()
    self.services[0x0a24a291] = SearchService()
    
  def SetServiceCallbacks(self):
    self.services[0x00000000].RegisterCallback(0x01, self.OnConnect)
    self.services[0x00000000].RegisterCallback(0x02, self.OnBind)
    
    self.services[0x0decfc01].RegisterCallback(0x01, self.OnLogon)
    
    self.services[0x83040608].RegisterCallback(0x01, self.OnChannelInvitationSubscribe)

    self.services[0xfa0796ff].RegisterCallback(0x01, self.OnPresenceSubscribe)
    
    self.services[0x4124c31b].RegisterCallback(0x01, self.OnToonListRequest)
    
    self.services[0xe5a11099].RegisterCallback(0x01, self.OnFollowersSubscribe)
    
    self.services[0x3e19268a].RegisterCallback(0x01, self.OnUserManagerSubscribe)
    
    self.services[0xa3ddb1bd].RegisterCallback(0x01, self.OnFriendsSubscribe)
    
    self.services[0x810cb195].RegisterCallback(0x02, self.OnListFactories)
    
    
  def NextUnusedId(self, addToUsedList=True):
    id = max(self.usedIds) + 1
    assert(id < 0xfe)
    if addToUsedList:
      self.usedIds += [id]
    return id
    
  def SendToClient(self, packet, message):
    if self.debugging:
      print ' ---------- '
      print 'sending message ' + Utils.MessageType(message)
      print 'message contents:'
      print message
      print ' ---------- '
    self.client.send(Utils.BytesToString(packet))
    
  def BuildResponsePacket(self, method, response, requestPacket):
    payload = Utils.StringToBytes(response.SerializeToString())
    requestId = Utils.ValueToBytes(requestPacket.request, 2)
    length = Utils.ValueToVarInt(len(payload))
    return [0xfe] + [method] + requestId + length + payload
    
  def BuildRequestPacket(self, serviceId, methodId, requestId, unknown, requestMsg):
    payload = Utils.StringToBytes(requestMsg.SerializeToString())
    methodId = Utils.ValueToVarInt(methodId)
    length = Utils.ValueToVarInt(len(payload))
    requestId = Utils.ValueToBytes(requestId, 2)
    unknown = Utils.ValueToVarInt(unknown)
    return [serviceId] + methodId + requestId + unknown + length + payload
    
  def AddToSendBuffer(self, packet, message):
    self.sendBuffer = [(packet, message)] + self.sendBuffer
    
  def ExportToImportId(self, id):
    assert(id in self.exports)
    hash = self.exports[id]
    for impId in self.imports:
      if self.imports[impId] == hash:
        return impId
    raise RuntimeError('import id for export 0x%x not found' % id)
    
  def ImportIdFromHash(self, hash):
    for i in self.imports:
      if self.imports[i] == hash:
        return i
    raise RuntimeError('service 0x%08x not imported' % hash)
    
  def ExportIdFromHash(self, hash):
    for i in self.exports:
      if self.exports[i] == hash:
        return i
    raise RuntimeError('service 0x%08x not exported' % hash)
    
  def Run(self):
    print 'accepting..'
    self.client = None
    while not self.client:
      readfds, writefds, errfds = select.select([self], [], [], 0.3)
      if readfds:
        self.client, _addr = self.accept()
    print 'pulsing..'
    while self.Tick(): pass
      
  def Tick(self):
    readfds, writefds, errfds = select.select([self.client], [], [], 0.1)
    if readfds:
      data = self.client.recv(0x10000)
      if data and len(data) > 0:
        packet = D3Packet(Utils.StringToBytes(data))
        while packet:
          assert(packet.service in self.exports)
          hash = self.exports[packet.service]
          service = self.services[hash]
          rpc = service.GetRpcMethod(packet.method)
          rpc(packet)
          packet = packet.next
      else:
        return False
    else:
      while self.sendBuffer and len(self.sendBuffer) > 0:
        item = self.sendBuffer.pop()
        self.SendToClient(item[0], item[1])
    self.Update()
    return True
    
  def Update(self):
    pass
    
  # *** ConnectionService ***
  
  def OnConnect(self, request, response, packet):
    response.server_id.label = 3882071261
    response.server_id.epoch = int(time.time())
    response.client_id.label = 60996
    response.client_id.epoch = int(time.time())
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    self.lastRequest = (request, packet)
    self.lastResponse = (response, pkt)
    
  def OnBind(self, request, response, packet):
    for hash in request.imported_service_hash:
      id = self.NextUnusedId()
      response.imported_service_id.append(id)
      self.exports[id] = hash
    for export in request.exported_service:
      self.imports[export.id] = export.hash
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    self.lastRequest = (request, packet)
    self.lastResponse = (response, pkt)
    
  # *** AuthenticationServer ***
  
  def OnLogon(self, request, response, packet):
    self.listenerId = request.listener_id
    response.account.high = 72057594037927936
    response.account.low = 23545
    response.game_account.high = 144115608982668339
    response.game_account.low = 5200929
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    self.lastRequest = (request, packet)
    self.lastResponse = (response, pkt)
    
  # *** ChannelInvitationService ***
  
  def OnChannelInvitationSubscribe(self, request, response, packet):
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    self.lastRequest = (request, packet)
    self.lastResponse = (response, pkt)
    notification = channel.AddNotification()
    notification.ParseFromString('\x1a\x94\x02\xaa\x06\x90\x02\x0a\x12\x09\x33\x44\x00\x00\x62\x01\x00\x03\x11\xc8\x2c\xc5\x33\xa3\x54\x63\xcb\x12\x24\x0a\x22\x0a\x0a\x08\xb3\x88\x01\x10\x02\x18\x01\x20\x00\x12\x14\x3a\x12\x08\x08\x10\x03\x18\x04\x20\x0b\x28\x14\x30\x07\x38\x0b\x40\x04\x48\x01\x12\x16\x0a\x14\x0a\x0a\x08\xb3\x88\x01\x10\x03\x18\x01\x20\x00\x12\x06\x18\xb1\x83\x9a\xea\x01\x12\x12\x0a\x10\x0a\x0a\x08\xb3\x88\x01\x10\x03\x18\x02\x20\x00\x12\x02\x18\x01\x12\x35\x0a\x33\x0a\x0a\x08\xb3\x88\x01\x10\x03\x18\x03\x20\x00\x12\x25\x3a\x23\x0a\x02\x20\x00\x0a\x02\x20\x00\x0a\x02\x20\x00\x0a\x02\x20\x00\x0a\x05\x0d\xd9\xeb\x48\x05\x0a\x02\x20\x00\x0a\x02\x20\x00\x0a\x02\x20\x00\x12\x12\x0a\x10\x0a\x0a\x08\xb3\x88\x01\x10\x03\x18\x04\x20\x00\x12\x02\x18\x02\x12\x1f\x0a\x1d\x0a\x0a\x08\xce\x84\x01\x10\x03\x18\x02\x20\x00\x12\x0f\x2a\x0d\x46\x65\x6d\x57\x69\x7a\x61\x72\x64\x23\x37\x33\x36\x12\x12\x0a\x10\x0a\x0a\x08\xce\x84\x01\x10\x03\x18\x03\x20\x00\x12\x02\x10\x00\x12\x14\x0a\x12\x0a\x0a\x08\xce\x84\x01\x10\x03\x18\x09\x20\x00\x12\x04\x42\x02\x44\x33\x12\x12\x0a\x10\x0a\x0a\x08\xce\x84\x01\x10\x03\x18\x0a\x20\x00\x12\x02\x18\x00')
    requestPkt = self.BuildRequestPacket(self.ImportIdFromHash(0xbf8c8094),
    0x01, 0x00, packet.request, notification)
    self.AddToSendBuffer(requestPkt, notification)
    print 'adding AddNotification to send buffer (ChannelInvitationSubscribe)'
  
    
  # *** PresenceService ***
  
  def OnPresenceSubscribe(self, request, response, packet):
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    self.lastRequest = (request, packet)
    self.lastResponse = (response, pkt)
    notification = channel.AddNotification()
    notification.ParseFromString('\x1a\xd4\x01\xaa\x06\xd0\x01\x0a\x12\x09\x00\x00\x00\x00\x00\x00\x00\x01\x11\xf9\x5b\x00\x00\x00\x00\x00\x00\x12\x27\x0a\x25\x0a\x0a\x08\xb3\x88\x01\x10\x01\x18\x01\x20\x00\x12\x17\x3a\x15\x08\xb3\x88\x81\x80\xa0\xac\x80\x80\x03\x10\xc8\xd9\x94\x9e\xb3\x94\xd5\xb1\xcb\x01\x12\x1f\x0a\x1d\x0a\x0a\x08\xce\x84\x01\x10\x01\x18\x01\x20\x00\x12\x0f\x2a\x0d\x44\x72\x65\x79\x66\x61\x6c\x20\x48\x79\x61\x74\x74\x12\x12\x0a\x10\x0a\x0a\x08\xce\x84\x01\x10\x01\x18\x02\x20\x00\x12\x02\x10\x01\x12\x2d\x0a\x2b\x0a\x13\x08\xce\x84\x01\x10\x01\x18\x04\x20\xc6\xd5\xf4\xf3\x96\xa2\x97\x9c\x95\x01\x12\x14\x3a\x12\x09\x33\x44\x00\x00\x62\x01\x00\x03\x11\xf5\x6e\x7d\x6e\x73\x5c\x38\x96\x12\x2d\x0a\x2b\x0a\x13\x08\xce\x84\x01\x10\x01\x18\x04\x20\xfb\xd1\x95\x9e\x93\xb8\xd5\xb1\xc8\x01\x12\x14\x3a\x12\x09\x33\x44\x00\x00\x62\x01\x00\x03\x11\xc8\x2c\xc5\x33\xa3\x54\x63\xcb')
    requestPkt = self.BuildRequestPacket(self.ImportIdFromHash(0xbf8c8094),
    0x01, 0x00, packet.request, notification)
    self.AddToSendBuffer(requestPkt, notification)
    print 'adding AddNotification to send buffer (PresenceSubscribe)'
    
  # *** other ***
  
  def OnToonListRequest(self, request, response, packet):
    response.ParseFromString('\x12\x12\x09\x33\x44\x00\x00\x62\x01\x00\x03\x11\xf5\x6e\x7d\x6e\x73\x5c\x38\x96\x12\x12\x09\x33\x44\x00\x00\x62\x01\x00\x03\x11\xc8\x2c\xc5\x33\xa3\x54\x63\xcb')
    pkt = self.BuildResponsePacket(0x00, response, packet)
    self.SendToClient(pkt, response)
    
  def OnFollowersSubscribe(self, request, response, packet):
    pass
    
  def OnUserManagerSubscribe(self, request, response, packet):
    pass
    
  def OnFriendsSubscribe(self, request, response, packet):
    pass
    
  def OnListFactories(self, request, response, packet):
    pass
  
  
  
  
  
  
  
  
  
  
    
# run server
s = Server(6666)
s.Run()
