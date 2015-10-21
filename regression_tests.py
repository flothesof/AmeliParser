# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:58:30 2015

@author: FL232714
"""
import new_parser
from bs4 import BeautifulSoup

def test_extraction1():
    block = BeautifulSoup("""<div class="item-professionnel"><div class="item-professionnel-inner"><span class="num">1</span><div class="nom_pictos"><h2><a href="/professionnels-de-sante/recherche-1/fiche-detaillee-B7c1lTM1MTu1-72749a39f3cde0042df09cdc8951bd9a.html"><strong>VAN WENT</strong> CHARLES</a></h2><div class="pictos"><img alt="Accepte la carte Vitale" class="infobulle" src="/resources_ver/20150826115145/images/picto_cartevitale.png"/></div><div class="clear"></div></div><div class="clear"></div><div class="elements"><div class="item left"></div><div class="item right type_honoraires">Honoraires libres</div><div class="clear"></div><div class="item left"></div><div class="item right convention"><a alt="Les médecins fixent librement leurs tarifs et peuvent donc pratiquer des dépassements d’honoraires avec tact et mesure. L’Assurance Maladie rembourse les consultations et actes réalisés par ces médecins sur la base des tarifs fixés dans la convention (tarifs applicables au médecin de secteur 2), le montant des éventuels dépassements d’honoraires reste à votre charge." class="infobulle" href="#">Conventionné secteur 2</a></div><div class="clear"></div><div class="item left adresse">SELARL CHASSIGNOL VAN WENT<br/>79 AVENUE DU GENERAL LECLERC<br/>75014 PARIS</div><div class="clear"></div></div><div class="clear"></div></div></div>""", 
                          'html.parser')    
    info = new_parser.extract_information(block)
    assert(len(info) == 5)
    
def test_extraction2():
    block = BeautifulSoup("""<div class="item-professionnel"><div class="item-professionnel-inner"><span class="num">1</span><div class="nom_pictos"><h2><a href="/professionnels-de-sante/recherche-1/fiche-detaillee-Bbs1lTUwMDO7-980a7113e4ee86e420d92353e43e82c9.html"><strong>KONE FEZING</strong> ALEXANDRE</a></h2><div class="pictos"><img alt="Accepte la carte Vitale" class="infobulle" src="/resources_ver/20150826115145/images/picto_cartevitale.png"/></div><div class="clear"></div></div><div class="clear"></div><div class="elements"><div class="item left"></div><div class="item right type_honoraires">Honoraires sans dépassement</div><div class="clear"></div><div class="item left"></div><div class="item right convention"><a alt="Les médecins appliquent les tarifs fixés dans la convention nationale sans dépassements d’honoraires (dits tarifs conventionnels, opposables ou de secteur 1). Ces tarifs servent de base au remboursement de l’Assurance Maladie. Des dépassements d’honoraires ne peuvent être facturés qu’à titre exceptionnel, pour des motifs liés, par exemple à des exigences de temps ou de lieu du patient (DE). Ces dépassements ne sont pas remboursés par l’Assurance Maladie, que vous soyez dans le parcours de soins ou non." class="infobulle" href="#">Conventionné secteur 1</a></div><div class="clear"></div><div class="item left adresse">ALEXANDRE KONE<br/>531 RUE RENE D'HESPEL<br/>59910 BONDUES</div><div class="clear"></div></div><div class="clear"></div></div></div>""",
                          'html.parser')
    info = new_parser.extract_information(block)
    assert(len(info) == 5)
    
def test_single():
    df = new_parser.make_single_query('ophtalmologiste', '59000')
    assert(df.shape == (47, 7))

def test_multiple():
    df = new_parser.make_multiple_query('ophtalmologiste', ["59910", "59166", "59560", "59170", "59510"])
    assert(df.shape == (4, 7))    
