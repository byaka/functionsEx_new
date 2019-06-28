# -*- coding: utf-8 -*-

import sys, time, datetime

timetime=time.time
datetime_now=datetime.datetime.now
date_now=datetime.date.today

global PY_V
PY_V=float(sys.version[:3])

class NullUnique(object):
   def __str__(self):
      return 'Null(unique)'

global Null, NULL
NULL=Null=null=NullUnique()

global INFINITY, Infinity
INFINITY=Infinity=float('Inf')
