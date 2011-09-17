#! /usr/bin/env python


import os, sys

class FolderTraveller:
  def __init__(self, root, recursive=True):
    self.root = root
    self.recursive = recursive
    self.onFile = self.Dummy
    self.onFolder = self.Dummy
    
  def Dummy(self, fullPath):
    pass
    
  def OnFile(self, callback):
    self.onFile = callback
    
  def OnFolder(self, callback):
    self.onFolder = callback
    
  def Run(self):
    self._InternalRun(self.root)
        
  def _InternalRun(self, path):
    for f in os.listdir(path):
      fullPath = path + '/' + f
      if os.path.isfile(fullPath):
        self.onFile(fullPath)
      else:
        self.onFolder(fullPath)
        if self.recursive:
          self._InternalRun(fullPath)