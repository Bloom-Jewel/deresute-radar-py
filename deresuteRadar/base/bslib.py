#! /usr/bin/env python

from sys  import stdin,stdout,stderr
from enum import Enum as BaseEnum

def ternary(cond, res_true, res_false):
  sel_val = None
  if cond:
    sel_val = res_true
  else:
    sel_val = res_false
  
  if callable(sel_val):
    return sel_val()
  else:
    return sel_val

class Enum(BaseEnum):
  @classmethod
  def aliases(cls):
    return [name for name, member in cls.__members__.items() if member.name != name]
  
  @classmethod
  def names(cls):
    return cls._member_names_
  
  @classmethod
  def get(cls,key):
    if key in cls.names():
      return [member for name,member in cls.__members__.items() if member.name == key][0]
    elif key is cls:
      return key
    else:
      return None

if __name__ == '__main__':
  print("Load test, OK!")
else:
  print("Loaded %s" % __name__,file=stderr)
