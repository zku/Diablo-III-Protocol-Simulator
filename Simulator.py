#! /usr/bin/env python


import Utils
from D3Packet import D3Packet

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

class Entity:
  def __init__(self, role, sim):
    self.sim = sim
    self.debugging = 1
    self.role = role
    self.other = None
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
    self.services[0x00000000].RegisterCallback(0x02, self.OnBind)
    self.services[0xfffffffe].RegisterCallback(self.OnResponse)
    
  def Send(self, packet, allPackets):
    self.packets += 1
    print '\n\n*** %s received packet ***' % self.role
    print '> this is total packet 0x%04x' % allPackets
    print '> this is %s\'s 0x%04x-th received packet' % (self.role, self.packets)
    print '> packet header: %s' % packet.HeaderString()
    print '> packet payload/protobuffer:\n' + packet.PayloadString()
    if packet.service in self.exports:
      hash = self.exports[packet.service]
      service = self.services[hash]
      rpc = service.GetRpcMethod(packet.method)
      response, request = rpc(packet)
      direction = 's2c' if self.role == 'client' else 'c2s'
      if hash != 0xfffffffe:
        assert(response and request)
        self.sim.LogHtml(request, packet, direction)
        self.other.responses[packet.request] = (response, packet, request)
      else:
        assert(response and not request)
        self.sim.LogHtml(response, packet, direction)
    else:
      raise RuntimeError('service binding not properly handled')
      
  def OnBind(self, request, response, packet):
    self.pending[packet.request] = []
    for hash in request.imported_service_hash:
      self.pending[packet.request] += [hash]
    for export in request.exported_service:
      self.imports[export.id] = export.hash
      self.other.exports[export.id] = export.hash
    return response
  
  def OnResponse(self, packet):
    requestId = packet.request
    if requestId in self.responses:
      t = self.responses[requestId]
      response = t[0]
      requestPacket = t[1]
      request = t[2]
      assert(requestPacket.request == packet.request)
      if packet.HasPayload():
        response.ParseFromString(packet.PayloadAsString())
      if self.debugging:
        print response.__class__.__name__
        print response
      if response.__class__.__name__ == 'BindResponse':
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
      elif response.__class__.__name__ == 'ExecuteResponse':
        self.DumpExecuteResponse(request, response)
      return response
    else:
      raise RuntimeError('no request stored for this response, inconsistent..')

  def DumpExecuteResponse(self, request, response):
    if request.HasField('query_name') and request.query_name == 'GetHeroDigests':
      for result in response.results:
        for cell in result.data:
          data = cell.data
          if data and len(data) > 0:
            digest = Hero.Digest()
            digest.ParseFromString(data)
            print digest
    
class Simulator:
  def __init__(self):
    self.html = open('output/index.html', 'w')
    self.c = Entity('client', self)
    self.s = Entity('server', self)
    self.c.other = self.s
    self.s.other = self.c
    self.all = Utils.FileBytes('data/all.dat')
    self.c2s = Utils.FileBytes('data/c2s.dat')
    self.s2c = Utils.FileBytes('data/s2c.dat')
  
  def Run(self):
    print 'Simulating protocol'
    self.html.write('<html><head><title>Diablo III Protocol Simulator by sku/thesku</title></head><link rel="stylesheet" type="text/css" href="css/style.css" /><body><div id="log">\n')
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
        raise RuntimeError('unknown packet sender / streams malformed')
      recipient.Send(allPacket, allPackets)
    assert(len(self.all) == 0 and len(self.c2s) == 0 and len(self.s2c) == 0)
    self.html.write('</div></body></html>')
    self.html.close()
    
  def LogHtml(self, message, packet, direction):
    html = self.html
    html.write('<div align="center">')
    html.write('<table class="%s">' % direction)
    if direction == 's2c':
      title = 'server -> client'
    else:
      title = 'client -> server'
    title += ' :: ' + Utils.MessageType(message) + ' :: ' + packet.HeaderString()
    html.write('<tr><td class="title">%s</td></tr>' % title)
    html.write('<tr><td class="hexdump">%s</td></tr>' % (Utils.BytesToHtml(packet.payload) if packet.HasPayload() else 'no payload'))
    proto = ('empty' if len(str(message).strip()) == 0 else str(message))
    html.write('<tr><td class="proto">%s</td></tr></table></div>\n' % proto.strip())
    
sim = Simulator()
sim.Run()
print 'completed simulation'