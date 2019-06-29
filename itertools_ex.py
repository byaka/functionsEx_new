# -*- coding: utf-8 -*-
import types, collections

"""
Collection of methods for working with Generators, which respects `yield .. send ..` ability.
"""

def gExtend(prepend, g, append=None):
   _gType=types.GeneratorType
   _iType=collections.Iterable
   if not isinstance(g, _gType):
      raise TypeError('Wrong type, second arg must be Generator')
   if isinstance(prepend, _gType): gPrepend=prepend
   elif isinstance(prepend, _iType): gPrepend=g
   else:
      raise TypeError('Wrong type, first arg must be Generator or Iterable')
   if append is None: gAppend=None
   elif isinstance(append, _gType): gAppend=append
   elif isinstance(append, _iType): gAppend=None
   else:
      raise TypeError('Wrong type, arg `append` must be Generator or Iterable')
   for v in prepend:
      extCmd=(yield v)
      if extCmd is not None:
         yield  # this allows to use our generator inside `for .. in ..` without skipping on `send`
         gPrepend.send(extCmd)
   #
   for v in g:
      extCmd=(yield v)
      if extCmd is not None:
         yield  # this allows to use our generator inside `for .. in ..` without skipping on `send`
         g.send(extCmd)
   #
   if append is not None:
      for v in prepend:
         extCmd=(yield v)
         if extCmd is not None:
            yield  # this allows to use our generator inside `for .. in ..` without skipping on `send`
            if gAppend is not None:
               gAppend.send(extCmd)

def gCheck(g):
   try:
      return gExtend((next(g),), g)
   except StopIteration:
      return ()

def gChain(*gens):
   for g in gens:
      isGen=isinstance(g, types.GeneratorType)
      for o in g:
         extCmd=(yield o)
         if extCmd is not None:
            yield  # this allows to use our generator inside `for .. in ..` without skipping on `send`
            if isGen:
               g.send(extCmd)

def grouper(n, obj, fill=None):
   # group items by n (ABCDEFG --> ABC DEF Gxx if n=3)
   args=[iter(obj)]*n
   return izip_longest(fill=fill, *args)
