#! /usr/bin/env python

# NOTHIGN YET, GO AWAY.

'''
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


import socket

class Server(socket.socket):
  def __init__(self, port):
    super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
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
    self.usedIds = []
    
  def NextUnusedId(self):
    return max(self.usedIds) + 1
  
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
    # add moar
    
  def Run(self):
    self.client, _addr = self.accept()
    


'''

print 'hi :-)'