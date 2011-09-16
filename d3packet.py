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

import util
from bytestream import ByteStream

class D3Packet:
  def __init__(self, bytes, recursive=True):
    if len(bytes) <= 4:
      raise RuntimeError('invalid packet length %d' % len(bytes))
    self.bytes = bytes
    self.stream = ByteStream(bytes)
    self.service = self.stream.NextByte()
    self.method = self.stream.NextVarInt()
    self.request = self.stream.NextWord()
    self.payload = None
    if not self.IsAnswer():
      self.unknown = self.stream.NextVarInt()
    self.size = self.stream.NextVarInt()
    if self.size > 0:
      self.payload = bytes[:self.stream.index+self.size]
      self.payload = self.payload[self.stream.index:]
    self.next = None
    if recursive and self.stream.index + self.size < len(bytes):
      self.next = D3Packet(bytes[self.stream.index + self.size:])
  
  def HasPayload(self):
    return self.payload and self.payload > 0
    
  def PayloadString(self):
    if self.HasPayload():
      return util.HexDump(self.payload)
    else:
      return 'no payload!'
      
  def PayloadAsString(self):
    return util.BytesToString(self.payload)
    
  def IsAnswer(self):
    return self.service == 0xfe
    
  def HeaderString(self):
    if self.service == 0xfe:
      return 'Answer [service=0x%x] [method=0x%x] [request=0x%x] [size=0x%x]' % (self.service,
      self.method, self.request, self.size)
    else:
      return '[service=0x%x] [method=0x%x] [request=0x%x] [unknown=0x%x] [size=0x%x]' % (self.service,
      self.method, self.request, self.unknown, self.size)
  
  def SizeAsVarInt(self):
    return util.ValueToVarInt(self.size)
    
  def Remainder(self):
    return self.bytes[self.stream.index + self.size:]
    
  def Guess(self):
    if not self.HasPayload():
      return {}
    bs = ByteStream(self.payload)
    return util.ParseProtoBuffer(bs)
      
      