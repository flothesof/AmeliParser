# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 08:59:52 2012

@author: FL232714
"""

import sys, codecs, pdb
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
        print "Has attributes:", attrs
        
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :", data

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
    pass
else:
    filename = u'input_kiné_75014.txt'
    savename = 'output_' + filename[6:-4] + '.csv'
    lines = codecs.open(filename).readlines()
    
    # instantiate the parser and feed it some HTML
    ameli_parser = AmeliHTMLParser()
    
    for line in lines: #test_line 
        ameli_parser.feed(line)

    data = {}    
    # les cartes vitales 
    data['vitale'] = filter(lambda x: x!='', map(str.strip, ameli_parser.data['prof']))
    
    #les numéros de téléphone
    s = ''.join(ameli_parser.data['tel'])
    s = map(str.strip, s.split('\t'))
    data['tel'] = []   
    data['convention'] = []
    for i in range(len(s)):
        if i % 5 == 1:
            data['tel'].append(s[i])
        if i % 5 == 4:
            data['convention'].append(s[i])    
    
    # les noms et adresses
    s = ' '.join(ameli_parser.data['nom'])    
    s = map(str.strip, s.split('\t'))
    data['nom'] = []
    data['adresse'] = []
    for i in range(len(s)):
        if i % 34 == 11:
            data['nom'].append(s[i])
        if i % 34 == 33:
            data['adresse'].append(s[i])

    with codecs.open(savename, 'w') as f:
        f.writelines('name,phone,carte vitale,convention,location\n')
        for i in range(len(data['adresse'])):        
            f.writelines(','.join([data['nom'][i], data['tel'][i],
                                   data['vitale'][i], data['convention'][i],
                                    data['adresse'][i]]) + '\n')