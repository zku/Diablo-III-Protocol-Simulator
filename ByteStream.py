#! /usr/bin/env python


class ByteStream:
  def __init__(self, bytes):
    self.length = len(bytes)
    self.bytes = bytes
    self.index = 0
  
  def HasBytes(self):
    return self.index < self.length
  
  def NextByte(self):
    byte = self.bytes[self.index]
    self.index += 1
    return byte
    
  def NextBytes(self, count):
    ret = []
    for i in range(0, count):
      ret += [self.NextByte()]
    return ret
  
  def NextVarInt(self):
    sum = 0
    shift = 0
    while 1:
      sum += (self.bytes[self.index] & 0x7f) << shift
      shift += 7
      self.index += 1
      if (self.bytes[self.index - 1] & 0x80) == 0:
        break
    return sum
    
  def NextWord(self):
    return self.NextByte() | (self.NextByte() << 8)
    
  def NextInt32(self):
    return self.NextWord() | (self.NextWord() << 16)
    
  def NextInt64(self):
    return self.NextInt32() | (self.NextInt32() << 32)
    
  def Skip(self, number):
    self.index += number
    
  def Remaining(self):
    return self.bytes[self.index:]
    