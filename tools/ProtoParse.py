#! /usr/bin/env python


import os, re, sys
from FolderTraveller import FolderTraveller

# note: output is not 100% complete, a few request/response package paths have to be changed
# and the ExchangeService indices are off by 1.


def BuildServiceClass(service):
  m = re.search('service\\s([a-zA-Z]+)\\s{\\s*', service)
  className = m.group(1).strip()
  output = '#! /usr/bin/env python\n\n\nimport Utils\nimport proto.lib.rpc.rpc_pb2 as rpc\nfrom services.BaseService import BaseService\nfrom D3ProtoImports import *\n\n\n'
  output += 'class %s(BaseService):\n' % className
  output += '  def __init__(self):\n'
  output += '    super(%s, self).__init__(\'%s\', 0xdeadbeef)\n' % (className, className)
  output += 'REPLACEMEPLEASE\n'
  rpcs = re.findall('\\s*rpc.+;', service)
  i = 0
  funcNames = {}
  for rpc in rpcs:
    i += 1
    pattern = '\\s*rpc\\s([a-zA-Z]+)\\(\\.bnet\\.protocol\\.([a-zA-Z\\._]+)\\)\\sreturns\\s\\(\\.bnet\\.protocol\\.([a-zA-Z\\._]+)'
    m = re.search(pattern, rpc)
    funcName = m.group(1).strip()
    funcNames[i] = funcName
    requestName = m.group(2).strip()
    if re.search('toon.external', requestName):
      requestName = requestName.replace('toon.external', 'toon_external')
    responseName = m.group(3).strip()
    if responseName == 'NoData':
      responseName = 'rpc.NoData'
    elif responseName == 'NO_RESPONSE':
      responseName = 'rpc.NO_RESPONSE'
    elif re.search('toon.external', responseName):
      responseName = responseName.replace('toon.external', 'toon_external')
    
    output += '  def %s(self, packet):\n' % funcName
    output += '    request = Utils.LoadRequest(%s(), packet)\n' % requestName
    output += '    response = %s()\n' % responseName
    output += '    return self.PerformRpc(0x%02x, request, response, packet)\n\n' % i
  init = ''
  for index in range(1, i + 1):
    init += '    self.rpc[0x%02x] = self.%s\n' % (index, funcNames[index]) 
  output = output.replace('REPLACEMEPLEASE', init)
  f = open('./gen/%s.py' % className, 'w')
  f.write(output.strip())
  f.close()
          
def ExtractServices(path):
  path = path.strip()
  if re.search('\\.proto$', path):
    f = open(path)
    text = f.read(0x10000)
    pattern = 'service\\s[a-zA-Z]*\\s{\\s*[a-zA-Z\\s\\.\\(\\);_]*}'
    services = re.findall(pattern, text)
    for service in services:
      BuildServiceClass(service)
      

rootPath = '../libs/definitions'
traveller = FolderTraveller(rootPath)
traveller.OnFile(ExtractServices)
traveller.Run()
