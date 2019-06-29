# -*- coding: utf-8 -*-
import string, sys, traceback, zipfile, os, datetime, time, hmac, hashlib, math, random, re, copy, urllib2, urllib, types, decimal, inspect, subprocess, collections, _ctypes, ctypes, imp, shutil, itertools, functools, timeit, code, binascii, tempfile, errno, calendar, signal, atexit, platform  # noqa: E501, F401
try:
   import simplejson as json
except ImportError: import json
try:
   import cPickle as pickle
except ImportError: import pickle
try:
   import ujson
except ImportError: ujson=json
import os.path
from urlparse import *
from urllib import urlencode
from decimal import *

import difflib
from struct import Struct
from operator import xor
from itertools import izip, izip_longest, starmap, imap, chain, combinations, permutations  # noqa: E501, F401
from numbers import Number
from collections import Set, Mapping, deque, defaultdict, Counter, OrderedDict, namedtuple  # noqa: E501, F401

import smtplib, email
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email import encoders

# import typehack
# with typehack we can add methods to build-in classes, like in JS!
#? see code.google.com/p/typehack/source/browse/doc/readme.txt


mysqlEscaper=None  # библиотека pymysql блокирует патчинг через gevent, лучше импортирвоать ее на месте

noneStr=[None, '', "u'none'", '"none"', 'u"none"', "'none'", "u'None'", '"None"', 'u"None"', "'None'", 'none', 'None']
translitTable={u'а':'a', u'б':'b', u'в':'v', u'г':'g', u'д':'d', u'е':'e', u'ё':'e', u'ж':'zh', u'з':'z', u'и':'i', u'й':'y', u'к':'k', u'л':'l', u'м':'m', u'н':'n', u'о':'o', u'п':'p', u'р':'r', u'с':'s', u'т':'t', u'у':'u', u'ф':'f', u'х':'kh', u'ц':'ts', u'ч':'ch', u'ш':'sh', u'щ':'shch', u'ы':'y', u'ь':"'", u'ъ':"'", u'э':'e', u'ю':'yu', u'я':'ya'}  # noqa: E501
uLetters=['A','a','b','B', 'C','c', 'D','d', 'E','e','F','f','G','g','H','h','I','i','J','j','K','k','L','l','M','m','N','n','O','o','P','p','Q','q','U','u','R','r','S','s','T','t','V','v','W','w','X','x','Y','y','Z','z']  # noqa: E501
uLettersRu=[u'А', u'а', u'Б', u'б', u'В', u'в', u'Г', u'г', u'Д', u'д', u'Е', u'е', u'Ё', u'ё', u'Ж', u'ж', u'З', u'з', u'И', u'и', u'Й', u'й', u'К', u'к', u'Л', u'л', u'М', u'м', u'Н', u'н', u'О', u'о', u'П', u'п', u'Р', u'р', u'С', u'с', u'Т', u'т', u'У', u'у', u'Ф', u'ф', u'Х', u'х', u'Ц', u'ц', u'Ч', u'ч', u'Ш', u'ш', u'Щ', u'щ', u'Ъ', u'ъ', u'Ы', u'ы', u'Ь', u'ь', u'Э', u'э', u'Ю', u'ю', u'Я', u'я']  # noqa: E501
uPunctuations=[',','.',';',':','!','?']
uSpecials=['"',"'",'<','>','@','#','$','%','^','&','*','(',')','-','_','+','=','[',']','{','}','~','`','|']
uDash=['‐', '−', '‒', '–', '—', '―', '-']
uSpaces=[' ']
uDigits=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ucodes={'\\u0430': 'а','\\u0410': 'А','\\u0431': 'б','\\u0411': 'Б','\\u0432': 'в','\\u0412': 'В','\\u0433': 'г','\\u0413': 'Г','\\u0434': 'д','\\u0414': 'Д','\\u0435': 'е','\\u0415': 'Е','\\u0451': 'ё','\\u0401': 'Ё','\\u0436': 'ж','\\u0416': 'Ж','\\u0437': 'з','\\u0417': 'З','\\u0438': 'и','\\u0418': 'И','\\u0439': 'й','\\u0419': 'Й','\\u043a': 'к','\\u041a': 'К','\\u043b': 'л','\\u041b': 'Л','\\u043c': 'м','\\u041c': 'М','\\u043d': 'н','\\u041d': 'Н','\\u043e': 'о','\\u041e': 'О','\\u043f': 'п','\\u041f': 'П','\\u0440': 'р','\\u0420': 'Р','\\u0441': 'с','\\u0421': 'С','\\u0442': 'т','\\u0422': 'Т','\\u0443': 'у','\\u0423': 'У','\\u0444': 'ф','\\u0424': 'Ф','\\u0445': 'х','\\u0425': 'Х','\\u0446': 'ц','\\u0426': 'Ц','\\u0447': 'ч','\\u0427': 'Ч','\\u0448': 'ш','\\u0428': 'Ш','\\u0449': 'щ','\\u0429': 'Щ','\\u044a': 'ъ','\\u042a': 'Ъ','\\u044b': 'ы','\\u042b': 'Ы','\\u044c': 'ь','\\u042c': 'Ь','\\u044d': 'э','\\u042d': 'Э','\\u044e': 'ю','\\u042e': 'Ю','\\u044f': 'я','\\u042f': 'Я'}  # noqa: E501
usymbols=uLetters+uPunctuations+uSpecials
####
uCodes=ucodes
uSymbols=usymbols

allColors=['alicemblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgray','darkgreen','darkkhaki','darkmagenta','darkolivegreen','darkorange','darkochid','darkred','darksalmon','darkseagreen','darkslateblue','darkslategray','darkturquoise','darkviolet','deeppink','deepskyblue','dimgray','dodgerblue','firebrick','floralwhite','forestgreen','fushsia','gainsboro','ghostwhite','gold','goldenrod','gray','green','greenyellow','honeydew','hotpink','indiandred','indigo','ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon','ligtblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgreen','lightgrey','lightpink','lightsalmon','lightseagreen','lightscyblue','lightslategray','lightsteelblue','lightyellow','lime','limegreen','linen','magenta','mahogany','maroon','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise','medium','midnightblue','mintcream','mistyrose','moccasin','navajowhite','navy','oldlace','olive','olivedrab','orange','orengered','orchid','palegoldenrod','palegreen','paleturquose','palevioletred','papayawhop','peachpuff','peru','pink','plum','powderblue','purple','red','rosybrown','royalblue','saddlebrown','salmon','sandybrown','seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','snow','springgreen','steelblue','tan','teal','thistle','tomato','turquose','violet','wheat','white','whitesmoke','yellow','yellowgreen']
# uCodes={}
for s in uSymbols:
   c=str(hex(ord(s)))[2:]
   while len(c)<4: c='0'+c
   c='\\u'+c
   uCodes[c]=s

_deprecatedWarningShowed={}

