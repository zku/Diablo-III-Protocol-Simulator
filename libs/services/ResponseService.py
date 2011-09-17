#! /usr/bin/env python


class ResponseService(object):
  def __init__(self):
    self.name = 'ResponseService'
    self.hash = 0xfffffffe
    self.debugging = 1
    self.callback = None
    self.rpc = {}
    self.rpc[0] = self.Response
    
  def Response(self, packet):
    if self.callback:
      return [self.callback(packet), None]
    else:
      return None
      
  def RegisterCallback(self, callback):
    self.callback = callback
    return self
    
  def GetRpcMethod(self, methodId):
    return self.rpc[0]