# -*- coding: utf-8 -*-


def parseFloatEx(s):
   v=regExp_parseFloat.search(s)
   if not v: return 0
   return float(v.group(0))