def deprecated(f):
   """
   Decorator for deprecated functions. Shows detailed message and writes to log (but only one time per call).
   """
   def tmp(*args, **kwargs):
      try:
         module, line, name, _=traceback.extract_stack()[-2]
         msg='>> DEPRECATED function "%s:%s()" called from %s:%s <<'%(getScriptName(f=f.func_code.co_filename, withExt=True), f.__name__, module, line)
         if msg not in _deprecatedWarningShowed:
            _deprecatedWarningShowed[msg]=None
            try:
               p='%s/functionsex_deprecatedCalls.txt'%getScriptPath(f=__file__)
               m='%s:%s <- %s:%s\n'%(f.func_code.co_filename, f.__name__, module, name)
               fileAppend(p, m)
            except Exception, e:
               print '! Cant log deprecated call to "%s": %s'%(p, e)
            if consoleIsTerminal():
               msg=consoleColor.bold+consoleColor.warning+msg+consoleColor.end
            print msg
      except Exception, e:
         print '! You call deprecated function, but decorator failed:', e
      return f(*args, **kwargs)
   return tmp
#===================================

#===================================
def getHtml(url, tryEncode=True, followRedirect=True):
   class NoRedirection(urllib2.HTTPErrorProcessor):
      def http_response(self, request, response):
         code, msg, hdrs = response.code, response.msg, response.info()
         return response
      https_response = http_response
   if followRedirect:
      opener=urllib2.build_opener()
   else:
      opener=urllib2.build_opener(NoRedirection)
   try:
      page=opener.open(url)
      pageHtml=page.read()
   except:
      opener.close()
      return None
   if tryEncode:
      try:
         charset = re.findall('charset=(.*?)$', page.info()['Content-Type'])[0].lower()
         if charset != 'utf-8': pageHtml = pageHtml.decode(charset) #решаем проблему с кодировками
      except: pass
      pageHtml = strUniEncode(pageHtml)
   opener.close()
   return pageHtml

def getHtml2(url, followRedirect=True, headers={}, proxie=None, type='get', timeout=15, returnOnlyData=True, checkHtml=False, logHeadersBefore=False, auth=False, base64Auth=False, data={}, tryForceEncoding=False, forceEncoding=False, cookies=False, silent=False, raiseErrors=False):  # noqa
   # print url, data
   import requests
   # from requests.auth import HTTPBasicAuth
   # from requests.auth import HTTPDigestAuth
   try: #работаем с кириллическими доменами
      if re.findall('[а-яА-Я]',url) != []:
         urlArr=urlparse(url.decode('utf-8'))
         import idna
         urlDomain=idna.encode(urlArr.netloc)#.decode('utf-8')
         url=url.replace(urlArr.netloc.encode('utf-8'),urlDomain)
   except: pass  # noqa
   if proxie and len(proxie):
      if isArray(proxie):
         proxie={'http':'http://%s:%s@%s'%(arrGet(proxie,1) or '', arrGet(proxie,2) or '', proxie[0])}
      else:
         proxie={'http':'http://%s'%(proxie)}
   if base64Auth:
      import base64
      base64string = base64.encodestring('%s:%s' % (base64Auth[0], base64Auth[1]))[:-1]
      headers={"Authorization":"Basic %s" % base64string}
   if checkHtml:  #! Опять женя какуюто херню наворотил, поправить на рекурсивный вызов
      r=requests.head(url, allow_redirects=followRedirect, headers=headers, timeout=timeout, proxies=proxie)
      # if r.status_code != 200:
      #    return magicDict({'status':r.status_code})
      try: contentType=r.headers['content-type'].split(';')[0]
      except: contentType='text/html'  # noqa
      if contentType!='text/html':
         return magicDict({'status':r.status_code, 'contentType':contentType})
   if auth:
      if isArray(auth):
         auth=(auth[0], auth[1])
      else:
         auth=('BuberStats','76d3ca8d538bc44bd5a5aa0c316ff428')
   else: auth=None
   # select request's method
   args={'allow_redirects':followRedirect, 'headers':headers, 'timeout':timeout, 'proxies':proxie, 'stream':logHeadersBefore, 'auth':auth, 'cookies':cookies}
   if type in ('get', 'post', 'head'):
      m=getattr(requests, type)
      if type=='post': args['data']=data
   else:
      raise NotImplementedError('! GetHtml2 not provide "%s" request method'%type)
   # send request
   try:
      # r=requests.get(url, allow_redirects=followRedirect, headers=headers, timeout=timeout, proxies=proxie, stream=logHeadersBefore, auth=auth, cookies=cookies)
      # r=requests.post(url, data=data, allow_redirects=followRedirect, headers=headers, timeout=timeout, proxies=proxie, stream=logHeadersBefore, auth=auth, cookies=cookies)
      r=m(url, **args)
      if logHeadersBefore: print_r(dict(r.headers))
   except Exception, e:
      if not silent:
         print '!!! GetHtml2 error:', e
      if raiseErrors: raise e
      return None if returnOnlyData else magicDict({'data':None, 'status':e, 'url':url, 'response':None})
   try:
      contentType=r.headers['content-type'].split(';')[0]
   except: contentType=None  # noqa

   text=r.text
   if forceEncoding or (tryForceEncoding and (r.encoding=='ISO-8859-1' or not r.encoding)):
      #ISO-8859-1 проставляется, если сервер не отдал кодировку
      try:
         if r.apparent_encoding:
            enc=r.apparent_encoding
         else:  #ищем кодировку в теле ответа
            enc=regExp_htmlEncoding.search(text).group(1)
         r.encoding=enc
         text=r.text  #перекодируем ответ в правильной кодировке
      except: pass  # noqa
   if returnOnlyData: return text
   else:
      headersArr=dict(r.headers)
      try: cookieArr=dict(r.cookies)
      except Exception, e:
         print '! GetHtml2 cant extract cookies: %s. Headers: %s'%(e, headersArr)
         cookieArr={}
      enc=r.encoding.lower() if r.encoding else None
      enc2=r.apparent_encoding.lower() if r.apparent_encoding else None
      return magicDict({'data':text, 'encoding':enc, 'encoding2':enc2, 'status':r.status_code, 'contentType':contentType, 'response':r, 'url':r.url, 'cookies':cookieArr, 'headers':headersArr})
#===================================
#===================================
def everyWithEvery(arr, func, onlyIndex=False):
   for i1 in xrange(len(arr)):
      for i2 in xrange(len(arr)):
         if i1==i2: continue
         s=func(i1 if onlyIndex else arr[i1], i2 if onlyIndex else arr[i2])
         if s is False: return False
   return True
EveryWithEvery=everyWithEvery #для обратной совместимости

