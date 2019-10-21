import re
import os
from time import sleep
from threading import Thread

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


URL = 'https://www.letras.mus.br'
DIR = './dataset-musica'
regex_br = re.compile(r'<\/?br\/?>')
regex_p = re.compile(r'<\/?p>')


def buscar_musica(tipo, titulo, href_musica, musicas_salva):
    if titulo not in musicas_salva:
        r = requests.get(f"{URL}{href_musica}")
        html = BeautifulSoup(r.text, 'html.parser')
        texto_musica = html.find('div', {'class': 'cnt-letra p402_premium'}).find_all('p')

        musica = ''
        for texto in texto_musica:
            musica += regex_p.sub('', regex_br.sub('\n', str(texto)))
            if not musica.endswith('\n'):
                musica += '\n'

        open(f'{DIR}/{tipo}/{titulo}', 'w').write(musica)
        sleep(2)


def genero():
    for tipo in ['forro', 'funk', 'sertanejo']:
        r = requests.get(f'{URL}/mais-acessadas/{tipo}/')
        html = BeautifulSoup(r.text, 'html.parser')
        top_musicas = html.find('ol', {'class': 'top-list_mus cnt-list--col1-3'}).find_all('a')

        ths = []
        musicas_salva = set(os.listdir(f'{DIR}/{tipo}'))
        for musica in tqdm(top_musicas):
            t = Thread(target=buscar_musica, args=(tipo, musica.get('title').replace('/', ''), 
                       musica.get('href'), musicas_salva))
            ths.append(t)

            if len(ths) % 50 == 0:
                for t in ths:
                    t.start()

                for t in ths:
                    t.join()

                ths = []


def top_musicas(tipo, artista):
    tipo += '/artistas/' + artista[:-1]

    try:
        os.mkdir(f'{DIR}/{tipo}')
    except FileExistsError:
        pass

    r = requests.get(f"{URL}{artista}")
    html = BeautifulSoup(r.text, 'html.parser')
    top20 = html.find('ol', {'class': 'cnt-list cnt-list--num cnt-list--col2'}).find_all('a')

    musicas_salva = set(os.listdir(f'{DIR}/{tipo}'))
    for musica in top20:
        buscar_musica(tipo, musica.get('title').replace('/', ''), musica.get('href'), musicas_salva)


def artista():
    for tipo in ['sertanejo']: # ['forro', 'funk', 'sertanejo']:
        r = requests.get(f'{URL}/mais-acessadas/{tipo}/')
        html = BeautifulSoup(r.text, 'html.parser')
        top_artistas = html.find('ol', {'class': 'top-list_art'}).find_all('a')

        ths = []
        for artista in tqdm(top_artistas):
            t = Thread(target=top_musicas, args=(tipo, artista.get('href')))
            ths.append(t)

            if len(ths) % 10 == 0:
                for t in ths:
                    t.start()

                for t in ths:
                    t.join()

                ths = []


if __name__ == '__main__':
    artista()
    
