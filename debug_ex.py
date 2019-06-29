# -*- coding: utf-8 -*-
import timeit, sys, traceback, inspect

def timeitMe(f, n=100, m=None):
   if m is None:
      m=3 if n>1 else 1
   _m=float(m)
   tArr1=tuple(s/_m for s in timeit.repeat(f, number=m, repeat=n))
   s='<%s> %i*%i repeats: min=%s, mid=%s, max=%s'
   print s%(f.__name__, m, n, time2human(min(tArr1), inMS=False), time2human(arrMedian(tArr1), inMS=False), time2human(max(tArr1), inMS=False))

def getErrorRaw():
   return sys.exc_info()

def getErrorInfo(fallback=False, raw=False):
   """
   This method return info about last exception.

   :return str:
   """
   if not fallback and not raw:
      return traceback.format_exc()
   tArr=inspect.trace()[-1]
   fileName=getScriptName(f=tArr[1])
   lineNo=tArr[2]
   _, eObj, eTB=sys.exc_info()
   if raw:
      res=(fileName, lineNo, eObj, eTB)
   else:
      res='%s:%s > %s'%(fileName, lineNo, eObj)
   sys.exc_clear()
   return res
