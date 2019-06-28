



if PY_V<2.7:
   class deque2(collections.deque):
      """
      This class add support of <maxlen> for old deque in python2.6.
      Thx to Muhammad Alkarouri.
      http://stackoverflow.com/a/4020363
      """
      def __init__(self, iterable=(), maxlen=None):
         collections.deque.__init__(self, iterable, maxlen)
         self._maxlen=maxlen

      @property
      def maxlen(self):
         return self._maxlen
else:
   deque2=collections.deque

class CaseInsensitiveDict(dict):
   @classmethod
   def _k(cls, key):
      return key.lower() if isinstance(key, basestring) else key

   def __init__(self, *args, **kwargs):
      super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
      self._convert_keys()
   def __getitem__(self, key):
      return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
   def __setitem__(self, key, value):
      super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
   def __delitem__(self, key):
      return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
   def __contains__(self, key):
      return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
   def has_key(self, key):
      return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
   def pop(self, key, *args, **kwargs):
      return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
   def get(self, key, *args, **kwargs):
      return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
   def setdefault(self, key, *args, **kwargs):
      return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
   def update(self, E={}, **F):
      super(CaseInsensitiveDict, self).update(self.__class__(E))
      super(CaseInsensitiveDict, self).update(self.__class__(**F))
   def _convert_keys(self):
      for k in list(self.keys()):
         v = super(CaseInsensitiveDict, self).pop(k)
         self.__setitem__(k, v)

class MagicDict(dict):
   """
   Get and set values like in Javascript (dict.<key>).
   """
   def __getattr__(self, k):
      if k[:2]=='__': raise AttributeError(k)  #for support PICKLE protocol and correct isFunction() check
      return self.__getitem__(k)

   # __getattr__=dict.__getitem__
   __setattr__=dict.__setitem__
   __delattr__=dict.__delitem__
   __reduce__=dict.__reduce__
magicDict=MagicDict

class MagicDictCold(MagicDict):
   """
   Extended MagicDict, that allow freezing.
   """
   def __getattr__(self, k):
      if k=='__frozen': return object.__getattribute__(self, '__frozen')
      return MagicDict.__getattr__(self, k)

   def __freeze(self):
      object.__setattr__(self, '__frozen', True)

   def __unfreeze(self):
      object.__setattr__(self, '__frozen', False)

   def __setattr__(self, k, v):
      if getattr(self, '__frozen', None): raise RuntimeError('Frozen')
      MagicDict.__setattr__(self, k, v)

   def __setitem__(self, k, v):
      if getattr(self, '__frozen', None): raise RuntimeError('Frozen')
      MagicDict.__setitem__(self, k, v)

   def __delattr__(self, k):
      if getattr(self, '__frozen', None): raise RuntimeError('Frozen')
      MagicDict.__delattr__(self, k)

   def __delitem__(self, k):
      if getattr(self, '__frozen', None): raise RuntimeError('Frozen')
      MagicDict.__delitem__(self, k)
magicDictCold=MagicDictCold

def dict2magic(o, recursive=False):
   if recursive:
      if isArray(o) or isDict(o) or isSet(o) or isTuple(o):
         for i in (o if isDict(o) else xrange(len(o))):
            o[i]=dict2magic(o[i], recursive=True)
         if isDict(o): o=MagicDict(o)
   elif isDict(o):
      o=MagicDict(o)
   return o
dictToMagic=dict2magic

