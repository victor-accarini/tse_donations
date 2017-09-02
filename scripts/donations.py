from bs4 import BeautifulSoup
import xml.etree.cElementTree as et
import requests
import pandas as pd
import re

DONATIONS_URL = 'http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/abrirTelaPesquisaCandidatos.action'

response = requests.get(DONATIONS_URL).text
soup = BeautifulSoup(response, 'html.parser')

roles = [str(x['value']) for x in soup.find(id="idFrmPesqCandidato_cdCargo").find_all('option')][1:]
ufs = [str(x['value']) for x in soup.find(id="idSiglaUf").find_all('option')][1:]

params = []

for uf in ufs:
    for role in roles:
        p = {}
        p['sgUe'] = uf
        p['cdCargo'] = role
        p['noCandLimpo'] = ''
        params.append(p)
        
candidates_id = []

for param in params:
    r = requests.get('http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/candidatoAutoComplete.do', params = param).text
    tree = et.fromstring(r)
    candidates_id.append([element.text for element in tree.findall('sqCand') if element.text != '.'])


