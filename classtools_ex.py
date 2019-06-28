# -*- coding: utf-8 -*-



def ClassFactory(base, extend, fixPrivateAttrs=True):
   """ Возвращает новый класс, являющийся суб-классом от `base` и цепочки `extend`. """
   extend=(base,)+tuple(extend) if extend else ()
   name='_'.join(cls.__name__ for cls in extend)
   extend=tuple(reversed(extend))
   attrs={}
   if fixPrivateAttrs:
      # фиксит специфичный для питона подход к приватным атрибутам, добавляя поддержку специальных приватные атрибуты, начинающиеся на `___` (например self.___test). к ним можно получить доступ из любого суб-класс, но не извне
      #~ оверхед для обычных приватных атрибутов отсутствует, для новых он порядка x10, такчто не стоит использовать их в критичных по скорости участках
      #? одна из потенциальных оптимизаций: отказ от замыканий `bases`, `name`, `nCache` но пока неясно как это лучше сделать
      bases=[('_%s___'%cls.__name__, len(cls.__name__)+4) for cls in extend]
      objSetM=object.__setattr__
      objGetM=object.__getattribute__
      objDelM=object.__delattr__
      nCache={}
      def tFunc_setattr(self, key, val):
         if key in nCache: key=nCache[key]
         elif '___' in key:
            for s, l in bases:
               if key[:l]!=s: continue
               k=key
               key='_'+name+'___'+key[l:]
               nCache[k]=key
               break
         return objSetM(self, key, val)
      def tFunc_getattr(self, key):
         key2=None
         if key in nCache: key2=nCache[key]
         elif '___' in key:
            for s, l in bases:
               if key[:l]!=s: continue
               key2='_'+name+'___'+key[l:]
               nCache[key]=key2
               break
         if key2:
            return objGetM(self, key2)
         else:
            raise AttributeError("'%s' object has no attribute '%s'"%(name, key))
      def tFunc_delattr(self, key):
         if key in nCache: key=nCache[key]
         elif '___' in key:
            for s, l in bases:
               if key[:l]!=s: continue
               k=key
               key='_'+name+'___'+key[l:]
               nCache[k]=key
               break
         return objDelM(self, key)
      attrs['__getattr__']=tFunc_getattr
      attrs['__setattr__']=tFunc_setattr
      attrs['__delattr__']=tFunc_delattr
   cls=type(name, extend, attrs)
   return cls

class Singleton(type):
   _instances={}
   def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
         cls._instances[cls]=super(Singleton, cls).__call__(*args, **kwargs)
      #? this allows to call `__init__` each time when class requested, but not sure how to add this configurable
      # else:
      #    cls._instances[cls].__init__(*args, **kwargs)
      return cls._instances[cls]