def intINstr(data, specialAs=None):
   # проверяет строку, чего в ней больше - букв или цифр
   try: data=data.decode('utf-8')
   except: pass
   data=data.replace(' ', '')
   if specialAs is None:
      data=regExp_specialSymbols0.sub('',data)
   elif isString(specialAs):
      data=regExp_specialSymbols0.sub('a',data)
   else:
      data=regExp_specialSymbols0.sub('0',data)
   if not len(data): return None
   data=regExp_lettersReplace0.sub('a', data)
   try:
      float(data)
      return 'int'
   except: pass
   s=sorted(data, key=lambda i: i in uDigits)
   i=len(s)/2
   if not(len(s)%2) and i<len(s)-1: i=i+1
   if s[i] in uDigits: r='iws'
   elif s[-1] in uDigits: r='swi'
   else: r='str'
   return r

#===================================
#===================================

def stopwatchMark(name='default', clear=False, wait=False, inMS=True):
   if name not in stopwatch['values'] or clear: stopwatch['values'][name]=[]
   stopwatch['values'][name].append(getms(inMS))
   if wait: stopwatch['values'][name].append(None)

def stopwatchShow(name='default', save=True, wait=False, andPrint='%s = %s', inMS=True):
   s=getms(inMS)
   vals=stopwatch['values'][name]
   v=0.0
   for i in xrange(1, len(vals)):
      if vals[i] is None or vals[i-1] is None: continue
      v+=vals[i]-vals[i-1]
   v+=s-vals[-1] if vals[-1] is not None else 0
   # print v
   if save: stopwatchMark(name=name, wait=wait, inMS=inMS)
   if andPrint and isString(andPrint): print andPrint%(name, v)
   return v

def stopwatchShowAll(includeDefault=False, andPrint='%s = %s', printSorted=True):
   v={}
   for k in stopwatch['values'].iterkeys():
      if not includeDefault and k=='default': continue
      v[k]=stopwatchShow(name=k, save=False, andPrint=False)
   stopwatch['values']={'default':[]}
   if isString(andPrint):
      for k in sorted(v.keys(), key=lambda k: v[k], reverse=True):
         print andPrint%(k, v[k])
   return v

global stopwatch
stopwatch=magicDict({
   'mark':stopwatchMark,
   'values':{'default':[]},
   'show':stopwatchShow,
   'showAll':stopwatchShowAll
})
#===================================
def isGenerator(var):
   return isinstance(var, types.GeneratorType)
isGen=isGenerator

def isFunction(var):
   return callable(var)  #respecting bugbear rule
   # return hasattr(var, '__call__')  #respecting bugbear rule
isFunc=isFunction

def isIterable(var):
   return isinstance(var, collections.Iterable)
isIter=isIterable

def isClass(var):
   return isinstance(var, (type, types.ClassType, types.TypeType))

def isInstance(var):
   #? work only with old-styled classes
   return isinstance(var, types.InstanceType)

def isModule(var):
   return isinstance(var, types.ModuleType)

def isModuleBuiltin(var):
   return imp.is_builtin(var)
   # imp.find_module(var)==imp.C_BUILTIN
   # return isModule(var) and getattr(var, '__name__', '') in sys.builtin_module_names

def isString(var):
   return isinstance(var, (str, unicode))
isStr=isString

def isBool(var):
   return isinstance(var, bool)

def isNum(var):
   return (var is not True) and (var is not False) and isinstance(var, (int, float, long, complex, decimal.Decimal))

def isFloat(var):
   return isinstance(var, (float, decimal.Decimal))

def isInt(var):
   return (var is not True) and (var is not False) and isinstance(var, int)

def isList(var):
   return isinstance(var, list)
isArray=isList

def isTuple(var):
   return isinstance(var, tuple)

def isDict(var):
   return isinstance(var, dict)
isObject=isDict

def isSet(var):
   return isinstance(var, set)

getObjectById=findObjectById

def json2generator(data, arrayKey=None):
   """
   Функция конвертирует переданный json в генератор. Это позволяет избежать утечки памяти на огромных обьемах данных. Может выдать генератор только для массива (неважно какой вложенности и сложности). arrayKey должен указывать на массив, может быть цепочкой (key1.key2)
   """
   from ijson import common
   from cStringIO import StringIO
   #? yajl2 беккенд работает значительно быстрее, но на первый сервак так и не удалось его установить, пишет "Yajl shared object cannot be found"
   try: import ijson.backends.yajl2_cffi as ijson
   except ImportError:
      try: from ijson.backends import yajl2 as ijson
      except ImportError:
         try: from ijson.backends import yajl as ijson
         except ImportError: from ijson.backends import python as ijson
   try: f=StringIO(data)
   except Exception: f=StringIO(data.encode('utf-8'))
   def _fixJSON(event):
      # функция исправляет "фичу" декодинга, Которая пытается все цифровые типы привести к decimal()
      if event[1]=='number':
         return (event[0], event[1], float(event[2]) if math.modf(event[2])[0] else int(event[2]))
      else: return event
   events=imap(_fixJSON, ijson.parse(f))
   g=common.items(events, (arrayKey+'.item' if arrayKey else 'item'))
   # g=ijson.items(f, (arrayKey+'.item' if arrayKey else 'item'))
   return g

def reprEx(obj, indent=None, toUtf8=True, sortKeys=True):
   def _fixJSON(o):
      if isinstance(o, decimal.Decimal): return str(o)  #fix Decimal conversion
      if isinstance(o, (datetime.datetime, datetime.date, datetime.time)): return o.isoformat() #fix DateTime conversion
   try:
      s=json.dumps(obj, indent=indent, separators=(',',':'), ensure_ascii=False, sort_keys=sortKeys, default=_fixJSON)
   except Exception:
      try: s=json.dumps(obj, indent=indent, separators=(',',':'), ensure_ascii=True, sort_keys=sortKeys, default=_fixJSON)
      except Exception as e:
         print '!!! reprEx', e
         return None
   if toUtf8:
      try: s=s.encode('utf-8')
      except Exception: pass
   return s

def numEx(val, forceFloat=False):
   #convert string to integer. if fail, convert to float. if fail return original
   if isString(val): val=val.strip()
   if forceFloat:
      try: return float(val)
      except Exception: return val
   try: return int(val)
   except Exception:
      try: return float(val)
      except Exception: return val
intEx=numEx

def prepDataMYSQL(data):
   """
   Функция для пред-обработки данных перед записью в базу
   """
   global mysqlEscaper
   if mysqlEscaper is None:
      try:
         import pymysql as mysqlEscaper
      except ImportError:
         import MySQLdb as mysqlEscaper
   if not isString(data):
      data=reprEx(data)
   data=mysqlEscaper.escape_string(data)
   try:data=data.decode('utf-8')
   except Exception: pass
   return data

def uLower(s):
   try: s=s.decode('utf-8').lower().encode('utf-8')
   except Exception: s=s.lower()
   return s

def uUpper(s):
   try: s=s.decode('utf-8').upper().encode('utf-8')
   except Exception: s=s.upper()
   return s

