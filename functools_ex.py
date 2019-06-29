# -*- coding: utf-8 -*-

import types, inspect

def callIgnoreErrors(method, args=None, kwargs=None, ignoreErr=None, limit=5, sleepTime=lambda i:(1<<(i*2))/1000.0, logMethod=None, sleepMethod=None):
   # вызывает переданную функцию, отслеживая ошибки. в случае возникновения ошибки из переданного сиска типов, вызывает функцию повторно, делаю паузу между вызовами. количество попыток может быть лимитировано, пауза между ними может меняться (поумолчанию растет экспоненциально). весь процесс логируется. в случае успеха вернет результат работы функции.
   logMethod=logMethod if callable(logMethod) else False
   sleepMethod=sleepMethod if callable(sleepMethod) else False
   if not ignoreErr:
      ignoreErr=(None,)
   elif ignoreErr is True:
      ignoreErr=(Exception,)
   args=args or []
   kwargs=kwargs or {}
   _methodStr=str(method)
   _sleepTime=sleepTime if isNum(sleepTime) else None
   errI=0
   while True:
      if limit and errI>limit:
         s='Max attempts reached while call %s'%(_methodStr)
         if logMethod: logMethod(1, s)
         raise ValueError(s)
      if errI:
         if sleepMethod and sleepTime:
            s=_sleepTime or sleepTime(errI)
            if logMethod:
               logMethod(3, 'Attempt [%s] to call'%errI, _methodStr, 'with sleep(%s)'%s)
            sleepMethod(s)
         else:
            if logMethod:
               logMethod(3, 'Attempt [%s] to call'%errI, _methodStr)
      #
      try:
         return method(*args, **kwargs)
      except ignoreErr:
         if not errI and not limit:  # show warning only 1 time
            if logMethod: logMethod(2, 'No limit setted while call', _methodStr, 'this can cause infinity loop')
         errI+=1
      except Exception, e:
         if logMethod: logMethod(1, 'Unknown error while call %s: %s'%(_methodStr, getErrorInfo()))
         raise e

def bind(f, defaultsUpdate=None, globalsUpdate=None, name=None):
   """
   Returns new function, similar as <f>, but with redefined default keyword-arguments values and updated globals.

   It have similar use-cases like `functools.partial()`, but executing few times faster (with cost of longer initialisation) and also faster than original function, if you pass alot args.

   :param func f:
   :param str name:
   :param dict globalsUpdate: Update global-env for new function, but only for this function, so not modify real globals
   :param dict defaultsUpdate: Update default keyword-arguments
   """
   p={
      'name':name or f.func_name+'_BINDED',
      'code':f.func_code,
      'globals':f.func_globals,
      'argdefs':f.func_defaults,
      'closure':f.func_closure
   }
   if globalsUpdate:
      p['globals']=p['globals'].copy()
      p['globals'].update(globalsUpdate)
   if defaultsUpdate:
      _args=inspect.getargs(f.func_code)[0]
      _defsL=len(p['argdefs'])
      _offset=len(_args)-_defsL
      p['argdefs']=list(p['argdefs'])
      for i in xrange(_defsL):
         k=_args[i+_offset]
         if k in defaultsUpdate:
            p['argdefs'][i]=defaultsUpdate[k]
      p['argdefs']=tuple(p['argdefs'])
   f2=types.FunctionType(**p)
   f2.__dict__=f.__dict__
   f2.__module__=f.__module__
   f2.__doc__=f.__doc__
   if isinstance(f, types.MethodType):
      f2=types.MethodType(f2, f.im_self, f.im_class)
   return f2

