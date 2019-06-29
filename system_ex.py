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
