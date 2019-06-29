# -*- coding: utf-8 -*-

def isURL(url):
   if not url or not isStr(url): return False
   try:
      r=urlparse(urljoin(url, '/'))
      return r.scheme and r.netloc and r.path and ('.' in r.netloc)
   except Exception:
      return False

def cropURL(t):
   if(t[:7]=='http://'): t=t[7:]
   if(t[:8]=='https://'): t=t[8:]
   if(t[:4]=='www.'): t=t[4:]
   return t

def rebuildURL(url, cb):
   #чиним адрес, чтобы парсить адреса без scheme
   for s in ['//', 'http://', 'https://', 'ftp://']:
      if url.startswith(s): break
   else: url='//'+url if(url.startswith('/') or '.' in strGet(url, '', '/')) else '///'+url
   #парсим
   scheme, netloc, path, query, fragment=urlsplit(url)
   if 'netloc' in cb:
      netloc=cb['netloc'](netloc) if callable(cb['netloc']) else cb['netloc']
   if 'path' in cb:
      path=cb['path'](path) if callable(cb['path']) else cb['path']
   if 'scheme' in cb:
      scheme=cb['scheme'](scheme) if callable(cb['scheme']) else cb['scheme']
   if 'fragment' in cb:
      if callable(cb['fragment']):
         fragment=parse_qs(fragment)
         tArr1={}
         for k, v in fragment.iteritems():
            if callable(cb['fragment']): s=cb['fragment'](k, v)
            elif isDict(cb['fragment']): s=oGet(cb['fragment'], k, v)
            else: s=cb['fragment']
            if s is not False: tArr1[k]=s
         try: fragment=urlencode(tArr1, doseq=True)
         except: fragment=''
      else: fragment=cb['fragment']
   if 'query' in cb:
      if callable(cb['query']) or isDict(cb['query']):
         query=parse_qs(query)
         tArr1={}
         for k, v in query.iteritems():
            if callable(cb['query']): s=cb['query'](k, v)
            elif isDict(cb['query']): s=oGet(cb['query'], k, v)
            else: s=cb['query']
            if s is not False: tArr1[k]=s
         try: query=urlencode(tArr1, doseq=True)
         except: query=''
      else: query=cb['query']
   return urlunsplit((scheme, netloc, path, query, fragment))
