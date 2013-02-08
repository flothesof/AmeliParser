# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 08:59:52 2012

@author: FL232714
"""

import sys, codecs, pdb
from HTMLParser import HTMLParser

def win32_unicode_argv():
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of Unicode
    strings.

    Versions 2.x of Python don't support Unicode in sys.argv on
    Windows, with the underlying Windows API instead replacing multi-byte
    characters with '?'.
    """

    from ctypes import POINTER, byref, cdll, c_int, windll
    from ctypes.wintypes import LPCWSTR, LPWSTR

    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        return [argv[i] for i in
                xrange(start, argc.value)]


# create a subclass and override the handler methods
class AmeliHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {'nom': [], 'prof': [], 'tel': []}
        self.listening = False
        self.data_type = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if len(attrs) == 1:
                if attrs[0] == ('class', 'medecin-item-nom-recherche'):
                    self.listening = True
                    self.data_type = 'nom'
                elif attrs[0] == ('class', 'medecin-item-prof-recherche'):
                    self.listening = True
                    self.data_type = 'prof'
                elif attrs[0] == ('class', 'medecin-item-tel-recherche'):
                    self.listening = True
                    self.data_type = 'tel'
                    
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.listening == True:
                #il faut penser à archiver les données
                self.listening = False
            else:
                self.listening = False
                
    def handle_data(self, data):
        if self.listening == True:
            self.data[self.data_type].append(data)
    
if len(sys.argv) > 1:
    argv = win32_unicode_argv()
    filename = unicode(argv[1])
    print filename
else:
    filename = u'input_ophtalmo_75014.txt'

savename = 'output_' + filename[6:-4] + '.csv'
lines = codecs.open(filename, "r", "utf-8").readlines()

# instantiate the parser and feed it some HTML
ameli_parser = AmeliHTMLParser()

for line in lines: #test_line 
#    line = line.encode()
    ameli_parser.feed(line)

#==============================================================================
# # extract data and write output file
#==============================================================================

# carte vitale
data = {}    
data['vitale'] = filter(lambda x: x!='', map(unicode.strip, ameli_parser.data['prof']))

# phone numbers and conventions
s = ''.join(ameli_parser.data['tel'])
s = map(unicode.strip, s.split('\n'))
data['tel'] = []   
data['convention'] = []
for i in range(1, len(s)):
    if i % 2 == 1:
        data['tel'].append(s[i])
    if i % 2 == 0:
        data['convention'].append(s[i])    

# names and addresses
s = ' '.join(ameli_parser.data['nom'])    
s = map(unicode.strip, s.split('\n'))
data['nom'] = []
data['adresse'] = []
for i in range(1, len(s)):
    if (i - 1) % 4 == 0:
        data['nom'].append(s[i])
    if (i - 1) % 4 == 3:
        data['adresse'].append(s[i])

# write data to file
with codecs.open(savename, 'w', 'utf-8') as f:
    f.writelines('name,phone,carte vitale,convention,location\n')
    for i in range(len(data['adresse'])):        
        f.writelines(','.join([data['nom'][i], data['tel'][i],
                               data['vitale'][i], data['convention'][i],
                                data['adresse'][i]]) + '\n')