def strEx(val):
   if isString(val): return val
   try: return str(val)
   except Exception:
      try: return reprEx(val)
      except Exception: return val

@deprecated
def str2dict(text, sep1='=', sep2=' '):
   #create dict{key:val} from string"key(sep1)val(sep2)"
   tArr1=text.split(sep2)
   tArr2={}
   for s in tArr1:
      if not s: continue
      s1=strGet(s, '', sep1, default=s)
      s2=strGet(s, sep1, default='')
      if s1: tArr2[s1]=s2
   return tArr2

def getms(inMS=False):
   #return time and date in miliseconds(UNIXTIME) or seconds
   if inMS: return round(time.time()*1000.0, 0)
   else: return int(time.time())

def dateComp(date, datewith=None, f='%d/%m/%Y %H:%M:%S'):
   #compare two dates in specific format
   if datewith is None:
      date1=datetime.datetime.now().strftime(f)
      date2=date
   else:
      date1=date
      date2=datewith
   date1=timeNum(date1, f) if not isNum(date1) else date1
   date2=timeNum(date2, f) if not isNum(date2) else date2
   dd=date1-date2
   return dd
dateDiff=dateComp

def dateAddMonth(date=None, n=1):
   date=date or datetime.datetime.now()
   new_year=date.year
   new_month=date.month+n
   if new_month>12:
      new_year+=1
      new_month-=12
   last_day_of_month=calendar.monthrange(new_year, new_month)[1]
   new_day=min(date.day, last_day_of_month)
   return date.replace(year=new_year, month=new_month, day=new_day)

def dateIncress(wait, f='%d.%m.%Y'):
   #incress date by given seconds
   if not wait: return None
   s=wait*3600.0*24.0
   s=datetime.datetime.now()+datetime.timedelta(seconds=s)
   return s.strftime(f)

# import code, readline, atexit, os

# class HistoryConsole(code.InteractiveConsole):
#    def __init__(self, locals=None, filename="<console>", histfile=os.path.expanduser("~/.console-history")):
#       code.InteractiveConsole.__init__(self, locals, filename)
#       self.init_history(histfile)

#    def init_history(self, histfile):
#       readline.parse_and_bind("tab: complete")
#       if hasattr(readline, "read_history_file"):
#          try:
#             readline.read_history_file(histfile)
#          except IOError:
#             pass
#          atexit.register(self.save_history, histfile)

#    def save_history(self, histfile):
#       readline.set_history_length(1000)
#       readline.write_history_file(histfile)

global consoleColor
consoleColor=MagicDict({
   # predefined colors
   'fail':'\x1b[91m',
   'ok':'\x1b[92m',
   'warning':'\x1b[93m',
   'okblue':'\x1b[94m',
   'header':'\x1b[95m',
   # colors
   'black':'\x1b[30m',
   'red':'\x1b[31m',
   'green':'\x1b[32m',
   'yellow':'\x1b[33m',
   'blue':'\x1b[34m',
   'magenta':'\x1b[35m',
   'cyan':'\x1b[36m',
   'white':'\x1b[37m',
   # background colors
   'bgblack':'\x1b[40m',
   'bgred':'\x1b[41m',
   'bggreen':'\x1b[42m',
   'bgyellow':'\x1b[43m',
   'bgblue':'\x1b[44m',
   'bgmagenta':'\x1b[45m',
   'bgcyan':'\x1b[46m',
   'bgwhite':'\x1b[47m',
   # specials
   'light':'\x1b[2m',
   'bold':'\x1b[1m',
   'inverse':'\x1b[7m',
   'underline':'\x1b[4m',
   'clearLast':'\x1b[F\x1b[K',
   'end':'\x1b[0m'
})

def consoleInteract(scope=None, msg=None):
   if not consoleIsTerminal():
      raise RuntimeError('Must be TTY')
   scope=(scope or {}).copy()
   def tFunc():
      raise SystemExit
   scope['exit']=tFunc
   try:
      if msg is None:
         # w=consoleSize()[0]
         msg=''
         # msg+='#'*w
         msg+='-'*48
         msg+='\n'+'Interactive session, for return back use `exit()`' #.center(w, '-')
         # msg+='#'*w
         msg=consoleColor.magenta+consoleColor.bold+msg+consoleColor.end
      code.interact(banner=msg, local=scope)
   except SystemExit: pass

def consoleSize():
   if not sys.stdout.isatty():
      return INFINITY, INFINITY
   import fcntl, termios, struct
   h, w, hp, wp=struct.unpack('HHHH', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))
   return w, h

def consoleClear():
   #clear console outpur (linux,windows)
   if sys.platform=='win32': os.system('cls')
   else: os.system('clear')

def consoleIsTerminal():
   return sys.stdout.isatty()

def consoleRepair():
   # https://stackoverflow.com/a/24780259/5360266
   os.system('stty sane')

global console
console=magicDict({
   'interact':consoleInteract,
   'clear':consoleClear,
   'inTerm':consoleIsTerminal,
   'color':consoleColor,
   'repair':consoleRepair,
   'size':consoleSize,
   'width':lambda: consoleSize()[0],
   'height':lambda: consoleSize()[1],
})

@deprecated
def cmd(command, path=None, enc="utf-8"):
   return runExternal(command, path=path, enc=enc, data=None)

def clearTypography(data):
   tMap={
      u' ':' ',
      u'«':'"',
      u'»':'"',
      ' ':' ',
      '«':'"',
      '»':'"',
      u'\u0301':''  #ударение над буквой
   }
   for k, v in tMap.iteritems():
      try:
         if k in data:
            data=data.replace(k, v)
      except: pass  # noqa
   return data

def strIsUpBegin(str):
   # проверяет, является ли первая найденная буква слова заглавной. игнорирует остальные символы в начале слова
   return bool(sum([int(s.isupper()) for s in str if s in uLetters]))

def strGet(text, pref='', suf='', index=0, default='', returnOnlyStr=True, caseSensitive=False):
   # return pattern by format pref+pattenr+suf
   if not text:
      if returnOnlyStr: return default
      else: return -1, -1, default
   if caseSensitive:
      text1=text.lower()
      pref=pref.lower()
      suf=suf.lower()
   else: text1=text
   if pref:
      i1=text1.find(pref,index)
   else:
      i1=index
   if i1==-1:
      if returnOnlyStr: return default
      else: return -1, -1, default
   if suf:
      i2=text1.find(suf,i1+len(pref))
   else:
      i2=len(text1)
   if i2==-1:
      if returnOnlyStr: return default
      else: return i1, -1, default
   s=text[i1+len(pref):i2]
   if returnOnlyStr: return s
   else:
      return i1+len(pref), i2, s
###str.get=strGet

def decode_utf8(text):
   """ Returns the given string as a unicode string (if possible). """
   if isinstance(text, str):
      for encoding in (("utf-8",), ("windows-1252",), ("utf-8", "ignore")):
         try:
            return text.decode(*encoding)
         except: pass
      return text
   return unicode(text)

