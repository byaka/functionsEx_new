# -*- coding: utf-8 -*-

import shutil, tempfile, platform, os, ctypes, sys, errno, subprocess

from .types_ex import CaseInsensitiveDict


class TemporaryDirectory(object):
   """Context manager for tempfile.mkdtemp() so it's usable with "with" statement."""
   def __enter__(self):
      self.name = tempfile.mkdtemp()
      return self.name

   def __exit__(self, *err):
      try:
         shutil.rmtree(self.name)
      except OSError as e:
         # Reraise unless ENOENT: No such file or directory
         if e.errno!=errno.ENOENT: raise getErrorRaw()

def getFreeDiskSpace(dirname):
   """Return folder/drive free space in bytes."""
   # https://stackoverflow.com/a/2372171
   if platform.system().lower().startswith('win'):
      free_bytes = ctypes.c_ulonglong(0)
      ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
      return free_bytes.value
   else:
      st = os.statvfs(dirname)
      return st.f_bavail * st.f_frsize

def parseCLI(argv=None, actionCaseSensitive=True, argCaseSensitive=False, argDefVal=None, argShortConv=None, smartType=True):
   """
   Parse CLI arguments.

   Format:
      <action> -key=value -key -key
   """
   if argv is None:
      argv=sys.argv
   if not argCaseSensitive:
      if argDefVal:
         argDefVal=dict((k.lower(), v) for k,v in argDefVal.iteritems())
      if argShortConv:
         argShortConv=dict((k.lower(), v.lower()) for k,v in argShortConv.iteritems())
   args={} if argCaseSensitive else CaseInsensitiveDict({})
   action=None
   err=RuntimeError('Incorrect arguments format, please use next: action -k1 -k2=value --key3 --key4=value')
   for i, s in enumerate(argv):
      if not i: continue  #script
      if i==1:
         # action
         if s.startswith('-'): raise err
         action=s if actionCaseSensitive else s.lower()
      elif s.startswith('-'):
         # arguments
         if '=' in s:
            s, v=s.split('=', 1)
            if not v: v=None
         else: v=None
         if not argCaseSensitive: s=s.lower()
         if not s.startswith('--'):
            k=s[1:]
            if argShortConv and k in argShortConv: k=argShortConv[k]
         else: k=s[2:]
         if v is None and argDefVal and k in argDefVal: v=argDefVal[k]
         elif smartType and isString(v):
            if v.lower() in ('true',): v=True
            elif v.lower() in ('false',): v=False
            else: v=numEx(v)
         args[k]=v
      else: raise err
   return action, args

def runExternal(command, path=None, enc="utf-8", data=None):
   process=subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
   if isString(data):
      data=data.encode(enc)+'\n'
   out, err=process.communicate(input=data)
   if err:
      try: err=err.decode(enc)
      except UnicodeDecodeError: pass
   r=process.poll()
   if r:
      raise RuntimeError("Process %s has returned error-code %s: %s"%(' '.join(command), r, err))
   if out:
      try: out=out.decode(enc)
      except UnicodeDecodeError: pass
   return out

def size2human(num, suffix='B'):
   for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
      if abs(num)<1024.0:
         return "%3.1f%s%s"%(num, unit, suffix)
      num/=1024.0
   return "%.1f%s%s"%(num, 'Yi', suffix)

def pathList(path, fullPath=True, alsoFiles=True, alsoDirs=False, recursive=False, filter=None, isBlacklist=True, cb=None, _result=None, _prefix=None):
   #! переписать нормально
   #list sub-files and sub-dirs for specific path
   #! нужна версия, отдающая генератор на основе os.walk
   res=[] if _result is None else _result
   for f in os.listdir(path):
      fp=os.path.join(path, f)
      if filter:
         if isFunction(filter):
            if filter(fp, f) is False: continue
         elif isBlacklist and f in filter: continue
         elif not isBlacklist and f not in filter: continue
      #
      if isFunction(cb): fp, f=cb(fp, f)
      if not os.path.isfile(fp):
         if recursive:
            pathList(fp, fullPath=fullPath, alsoFiles=alsoFiles, alsoDirs=alsoDirs, recursive=True, filter=filter, cb=cb, _result=res, _prefix='' if fullPath else f+'/')
         if not alsoDirs: continue
      elif not alsoFiles: continue
      s=fp if fullPath else f
      if _prefix and isString(_prefix): s=_prefix+s
      res.append(s)
      # yield (fp if fullPath else f)
   return res

