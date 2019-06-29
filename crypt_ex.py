# -*- coding: utf-8 -*-

import hashlib, binascii

def pbkdf2hmac(data, salt, iterations=10000, hashfunc='sha256', keylen=None):
   #wrapper for pbkdf2hmac
   try:
      c=hashlib.pbkdf2_hmac(hashfunc, data, salt, iterations, dklen=keylen)
   except UnicodeEncodeError:
      c=hashlib.pbkdf2_hmac(hashfunc, data, salt, iterations, dklen=keylen)
   return binascii.hexlify(c)

def aesEncrypt(data, password, enc="utf-8"):
   cmd=('openssl', 'enc', '-base64', '-e', '-aes-256-cbc', '-nosalt', '-pass', 'pass:%s'%password)
   res=runExternal(cmd, data=data, enc=enc)
   res=res[:-1]  #returned data ended with linebreak
   return res

def aesDecrypt(data, password, enc="utf-8"):
   cmd=('openssl', 'enc', '-base64', '-d', '-aes-256-cbc', '-nosalt', '-pass', 'pass:%s'%password)
   res=runExternal(cmd, data=data, enc=enc)
   res=res[:-1]  #returned data ended with linebreak
   return res

def sha1(text):
   #wrapper for sha1
   try: c=hashlib.sha1(text)
   except UnicodeEncodeError: c=hashlib.sha1(strUniDecode(text))
   return c.hexdigest()

def sha224(text):
   #wrapper for sha224
   try: c=hashlib.sha224(text)
   except UnicodeEncodeError: c=hashlib.sha224(strUniDecode(text))
   return c.hexdigest()

#? look at this implementation https://github.com/BIDS/sha256
def sha256(text):
   #wrapper for sha256
   try: c=hashlib.sha256(text)
   except UnicodeEncodeError: c=hashlib.sha256(strUniDecode(text))
   return c.hexdigest()

def sha384(text):
   #wrapper for sha384
   try: c=hashlib.sha384(text)
   except UnicodeEncodeError: c=hashlib.sha384(strUniDecode(text))
   return c.hexdigest()

def sha512(text):
   #wrapper for sha512
   try: c=hashlib.sha512(text)
   except UnicodeEncodeError: c=hashlib.sha512(strUniDecode(text))
   return c.hexdigest()

def md5(text):
   #wrapper for md5
   try: c=hashlib.md5(text)
   except UnicodeEncodeError: c=hashlib.md5(strUniDecode(text))
   return c.hexdigest()
