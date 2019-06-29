# -*- coding: utf-8 -*-

import random, sys

def randomEx_default_soLong(mult, vals, pref, suf, i):
   if i>100:
      raise OverflowError('randomeEx generating so long (%s attempts)'%i)
   print '!! randomEx: generating value so long for (%s, %s, %s), attempt %s to incress range'%(pref, mult, suf, i)
   if randomEx_default_soLong.sleepMethod:
      randomEx_default_soLong.sleepMethod(0.1)
   return mult*2
randomEx_default_soLong.sleepMethod=None

def randomEx(mult=None, vals=None, pref='', suf='', soLong=0.01, cbSoLong=None):
   """
   This method generate random value from 0 to <mult> and add prefix and suffix.
   Also has protection against the repeating values and against recurrence (long generation).

   :param int|None mult: If None, 'sys.maxint' will be used.
   :param list|dict|str vals: Blacklist of generated data.
   :param str pref: Prefix.
   :param str suf: Suffix.
   :param int soLong: Max time in seconds for generating.
   :param func cbSoLong: This function will called if generating so long. It can return new <mult>. If return None, generating will be aborted.
   :return str: None if some problems or aborted.
   """
   mult=mult or sys.maxint
   soLong=soLong*1000  # to ms
   if cbSoLong is None:
      cbSoLong=randomEx_default_soLong
   vals=vals or {}
   s=None
   toStr=isString(pref) and isString(suf)
   soLong_i=0
   mytime=getms()
   while not s or s in vals:
      s=int(random.random()*mult)
      if toStr:
         s=pref+str(s)+suf
      # defence frome freeze
      if (getms()-mytime)>soLong:
         soLong_i+=1
         mytime=getms()
         if callable(cbSoLong):
            mult=cbSoLong(mult, vals, pref, suf, soLong_i)
            if mult is not None: continue
         return None
   return s

