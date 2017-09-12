from bs4 import BeautifulSoup
import xml.etree.cElementTree as et
import requests
import logging
import pandas as pd
import csv
import re
import io

log = logging.getLogger('donations')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

CANDIDATES_ROLES_URL = 'http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/abrirTelaPesquisaCandidatos.action'
CANDIDATES_URL = 'http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/candidatoAutoComplete.do'
#DONATIONS_URL = 'http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/resumoReceitasByCandidato.action'
DONATIONS_URL = 'http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/exportaReceitaCsvCandidato.action'

def get_tse_roles_and_ufs():

    log.debug('Gathering all possible roles and federative units for election'
              ' candidates...')

    html_response = requests.get(CANDIDATES_ROLES_URL).text
    soup = BeautifulSoup(html_response, 'html.parser')

    roles = [str(x['value']) for x in soup.find(id="idFrmPesqCandidato_cdCargo").find_all('option')][1:]
    ufs = [str(x['value']) for x in soup.find(id="idSiglaUf").find_all('option')][1:]

    log.debug('Federative Units retrieved:\n[%s]', ','.join(ufs))
    log.debug('Possible roles retrieved:\n[%s]', ','.join(roles))

    return roles, ufs

def get_tse_candidates_ids(roles, ufs):
    log.info('Retrieving all candidates ids...')
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
        r = requests.get(CANDIDATES_URL, params = param).text
        tree = et.fromstring(r)
        candidates_id.extend(
            [element.text for element in tree.findall('sqCand')
                          if element.text != '.']
        )
        log.debug('Role %s ids from %s retrieved.', param['cdCargo'], param['sgUe'])
    log.debug('Candidates IDs retrieved:\n%s', '\n'.join(candidates_id))

    return candidates_id

if __name__ == '__main__':

    #roles, ufs = get_tse_roles_and_ufs()
    #candidates_id = get_tse_candidates_ids(roles, ufs)

    #todo: get donations recursively
    csv_data = requests.post(DONATIONS_URL, data = {'sqCandidato':'100000000134'}).text
    csv_buf = io.StringIO(csv_data)
    data = pd.read_csv(csv_buf, sep=';')
    print(data)
    #dsoup = BeautifulSoup(d, 'html.parser')

    #rows = dsoup.find_all('tr')

    #tab = []

    #for row in rows:
    #    cols = row.find_all('td')
    #    cols = [ele.text.strip() for ele in cols]
    #    tab.append([ele for ele in cols if ele])
    #    log.debug(cols)
    #    break;