def folderClear(path, alsoFiles=True, alsoDirs=False, silent=True, filter=None, isBlacklist=True):
   #! синкануть код с апстримом
   for f in os.listdir(path):
      fp=os.path.join(path, f)
      try:
         if alsoFiles and os.path.isfile(fp):
            if isFunction(filter):
               if filter(fp, f, True) is False: continue
            elif isBlacklist and f in filter: continue
            elif not isBlacklist and f not in filter: continue
            os.unlink(fp)
         if alsoDirs and os.path.isdir(fp):
            if isFunction(filter):
               if filter(fp, f, False) is False: continue
            elif isBlacklist and f in filter: continue
            elif not isBlacklist and f not in filter: continue
            #! это удалит все внутренности папки, а нам нужно пройтись фильтром
            if os.path.islink(fp):
               os.unlink(fp)
            else:
               shutil.rmtree(fp)
      except Exception:
         if not silent: raise
         print getErrorInfo(fallback=True)

def zipGet(fName, filterByName=None, forceTry=False, password=None, silent=True):
   z=zipfile.ZipFile(fName, mode='r')
   isOk=True
   isSingle=False
   if filterByName is None:
      filterByName=z.namelist()
   elif isString(filterByName):
      filterByName=(filterByName,)
      isSingle=True
   res={}
   for n in filterByName:
      try: res[n]=z.read(n, password)
      except Exception, e:
         if not silent:
            try: z.close()
            except Exception: pass
            raise e
         print '! Cant read file "%s" from zip "%s": %s'%(n, fName, e)
         isOk=False
         if not forceTry: break
   try: z.close()
   except Exception, e:
      if not silent: raise
      print '! Cant close zip "%s": %s'%(fName, e)
      isOk=False
   if forceTry: return res.values()[0] if isSingle else res
   else:
      return (res.values()[0] if isSingle else res) if isOk else False

def isZipCompressionSupported(returnConst=False):
   # check, if compression supported by OS
   try:
      import zlib  # noqa
      return zipfile.ZIP_DEFLATED if returnConst else True
   except Exception:
      return zipfile.ZIP_STORED if returnConst else False

def zipWrite(fName, data, mode='w', forceCompression=True, silent=True):
   if not isDict(data):
      raise ValueError('data must be a dict with <name>:<content>')
   isOk=True
   if forceCompression and not isZipCompressionSupported():
      raise RuntimeError('Compression not supported by OS')
   z=zipfile.ZipFile(fName, mode=mode, compression=isZipCompressionSupported(returnConst=True))
   for n, d in data.iteritems():
      isRaw=False
      if isinstance(d, tuple) and len(d)==2 and d[0]==open: isRaw, d=True, d[1]
      elif not isString(d): d=repr(d)
      try:
         z.write(d, n) if isRaw else z.writestr(n, d)
      except Exception, e:
         if not silent:
            try: z.close()
            except Exception: pass
            raise e
         print '! Cant write file "%s" to zip "%s": %s'%(n, fName, e)
         isOk=False
         break
   try: z.close()
   except Exception, e:
      if not silent: raise
      print '! Cant close zip "%s": %s'%(fName, e)
      isOk=False
   return isOk

def fileGet(fName, mode='r', silent=True, buffer=-1):
   fName=fName.encode('cp1251')
   if not os.path.isfile(fName): return None
   try:
      with open(fName, mode, buffer) as f: s=f.read()
   except Exception, e:
      if not silent: raise
      print '! Cant get file "%s": %s'%(fName, e)
      s=None
   return s

def fileWrite(fName, text, mode='w', silent=False, buffer=-1):
   try:
      with open(fName, mode, buffer) as f: f.write(text)
   except Exception, e:
      if not silent: raise
      print '! Cant write file "%s"(%s): %s'%(fName, mode, e)

def fileAppend(fName, text, mode='a', silent=False, buffer=-1):
   return fileWrite(fName, text, mode=mode, silent=silent, buffer=buffer)

