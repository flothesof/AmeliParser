# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:29:48 2015

@author: FL232714
"""

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import math

def extract_information(block):
    """
    returns name, address, phone, prices and convention from
    a doctor html block
    """
    name = block.find('h2')
    address = block.find("div", attrs={'class':"item left adresse"})
    phone = block.find("div", attrs={'class':"item left tel"})
    prices = block.find("div", attrs={'class':"item right type_honoraires"})
    convention = block.find("div", attrs={'class':"item right convention"})
    return [item.get_text(' ') for item in [name, address, phone, prices, convention] if item is not None]

def extract_number_of_doctors(soup):
    """
    returns the number of doctors found in the query page
    returns 0 if no doctors are found in the query
    """
    p = re.compile(u"(\d+) résultats correspondent à votre recherche")
    tags = soup.find_all(name="h1")
    for tag in tags:
        if tag.string is not None:
            return int(p.findall(tag.string)[0])
    return 0

def make_query(specialty, location):
    """queries Ameli for a given specialty of doctors in a given location
    returns a pandas dataframe or None if no doctors have been found"""
    
    # create new session and open the connection to get cookies
    s = requests.Session()
    r = s.get('http://ameli-direct.ameli.fr')
    
    # extract the page towards which we make our first request
    p = re.compile('<form action="([\w\d/.-]+)" method="post">')
    suburl = p.findall(r.text)[0]
    
    # make the request
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"}
    payload = {"type":"ps",
        "ps_profession":specialty,
        "ps_localisation":location}
    r = s.post("http://ameli-direct.ameli.fr" + suburl, params=payload,
          headers=headers)
    
    # extract information
    soup = BeautifulSoup(r.text, 'html.parser')
    number_of_doctors = extract_number_of_doctors(soup)
    if number_of_doctors == 0:
        return None
    
    # loop over needed pages
    dfs = []
    for pagenumber in range(1, int(math.ceil(number_of_doctors / 20.)) + 1):
        r2 = s.post(r.url.replace("liste-resultats-page-1-par_page-20", 
                                  "liste-resultats-page-{}-par_page-20").format(pagenumber))
        soup = BeautifulSoup(r2.text)
        doctors = soup.findAll('div', attrs={"class":"item-professionnel"})
        dfs.append(pd.DataFrame([extract_information(doc) for doc in doctors], 
                 columns=['Nom', u'Adresse', u"Téléphone", u"Honoraires", "Convention"]))
    
    return pd.concat(dfs, ignore_index=True)