def encode_utf8(text):
   """ Returns the given string as a Python byte string (if possible). """
   if isinstance(text, unicode):
      try:
         return text.encode("utf-8")
      except:
         return text
   return str(text)

def strUniDecode(text, alsoU=True):
   #decode unicode's things for russian,use map
   try:
      text=text.encode('utf-8').replace('°', ' ')
   except: pass
   if alsoU:
      try:
         text=str(text).replace('\\u0075', 'u').replace('\\u0055', 'U')
      except: pass
   try:
      for f, to in ucodes.iteritems():
         text=str(text).replace(f, to)
   except: pass
   return text
###str.uniDecode=strUniDecode

def strUniEncode(text, alsoU=True):
   #encode unicode's things for russian,use map
   if alsoU:
      try:
         text=str(text).replace('u', '\\u0075').replace('U', '\\u0055')
      except: pass
   try:
      for to,f in ucodes.iteritems():
         text=text.replace(f, to)
   except: pass
   return text
###str.uniEncode=strUniEncode

def print_r(arr, pref=''):
   try:
      from decimal import Decimal
      if isDict(arr):
         for k in arr:
            if isDict(arr[k]):
               for kk in arr[k]:
                  if isinstance(arr[k][kk], (datetime.date, datetime.datetime)): arr[k][kk]=str(arr[k][kk])
                  if isinstance(arr[k][kk], (int, float, long, Decimal)): arr[k][kk]=str(arr[k][kk])
            else:
               if isinstance(arr[k], (datetime.date, datetime.datetime)): arr[k]=str(arr[k])
               if isinstance(arr[k], (int, float, long, Decimal)): arr[k]=str(arr[k])
      print pref, strUniDecode(reprEx(arr,2))
   except:
      print 'ERROR in print_r'

def print_rd(arr,pref=''):
   print_r(arr, pref)
   sys.exit(0)

def printTable(table):
   col_width = [max(len(x) for x in col) for col in zip(*table)]
   for i, line in enumerate(table):
      s="| " + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |"
      if not i: print '-'*len(s)
      print s
      if not i or i==len(table)-1: print '-'*len(s)

def arrFind(arr, v, default=-1):
   """аналог str.find() для массивов"""
   if isGenerator(arr): arr=list(arr)
   try:
      return arr.index(v)
   except ValueError: return default

def arrEjectionClean3(arr, delicacy=1.03, returnEjections=False, returnIndex=False, sortKey=None, allowSort=True):
   """чистит цифровую выборку от выбросов, используя робастный подход по соседним значениям"""
   #! этот метод считает выбросом значение, отличающееся от предыдущего более чем на (предыдущее * <delicacy>). такой подход применим только в узком круге задач. Метод нужно оставить, но не использовать его в качестве дефолтного.
   arrMap=range(len(arr))
   if(allowSort):
      # в нормальных условия метод работает корректно только для отсортированных массивов
      arrMap=sorted(arrMap, key=sortKey, reverse=False)
   out=[]
   last=None
   delicacy=float(delicacy)
   for i in arrMap:
      e=arr[i]
      # if last is not None: print '..', last, e, e-last, delicacy*last
      if last is None and e==0:
         if not returnEjections: out.append(i)
         continue
      elif last is not None and (e-last>delicacy*last):
         if returnEjections: out.append(i)
         continue
      if not returnEjections: out.append(i)
      last=e
   if returnIndex: out=[i for i in xrange(len(arr)) if i in out]
   else: out=[arr[i] for i in xrange(len(arr)) if i in out]
   return out

def arrEjectionClean(arr, allowSort=True, sortKey=None, robustMultiplier=0.9, returnEjections=False):
   """чистит цифровую выборку от выбросов, используя дефолтный подход"""
   print '='*71, '\n', '!! used DEFAULT robust method, that working only with specific cases !!', '\n', '='*71
   return arrEjectionClean3(arr=arr, allowSort=allowSort, returnEjections=returnEjections, sortKey=sortKey, delicacy=robustMultiplier, returnIndex=False)

def arrCreateIndexMap(arr, sort=True, key=None, reverse=False):
   """ Create indexed and sorted (optionally) map. Also supports dicts. """
   if sort:
      if isFunction(key):
         def tFunc(i):
            return key(arr[i])
      else:
         def tFunc(i):
            return arr[i]
      arrMap=arr if isDict(arr) else range(len(arr))
      arrMap=sorted(arrMap, key=tFunc, reverse=reverse)
   elif isFunction(key):
      arrMap=arr if isDict(arr) else xrange(len(arr))
      arrMap=[key(arr[i]) for i in arrMap]
   else:
      arrMap=arr.keys() if isDict(arr) else range(len(arr))
   return arrMap

def arrMedian(arr, arrMap=None, key=None):
   """
   Find median. Also supports dicts.

   :Example:

   >>> arrMedian([1, 5, 6, 7, 9, 12, 15, 19, 20, 2, 3, 30, 35])
   9.0
   >>> arrMedian([1, 1, 3, 5, 7, 9, 10, 14, 18])
   7.0
   >>> arrMedian([0, 1, 2, 3, 4, 5, 6, 7, 8])
   4.0
   """
   if not len(arr): return 0
   elif len(arr)==1:
      if isDict(arr):
         return key(arr.values()[0]) if isFunction(key) else arr.values()[0]
      else:
         return key(arr[0]) if isFunction(key) else arr[0]
   if not arrMap:
      arrMap=arrCreateIndexMap(arr, key=key)
   if len(arrMap)%2:
      i1=arrMap[len(arrMap)/2]
      median=key(arr[i1]) if isFunction(key) else arr[i1]
   else:
      i1=arrMap[(len(arrMap)-1)/2]
      i2=arrMap[(len(arrMap)-1)/2+1]
      median=(key(arr[i1])+key(arr[i2]))/2.0 if isFunction(key) else (arr[i1]+arr[i2])/2.0
   return median

