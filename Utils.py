#! /usr/bin/env python


import sys, os
from ByteStream import ByteStream

def BytesToHtml(bytes):
  result = ''
  for byte in bytes:
    result += '%02x ' % byte
  return result

def LoadRequest(request, packet):
  if packet.HasPayload():
    request.ParseFromString(packet.PayloadAsString())
  return request

def TypeCheck(obj, typeName):
  assert(obj.__class__.__name__ == typeName)

def FileBytes(filepath):
  f = open(filepath, 'rb')
  f.seek(0, os.SEEK_END)
  size = f.tell()
  f.seek(-size, os.SEEK_END)
  data = f.read(size)
  return StringToBytes(data)
  
def ParseProtoBuffer(bs):
  fields = {}
  while bs.HasBytes():
    key = bs.NextVarInt()
    wireType = key & 0x3
    fieldNumber = key >> 3
    if wireType == 0:     # varint
      fields[fieldNumber] = bs.NextVarInt()
    elif wireType == 1:   # fixed 64bit
      fields[fieldNumber] = bs.NextInt64()
    elif wireType == 2:   # length delimited
      length = bs.NextVarInt()
      bytes = bs.NextBytes(length)
      fields[fieldNumber] = BytesToString(bytes)
    elif wireType == 3:   # start group
      raise RuntimeError('depreciated, cba to handle')
    elif wireType == 4:   # end group
      raise RuntimeError('depreciated, cba to handle')
    elif wireType == 5:   # fixed 32bit
      fields[fieldNumber] = bs.NextInt32()
    else:
      raise RuntimeError('unknown wire type %d' % wireType)
  return fields
  
def FileByteStream(filepath):
  return ByteStream(FileBytes(filepath))

def StringToBytes(string):
  return map(lambda x: ord(x), string)
  
def BytesToString(bytes):
  string = ''
  for byte in bytes:
    string += chr(byte)
  return string

def ValueToBytes(value, minLength):
  num = 0
  while pow(2, num * 8) <= value:
    num += 1
  bytes = []
  for i in range(0, num):
    bytes += [(value >> (i * 8)) & 0x00000000000000ff]
  while len(bytes) < minLength:
    bytes += [0x00]
  return bytes
  
def ValueToVarInt(value):
  num = 0
  while pow(2, num * 7) <= value:
    num += 1
  if num <= 1:
    return [value]
  bytes = []
  for i in range(0, num):
    bytes += [(value >> (i * 7)) & 0x00000000000000ff]
  for i in range(0, num - 1):
    bytes[i] = bytes[i] | 0x80
  return bytes

def HexDump(data):
  if type(data) == str:
    data = StringToBytes(data)
  output = ' ' * 5
  for i in range(0, 16):
    output += '%02x ' % i
  output += '\n' + 5 * ' ' + 47 * '-' + '\n0000 '
  count = 0
  for byte in data:
    output += '%02x' % byte
    count += 1
    if (count % 16) == 0:
      output += '\n%04x ' % (int(count / 16) * 16)
    else:
      output += ' '
  return output.rstrip()