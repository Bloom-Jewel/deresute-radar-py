#! /usr/bin/env python

from sys   import stdin,stdout,stderr

from .bslib import ternary, Enum

class DereIdolType(Enum):
  all = 0,"ZN"
  cu  = 1,"CT"
  co  = 2,"CL"
  pa  = 3,"PS"
  
  def abbrev(self):
    return self.value[1]

class DereIdolDiff(Enum):
  debut      = 0, "Debut"   , "DB"
  regular    = 1, "Regular" , "RG"
  pro        = 2, "Pro"     , "PR"
  master     = 3, "Master"  , "MS"
  masterplus = 4, "Master+" , "MSP"
  
  def actual(self):
    return self.value[1]
  def abbrev(self):
    return self.value[2]

if __name__ == '__main__':
  for cls in [DereIdolType,DereIdolDiff]:
    for idtp in list(cls):
      print("%s\t%s" % (idtp,idtp.value))
  print("Load test, OK!")
else:
  print("Loaded %s" % __name__,file=stderr)