def arrQuartiles(arr, arrMap=None, method=1, key=None, median=None):
   """
   Find quartiles. Also supports dicts.
   This function know about this quartile-methods:
      1. Method by Moore and McCabe's, also used in TI-85 calculator.
      2. Classical method, also known as "Tukey's hinges". In common cases it use values from original set, not create new.
      3. Mean between  method[1] and method[2].

   :param int method: Set method for find quartiles.

   :Example:

   >>> arrQuartiles([1, 5, 6, 7, 9, 12, 15, 19, 20], method=1)
   (5.5, 9, 17.0)
   >>> arrQuartiles([1, 5, 6, 7, 9, 12, 15, 19, 20], method=2)
   (6, 9, 15)
   >>> arrQuartiles([1, 5, 6, 7, 9, 12, 15, 19, 20], method=3)
   (5.75, 9, 16.0)
   >>> arrQuartiles([1, 1, 3, 5, 7, 9, 10, 14, 18], method=1)
   (2.0, 7, 12.0)
   >>> arrQuartiles([1, 1, 3, 5, 7, 9, 10, 14, 18], method=2)
   (3, 7, 10)
   >>> arrQuartiles([1, 1, 3, 5, 7, 9, 10, 14, 18], method=3)
   (2.5, 7, 11.0)
   """
   if method not in (1, 2, 3):
      raise ValueError('Unknown method: %s'%method)
   if not arr: return (0, 0, 0)
   elif len(arr)==1:
      #? что лучше отдавать
      if isDict(arr):
         r=key(arr.values()[0]) if isFunction(key) else arr.values()[0]
      else:
         r=key(arr[0]) if isFunction(key) else arr[0]
      return (0, r, r+1)
   if not arrMap:
      arrMap=arrCreateIndexMap(arr, key=key)
   if median is None:
      median=arrMedian(arr, arrMap, key=key)
   def getHalve(isLow=True, includeM=False):
      tArr=[]
      for i in arrMap:
         v=key(arr[i]) if isFunction(key) else arr[i]
         if isLow and (v<=median if includeM else v<median): tArr.append(v)
         elif not isLow and (v>=median if includeM else v>median): tArr.append(v)
      tArrMap=range(len(tArr))
      return tArr, tArrMap
   if method in (1, 2):  #methods "Moore and McCabe's" and "Tukey's hinges"
      tHalveL, tHalveL_arrMap=getHalve(True, method==2)
      tHalveH, tHalveH_arrMap=getHalve(False, method==2)
      qL=arrMedian(tHalveL, tHalveL_arrMap)
      qH=arrMedian(tHalveH, tHalveH_arrMap)
   elif method==3:  #mean between  method[1] and method[2]
      tHalveL1, tHalveL1_arrMap=getHalve(True, False)
      tHalveH1, tHalveH1_arrMap=getHalve(False, False)
      qL1=arrMedian(tHalveL1, tHalveL1_arrMap)
      qH1=arrMedian(tHalveH1, tHalveH1_arrMap)
      tHalveL2, tHalveL2_arrMap=getHalve(True, True)
      tHalveH2, tHalveH2_arrMap=getHalve(False, True)
      qL2=arrMedian(tHalveL2, tHalveL2_arrMap)
      qH2=arrMedian(tHalveH2, tHalveH2_arrMap)
      qL=(qL1+qL2)/2.0
      qH=(qH1+qH2)/2.0
   return qL, median, qH

def arrTrimean(arr, arrMap=None, key=None, median=None):
   """
   Find Tukey's trimean. Also supports dicts.

   :Example:

   >>> arrTrimean([1, 5, 6, 7, 9, 12, 15, 19, 20])
   9.75
   >>> arrTrimean([1, 1, 3, 5, 7, 9, 10, 14, 18])
   6.75
   >>> arrTrimean([0, 1, 2, 3, 4, 5, 6, 7, 8])
   4.0
   """
   if not len(arr): return 0
   elif len(arr)==1:
      if isDict(arr):
         return key(arr.values()[0]) if isFunction(key) else arr.values()[0]
      else:
         return key(arr[0]) if isFunction(key) else arr[0]
   if not arrMap:
      arrMap=arrCreateIndexMap(arr, key=key)
   q1, m, q3=arrQuartiles(arr, arrMap, method=2, key=key, median=median)
   trimean=(q1+2.0*m+q3)/4.0
   return trimean

def arrMode(arr, rank=0, key=None, returnIndex=False):
   """ Find mode of specific rank. Also supports dicts. """
   if not len(arr):
      return -1 if returnIndex else 0
   elif len(arr)==1:
      if isDict(arr):
         return arr.keys()[0] if returnIndex else (key(arr.values()[0]) if isFunction(key) else arr.values()[0])
      else:
         return 0 if returnIndex else (key(arr[0]) if isFunction(key) else arr[0])
   arrMap={}
   for i, v in (arr.iteritems() if isDict(arr) else enumerate(arr)):
      if isFunction(key): v=key(v)
      if v not in arrMap: arrMap[v]=[]
      arrMap[v].append(i)
   kMap=arrMap.keys()
   if rank>=len(kMap):
      return [] if returnIndex else None
   kMap=sorted(kMap, key=lambda s: len(arrMap[s]), reverse=True)
   k=kMap[rank]
   return arrMap[k] if returnIndex else k

def arrEjectionClean2(arr, delicacy=0.51, returnEjections=False, returnIndex=False, useTrimean=False):
   """чистит цифровую выборку от выбросов, используя робастный подход по медиане или тримеане"""
   out=[]
   if useTrimean: median=arrTrimean(arr)
   else: median=arrMedian(arr)
   medianM=abs(float(delicacy)*median)
   for i in range(len(arr)):
      if abs(median-arr[i])>medianM:
         if not returnEjections: continue
         else:
            out.append(i if returnIndex else arr[i])
            continue
      if not returnEjections: out.append(i if returnIndex else arr[i])
   return out

def arrAverage(arr, robust=False):
   if robust: arr=arrEjectionClean2(arr)
   if not len(arr): return 0  #защита от деления на ноль
   return sum(arr)/float(len(arr))

def arrMax(arr, key=None, returnIndex=False):
   """позволяет использовать key при поиске максимума"""
   #! добавить поддержку работы со словарем как arrMedian
   if not len(arr):
      return -1 if returnIndex else None  #minimum possible number, so any other bigger
   elif len(arr)==1:
      return 0 if returnIndex else (key(arr[0]) if isFunction(key) else arr[0])
   else:
      if isFunction(key):
         arr=(key(s) for s in arr)
      if returnIndex:
         return arrFind(arr, max(arr), -1)
      else:
         return max(arr)

def arrMin(arr, key=None, returnIndex=False):
   """позволяет использовать key при поиске минимума"""
   if not len(arr):
      return -1 if returnIndex else None  #maximum possible number, so any other smaller
   elif len(arr)==1:
      return 0 if returnIndex else (key(arr[0]) if isFunction(key) else arr[0])
   else:
      if isFunction(key):
         arr=(key(s) for s in arr)
      if returnIndex:
         return arrFind(arr, min(arr), -1)
      else:
         return min(arr)

@deprecated
def arrUnique(arr, key=None):
   #unique elements of array
   if not(arr): return []
   tArr1=arr
   if isFunction(key):
      tArr1=(key(s) for s in tArr1)
   tArr1=set(tArr1)
   tArr1=list(tArr1)
   return tArr1
###list.unique=arrUnique

def setsSymDifference(*objs):
   # calc symmetric-difference between MULTIPLE sets
   # this equivalent for `(o1|o2|o3).difference((o1&o2),(o2&o3), (o1&o3))`
   r=objs[0].union(*objs[1:])
   r.difference_update(*(o1&o2 for o1,o2 in combinations(objs, 2)))
   return r

