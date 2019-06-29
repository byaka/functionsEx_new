# -*- coding: utf-8 -*-

import time, datetime

timetime=time.time
datetime_now=datetime.datetime.now
date_now=datetime.date.today

def time2human(val, inMS=True):
   if not inMS: val=val*1000.0
   d=24*60*60*1000.0
   h=60*60*1000.0
   m=60*1000.0
   s=1000.0
   ms=1
   mks=0.001
   ns=0.000001
   if not val: val='0'
   elif val>=d: val='%.2fd'%(val/d)
   elif val>=h: val='%.2fh'%(val/h)
   elif val>=m: val='%.1fm'%(val/m)
   elif val>=s: val='%.1fs'%(val/s)
   elif val>=ms: val='%.0fms'%(val/ms)
   elif val>=mks: val='%.0fmks'%(val/mks)
   else: val='%.0fns'%(val/ns)
   return val

def timestamp2unix(text, f='%d/%m/%Y %H:%M:%S'):
   #convert string to time
   t0=datetime.datetime.strptime(text, f)
   t1=time.mktime(t0.timetuple())
   return round(t1)
