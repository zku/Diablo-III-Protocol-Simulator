#! /usr/bin/env python


import Utils

class BaseService(object):
  def __init__(self, name, hash):
    self.name = name
    self.hash = hash
    self.debugging = 1
    self.rpc = {}
    self.callbacks = {}
    
  def DebugMessage(self, message):
    print 'dbg'
    if self.debugging:
      print message.__class__.__name__
      print message
      
  def RegisterCallback(self, methodId, callback):
    self.callbacks[methodId] = callback
    return self
    
  def Callback(self, methodId):
    if methodId in self.callbacks:
      return self.callbacks[methodId]
    else:
      return None
    
  def PerformCallback(self, methodId, request, response, packet):
    callback = self.Callback(methodId)
    if callback:
      return callback(request, response, packet)
    else:
      return response
      
  def PerformRpc(self, methodId, request, response, packet):
    if packet.HasPayload():
      request.ParseFromString(Utils.BytesToString(packet.payload))
    self.DebugMessage(request)
    return (self.PerformCallback(methodId, request, response, packet), request)
    
  def GetRpcMethod(self, methodId):
    return self.rpc[methodId]