def oGet(o, key, default=None):
   #get val by key from object(list,dict), or return <default> if key not exist
   try: return o[key]
   except (KeyError, IndexError): return default
arrGet=oGet
###list.get=arrGet

@deprecated
def arrDelta(arr, key=None):
#находим дельту между двумя каждыми соседними элементами
   #элементы должны быть числами
   dArr=[]
   tArr=sorted(arr, key=key, reverse=True)
   for i in xrange(1,len(tArr)):
      v1=float(key(tArr[i-1]) if key else tArr[i-1])
      v2=float(key(tArr[i]) if key else tArr[i])
      dArr.append(v1-v2)
   return dArr
###list.delta=arrDelta

def arrClear(arr):
   arr*=0
   return arr
arrClean=arrClear

@deprecated
def arrCreate(s1=2, s2=2, val=None):
   #create 2 dimensions array, filled with $val
   tArr=[]
   for i in xrange(s1):
      if s2 in [0, None]:
         tArr.append(val)
      else:
         tArr.append([])
         for j in xrange(s2):
            tArr[i].append(val)
   return tArr

def arrSplit(arr, pair=2, returnList=False):
   # very fast implementation for splitting list to pairs ([1,2,3,4] > [(1, 2), (3,4)])
   #! partially-duplicate of grouper()
   arr=izip(*[iter(arr)]*pair)
   if returnList: arr=list(arr)
   return arr


def dictMerge(o, withO, changed=None, changedType='key', modify=True, recursive=True):
   """ Another dict.update that supports recursive updating and store diff. """
   if not isDict(o) or not isDict(withO): raise TypeError('Need dicts')
   params={
      'cb':None,
      'modify':modify,
      'allowOrderOptimization':False,
      'recursive':recursive,
      'changedCB':None,
      'changedCBPassValues':False,
      'changedCBRecursive':False,
   }
   if changed in (None, False):
      params['allowOrderOptimization']=True
   elif changedType in ('new', 'old'):
      assert isinstance(changed, dict), 'For collecting changes-diff you must pass dict'
      def tFunc(k, vNew, vOld):
         ooo=changed
         if isinstance(k, list):
            k, kChain=k[-1], k[:-1]
            for kk in kChain:
               if kk not in ooo or not isinstance(ooo[kk], dict): ooo[kk]={}
               ooo=ooo[kk]
         ooo[k]=vOld if changedType=='old' else vNew
      params['changedCB']=tFunc
      params['changedCBPassValues']=2
      params['changedCBRecursive']=True
   elif changedType=='key':
      if isinstance(changed, dict):
         params['changedCB']=changed.__setitem__
         params['changedCBPassValues']=1
      elif isinstance(changed, list):
         params['changedCB']=changed.append
      elif isinstance(changed, set):
         params['changedCB']=changed.add
   return dictMergeEx(o, withO, **params)

dictUpdate=dictMerge

def dictMergeEx(oMain, other, cb=None, cbArgs=(), cbPassKey=False, cbMap=None, cbSwapValues=False, cbSkipIfNewKey=True, modify=True, recursive=True, allowOrderOptimization=False, filterKeys=None, isBlacklist=True, changedCB=None, changedCBRecursive=False, changedCBPassValues=False, __recursiveChain=None):
   emptyValue=NULL
   #
   _changedCB_inplaceType=None
   if isinstance(changedCB, dict): _changedCB_inplaceType='d'
   elif isinstance(changedCB, list): _changedCB_inplaceType='l'
   elif isinstance(changedCB, set): _changedCB_inplaceType='s'
   if _changedCB_inplaceType is not None and changedCBRecursive:
      raise NotImplementedError('Optimisation `changedCB_inplaceType` not implemented for recursive merging')
   if isinstance(other, dict): other=(other,)
   if not modify:
      if allowOrderOptimization:
         i2=None
         l2=len(oMain)
         for i, o in enumerate(other):
            if o is None: continue
            l=len(o)
            if l>l2:
               l2=l
               i2=i
         if i2 is not None:
            oMain, o=other[i], oMain
            other=other[:i]+(o,)+other[i+1:]
      #
      if filterKeys is None:
         oMain=oMain.copy()
      elif isBlacklist:
         oMain={k:v for k, v in oMain.iteritems() if k not in filterKeys}
      else:
         oMain={k:oMain[k] for k in filterKeys if k in oMain}
   #
   for o in other:
      if o is None: continue
      for k, v in o.iteritems():
         if filterKeys is not None and (k in filterKeys if isBlacklist else k not in filterKeys): continue
         #
         if k not in oMain and cbSkipIfNewKey:
            oMain[k]=vNew=v
            vOld=None
         else:
            vOld=oMain[k] if k in oMain else emptyValue
            if vOld is v: continue
            elif recursive and vOld is not emptyValue and isinstance(vOld, dict) and isinstance(v, dict):
               rc=(__recursiveChain+(k,) if __recursiveChain else (k,)) if changedCB and changedCBRecursive else None
               dictMergeEx(vOld, v, cb=cb, cbArgs=cbArgs, cbPassKey=cbPassKey, cbMap=cbMap, cbSwapValues=cbSwapValues, cbSkipIfNewKey=cbSkipIfNewKey, modify=True, recursive=True, changedCB=(changedCB if changedCB and changedCBRecursive else None), changedCBRecursive=changedCBRecursive, allowOrderOptimization=allowOrderOptimization, filterKeys=filterKeys, isBlacklist=isBlacklist, changedCBPassValues=changedCBPassValues, __recursiveChain=rc)
               continue
            else:
               _cb=cb if (not cbMap or k not in cbMap) else cbMap[k]
               if _cb is not None:
                  if cbPassKey:
                     vNew=_cb(k, vOld, v, *cbArgs) if cbSwapValues else _cb(k, v, vOld, *cbArgs)
                  else:
                     vNew=_cb(vOld, v, *cbArgs) if cbSwapValues else _cb(v, vOld, *cbArgs)
                  if vNew is vOld: continue
               else: vNew=v
               oMain[k]=vNew
         #
         if _changedCB_inplaceType is None and changedCB is not None:
            if not changedCBPassValues: changedCB(k)
            elif changedCBPassValues==2:
               changedCB((__recursiveChain+(k,) if __recursiveChain else k), vNew, vOld)
            else: changedCB(k, vNew)
         elif _changedCB_inplaceType=='d':
            changedCB[k]=vOld if changedCBPassValues==2 else vNew
         elif _changedCB_inplaceType=='l': changedCB.append(k)
         elif _changedCB_inplaceType=='s': changedCB.add(k)
   return oMain

def dictFilter(o, keys, allowModify=False):
   if len(keys)<=len(o)*0.5:
      if not allowModify: o=o.copy()
      for k in keys:
         if k in o: del o[k]
      return o
   else:
      if PY_V<2.7:
         return dict((k, v) for k, v in o.iteritems() if k not in keys)
      else:
         return {k: v for k, v in o.iteritems() if k not in keys}
