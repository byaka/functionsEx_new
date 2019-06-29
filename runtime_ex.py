# -*- coding: utf-8 -*-

import sys, traceback, os, ctypes

class ErrorHandler(object):
   __metaclass__=Singleton

   def __init__(self, cb=None, passErrorObjectToCB=False):
      self.cb=cb or self.cbDefault
      self.passErrorObjectToCB=passErrorObjectToCB
      sys.excepthook=self.__hook

   def __hook(self, *errObj):
      if issubclass(errObj[0], KeyboardInterrupt):
         return sys.__excepthook__(*errObj)
      if self.passErrorObjectToCB:
         self.cb(errObj)
      else:
         errStr=''.join(traceback.format_exception(*errObj))
         self.cb(errStr)

   @classmethod
   def cbDefault(cls, err):
      isTerm=consoleIsTerminal()
      if isTerm:
         err=consoleColor.bold+consoleColor.red+err+consoleColor.end
      print err
      if isTerm:
         r=raw_input('Programm paused, press any key to exit\nOr type "dbg" for starting debugger\n')
         if r and r.lower()=='dbg':
            import pdb; pdb.pm()
         sys.exit(1)

   @classmethod
   def disable(cls):
      sys.excepthook=sys.__excepthook__

def selfInfo(step=-2):
   module, line, name, code=traceback.extract_stack()[step]
   return MagicDict({'module':module, 'line':line, 'name':name, 'path':getScriptPath()})

def getScriptPath(full=False, real=True, f=None):
   """
   This method return path of current script. If <full> is False return only path, else return path and file name.

   :param bool full:
   :return str:
   """
   f=f or sys.argv[0]
   if full:
      return os.path.realpath(f) if real else f
   else:
      return os.path.dirname(os.path.realpath(f) if real else f)

def getScriptName(withExt=False, f=None):
   """
   This method return name of current script. If <withExt> is True return name with extention.

   :param bool withExt:
   :return str:
   """
   f=f or sys.argv[0]
   if withExt:
      return os.path.basename(f)
   else:
      return os.path.splitext(os.path.basename(f))[0]

try:  # Python 2
   _getsize_zeroDepth=(basestring, Number, xrange, bytearray)
   _getsize_iteritems='iteritems'
except NameError:  # Python 3
   _getsize_zeroDepth=(str, bytes, Number, range, bytearray)
   _getsize_iteritems='items'

def getsize(obj_0, seen=None):
   """Recursively iterate to sum size of object & members."""
   if not isSet(seen): seen=set()
   def inner(obj, _seen):
      obj_id=id(obj)
      if obj_id in _seen:
         return 0
      _seen.add(obj_id)
      size=sys.getsizeof(obj)
      if isinstance(obj, _getsize_zeroDepth):
         pass # bypass remaining control flow and return
      elif isinstance(obj, (tuple, list, Set, deque)):
         size+=sum(inner(i, _seen) for i in obj)
      elif isinstance(obj, Mapping) or hasattr(obj, _getsize_iteritems):
         try:
            tArr=getattr(obj, _getsize_iteritems)()
         except TypeError:
            tArr=()
         size+=sum(inner(k, _seen)+inner(v, _seen) for k, v in tArr)
      # Check for custom object instances - may subclass above too
      if hasattr(obj, '__dict__'):
         size+=inner(vars(obj), _seen)
      if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
         size+=sum(inner(getattr(obj, s), _seen) for s in obj.__slots__ if hasattr(obj, s))
      return size
   return inner(obj_0, seen)

def findObjectById(s):
   """ Try to find python object by given id(object). """
   # return _ctypes.PyObj_FromPtr(s)
   return ctypes.cast(s, ctypes.py_object).value
