# -*- coding: utf-8 -*-

import re

regExp_parseFloat=re.compile(r"-{0,1}[0-9]+([.]{0,1}[0-9]*)", re.U)
regExp_specialSymbols0=re.compile(r"[\W_]", re.U)
regExp_lettersReplace0=re.compile(r"[А-Яа-я]", re.U)
regExp_hex=re.compile(r"^[a-f0-9]*$", re.U)
regExp_htmlEncoding=re.compile(r'<meta .*?charset="?([\w-]*).*?>', re.U)
regExp_isEmail=re.compile(r'^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', re.U)
# regExp_isURL=re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)', re.U)
regExp_isPassword=re.compile(r'^[\w_]{6,18}$', re.U)
regExp_anySymbol=re.compile(r'.{1}', re.U)
regExp_anyText=re.compile(r'.*', re.U)
regExp_anyWord=re.compile(r'[a-zA-Zа-яёА-ЯЁ0-9_\-]+', re.U)