dictExclude=dictFilter

@deprecated
def inOf(o, v):
   if isArray(o):
      try:
         return o.index(v)+1
      except: return False
   else:
      try:
         return (v in o)
      except: return False

def sendmail(**p):
   p=magicDict(p)
   _login=p.get('login', p.get('user', ''))
   _password=p.get('password', p.get('passwd', ''))
   assert _login and _password
   msg=email.MIMEMultipart.MIMEMultipart()
   msg['From']=p.get('from', _login)
   # regExp_splitEmail=re.compile("[,\s]", re.U)
   # msg['To']=email.Utils.COMMASPACE.join(regExp_splitEmail.split(p.to) if isString(p.to) else p.to)
   # msg['To']= p.to.split(',') if isString(p.to) else p.to
   if isString(p.to):
      p.to=p.to.split(',')
   msg['Subject']=p.get('subject', p.get('title', ''))
   # attach body
   # msg.attach(MIMEText(p.get('body', p.get('text', '')), p.get('mime', 'plain'), "utf-8"))
   msg.attach(MIMEText(p.get('body', p.get('text', '')), p.get('mime', 'html'), "utf-8"))
   # attach other
   #http://stackoverflow.com/a/11921241/5360266
   #https://gist.github.com/vjo/4119185
   typeMap={
      'img':MIMEImage, 'image':MIMEImage, 'png':{'o':MIMEImage, 'm':'png'}, 'jpg':{'o':MIMEImage, 'm':'jpg'}, 'jpeg':{'o':MIMEImage, 'm':'jpeg'},
      'audio':MIMEAudio, 'sound':MIMEAudio, 'mp3':{'o':MIMEAudio, 'm':'mp3'}, 'wav':{'o':MIMEAudio, 'm':'wav'},
      'pdf':{'o':MIMEApplication, 'm':'pdf'},
      'xlsx':{'o':MIMEApplication,'m':'xlsx'}
   }
   cids=[]
   for o in p.get('xlsx', ()):
      part = MIMEBase('application', "octet-stream")
      part.set_payload(open(o['path'], "rb").read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename='+o['name'])
      msg.attach(part)
   for o in p.get('attach') or ():
      cid=''
      name=''
      if isDict(o):
         oo=typeMap.get(o.get('type', ''), MIMEApplication)
         a=oo['o'](o['data'], oo['m']) if isDict(oo) else oo(o['data'])
         cid=o.get('cid', randomEx(None, cids, '<', '>'))
         name=o.get('name', '')
      else:  # binary data
         a=MIMEApplication(o)
         cid=randomEx(None, cids, '<', '>')
      # if no cid, client like MAil.app (only one?) don't show the attachment
      if not isString(cid): cid='<%s>'%cid
      if not cid.startswith('<'): cid='<%s'%cid
      if not cid.endswith('>'): cid='%s>'%cid
      cids.append(cid)
      a.add_header('Content-ID', cid)
      if name:
         a.add_header('Content-Disposition', 'attachment', filename=name)
         a.add_header('Content-Disposition', 'inline', filename=name)
      msg.attach(a)
   # sending
   isSSL=p.get('isSSL', p.get('ssl', False))
   if isSSL:
      server=smtplib.SMTP_SSL(p.server, p.get('port', 465))
   else:
      server=smtplib.SMTP(p.server, p.get('port', 587))
   server.ehlo()
   if not isSSL:
      server.starttls()
      server.ehlo()
   server.login(_login, _password)
   server.sendmail(msg['From'], p.to, msg.as_string())
   server.close()
   return True

def gmailSend(login, password, to, text, subject='', attach=None):
   return sendmail(isSSL=True, server='smtp.gmail.com', login=login, password=password, to=to, subject=subject, text=text, attach=attach)

def yaSend(login, password, to, text, subject='', attach=None):
   return sendmail(isSSL=True, server='smtp.yandex.ru', login=login, password=password, to=to, subject=subject, text=text, attach=attach)

global gmail
gmail=magicDict({'send':gmailSend})

# usage example
# createSSLTunnel(6117, 6017, sslCert='/home/sslCert/screendesk_io.chained.crt', sslKey='/home/sslCert/screendesk_io.key') or sys.exit(0)

def createSSLTunnel(port_https, port_http, sslCert='', sslKey='', stunnel_configPath='/home/sslCert/', stunnel_exec='stunnel4', stunnel_configSample='/home/sslCert/stunnel_sample.conf', stunnel_sslAllow='all', stunnel_sslOptions='-NO_SSLv2 -NO_SSLv3', stunnel_logLevel=4, stunnel_logFile='/home/python/logs/stunnel_%s_%s-%s.log', name=None):
   print 'Creating tunnel (HTTPS:%s --> HTTP:%s)..'%(port_https, port_http)
   name=name or os.path.splitext(os.path.basename(sys.argv[0]))[0]
   configSample=fileGet(stunnel_configSample)
   stunnel_sslOptions='\n'.join(['options = '+s for s in stunnel_sslOptions.split(' ') if s])
   config={'name':name, 'logLevel':stunnel_logLevel, 'sslAllow':stunnel_sslAllow, 'sslOptions':stunnel_sslOptions, 'sslCert':sslCert, 'sslKey':sslKey, 'portHttps':port_https, 'portHttp':port_http}
   config=configSample%config
   configPath=stunnel_configPath+('stunnel_%s_%s-%s.conf'%(name, port_https, port_http))
   logPath=stunnel_logFile%(name, port_https, port_http)
   fileWrite(configPath, config)
   process=subprocess.Popen([stunnel_exec, configPath], stderr=open(logPath, "w"))
   time.sleep(1)
   if process.poll():  #error
      s=fileGet(logPath)
      s='[!] '+strGet(s, '[!]', '')
      print '!!! ERROR creating tunnel\n', s
      return False
   #
   def closeSSLTunnel():
      # try: os.system('pkill -f "%s %s"'%(stunnel_exec, configPath))
      # except: pass  # noqa
      try:
         process.terminate()
         time.sleep(1)
         process.kill()
      except Exception: pass
   atexit.register(closeSSLTunnel)
   #
   def tFunc(sigId, stack, self_close=closeSSLTunnel, old=None):
      self_close()
      if old is not None:
         old(sigId, stack)
      sys.exit(0)
   for s in (signal.SIGTERM, signal.SIGINT):
      old=signal.getsignal(s)
      if not isFunction(old): old=None
      signal.signal(s, bind(tFunc, {'old':old}))
   # def checkSSLTunnel():
   #    badPatterns=['Connection rejected: too many clients']
   #    while True:
   #       time.sleep(3)
   #       #! Здесь нужно проверять лог на наличие критических ошибок
   #       stunnelLog=fileGet(logPath)
   # thread_checkSSLTunnel=threading.Thread(target=checkSSLTunnel).start()
   return process
