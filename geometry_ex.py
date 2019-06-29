# -*- coding: utf-8 -*-
import math

def pointCheck(A,B,C):
   #check, if point C is on left side (>0) or right side(<0) from AB or belong AB (=0)
   return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])

def intersectCheck(A,B,C,D):
   s1=pointCheck(A,B,C)*pointCheck(A,B,D)
   s2=pointCheck(C,D,A)*pointCheck(C,D,B)
   return [s1<=0 and s2<=0,s1,s2]

def reRound(val, to=100, asFloat=True):
   if(abs(val)<to): return val
   s=val/to
   s=(s-math.floor(s))*to
   if not asFloat: s=int(s)
   return s

def reAngle(val):
   val=reRound(val, 360)
   if val<=0: val+=360
   return val
