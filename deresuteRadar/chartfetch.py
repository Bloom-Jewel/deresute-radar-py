#! /usr/bin/env python
# -*- coding: utf-8 -*-

import locale    as Locale
import codecs    as Codecs
import io        as IO
import sys       as System
import time      as Time
import json      as JSON
import re        as RegExp
from os          import path as OSPath
from collections import OrderedDict
from pathlib     import Path

import urllib.request   as BaseURLRequest
import urllib.error     as BaseURLError

import requests as Request
import requests.exceptions as RequestException

from base.bslib     import ternary as trn
from base.dereconst import DereIdolType, DereIdolDiff

def chart_purge(targetDir):
  listPath  = Path("%s" % (targetDir))
  listFile  = None
  isExists  = listPath.exists()
  isValid   = isExists and listPath.is_dir()
  if not isValid:
    listPath.unlink()
  if isExists:
    endingNum  = RegExp.compile('_\d+$')
    for pathdata in Path('../charts').iterdir():
      basename = OSPath.basename(str(pathdata))
      basename,extname  = basename.split('.',1)
      if (not extname == 'json') or (
        basename == 'list') or (
        basename.endswith('_revised')) or (
        endingNum.fullmatch(basename)):
        continue
      if (not pathdata.is_file()) or (
        ctime > pathdata.lstat().st_mtime + 259200):
        print('purged %s' % basename,file=System.stderr)
        pathdata.unlink()
  else:
    listPath.mkdir()

def fetch_list(targetDir):
  global _chartData, ctime
  listURL   = 'http://cgss.cf/static/list.json'
  listPath  = Path("%s/list.json" % (targetDir))
  isExists  = listPath.exists()
  isValid   = isExists and listPath.is_file() and (
    ctime <= (listPath.lstat().st_mtime + 259200))
  
  if not isValid:
    failData = ("",None)
    try:
      print("%s list, downloading the base song list" % (
        trn(isExists,lambda: 'invalid',lambda: 'non-existing')
      ))
      req = Request.get(listURL)
      req.raise_for_status()
      
      with listPath.open(mode='w',encoding='utf-8') as nlf:
        nlf.write(req.text)
    except RequestException.RequestException as ex:
      failData = ("Failed to download song list %s: %s",ex)
    except Exception as ex:
      failData = ("Exception %s: %s",ex)
    else:
      pass
    finally:
      if failData[0]:
        print(failData[0] % (failData[1].__class__, failData[1]),file=System.stderr)
        System.exit(1)
      else:
        pass
  
  with listPath.open(mode='r',encoding='utf-8') as listFile:
    getStr = listFile.read()
    _chartData = JSON.loads(getStr,object_pairs_hook=OrderedDict)

def fetch_chart(targetDir):
  global _chartData, ctime
  
  for songKey, songData in _chartData.items():
    diffData = OrderedDict([(k,v) for k,v in songData.items() if isinstance(v,list) and len(v) == 3])
    for diffType, diffItem in diffData.items():
      # The following naming format follows the Ruby
      chartName  = "%s_%s" % (songKey,diffType)
      destName   = "%s/%s.json" % (targetDir,chartName)
      diffTitle  = "%s" % (songData['title'])
      diffColor  = "%s (%s) <%s>" % (
        diffTitle,
        DereIdolType[songData['type']].abbrev(), DereIdolDiff[diffType].actual()
      )
      
      songPath   = Path(destName)
      noDownload = songPath.exists()
      
      if not noDownload:
        if not diffItem[2]:
          print("%s not available" % (diffColor),file=System.stderr)
          continue
        
        try:
          req = Request.get("http://cgss.cf/static/pattern2/%s.json" % chartName)
          req.raise_for_status()
          
          with songPath.open("w",encoding="utf-8") as ncf:
            ncf.write(req.text)
        except Exception as ex:
          print("%s failed to download\n\t(%s: %s)" % (
            diffColor, ex.__class__, ex
          ),file=System.stderr)
          continue
        else:
          print("%s downloaded" % (diffColor),file=System.stderr)
      else:
        print("%s loaded" % (diffColor),file=System.stderr)
      
      with songPath.open("r",encoding='utf-8') as songFile:
        jsonData   = JSON.loads(songFile.read(),object_pairs_hook=OrderedDict);
        # to note that, parsing the file IS NOT NECESSARY
        # the actual program that should do this instead.
        pass

# Main Program
def _main(*argv):
  global _chartData, ctime
  
  args      = tuple([len(argv)] + list(argv))
  argc      = (args[0])
  
  ctime     = Time.time()
  
  # Python directory structure is the exception
  # under single-level instead double-level depthness
  chartDir  = "../charts"
  _chartData = OrderedDict([])
  
  chart_purge(chartDir)
  fetch_list(chartDir)
  fetch_chart(chartDir)

# Ensures the main module to be loaded
if __name__ == '__main__':
  _a,_b = System.getdefaultencoding(), Locale.getpreferredencoding()
  if _a != _b:
    System.stdout = Codecs.getwriter(_b)(System.stdout.buffer, 'backslashreplace')
    System.stderr = Codecs.getwriter(_b)(System.stderr.buffer, 'backslashreplace')
  _main(*System.argv[1:])
else:
  raise ImportError("Cannot import '%s' module." % __name__)
