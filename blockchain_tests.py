# -*- coding: utf-8 -*-
import json
import requests
import asyncio
import concurrent.futures
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import csv
import random
from random import randint
import time
import timeit


localhost_url = 'http://150.165.167.110/api'

def cadastrar_emissor(emissor):
    payload_emissor = {
        '$class': 'org.conductor.blockchain.Emissor',
        'emissorId': emissor,
        'cnpj': '99999999999999'
    }
    r = requests.post(localhost_url + "/Emissor", data=json.dumps(payload_emissor), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
    print ('Emissor criado:', emissor)
    print(r.status_code)
    #print(r.text)

def criar_portadores(quantidade=20, csv_name=''):
    '''
        Descrição:
            A função lê um arquvo csv e cria certa quantidade de portadores na Blockchain. 
            Por enquanto a função está limitada a criação de no máximo 200 portadores.

        Utilização:
            criar_portdores(20, 'caminho/para/arquivo/nome.csv')

        Parâmetros:
            quantidade:
                O parâmetro especifica a quantidade de portadores a ser criado.
            csv_name:
                O parâmetro especifica o caminho/nome para o arquivo csv contendo as informações que serão inseridas na Blockchain. 
                ATENÇÃO: O arquivo deve conter, na sequência: nome, sobrenome e cpf.
        
        Retorno:
            A funcao retorna uma lista com os CPFs inseridos na Blockchain.
    '''    
    
    if quantidade > 200: 
        quantidade = 200
    
    cpfs = []
    payload_portador = {
        '$class': 'org.conductor.blockchain.CadastrarPortador',
        'cpf': ' ',
        'nome': ' ',
        'sobrenome': ' ',
        'endereco': 'CI'
    }
    
    with open(csv_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')           
       
        for i in range(quantidade+1):
            if i == 0:
                row = spamreader.__next__()
                continue 
            
            row = spamreader.__next__()
            
            row[0].replace(' ', '')
            row[1].replace(' ', '')
            row[2] = row[2].replace('.', '').replace('-', '')            
            cpfs.append(row[2])
            
            if row[0] == '':
                row[0] = 'zeninguem'

            if row[1] == '':
                row[1] = 'semininguem'

            payload_portador['nome'] = row[0]
            payload_portador['sobrenome'] = row[1]
            payload_portador['cpf'] = row[2]
            r = requests.post(localhost_url + '/CadastrarPortador', data=json.dumps(payload_portador), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
            print(r.status_code)
            #print(r.message)
    print('portadores criados:',len(cpfs), 'portadores')
    return cpfs

def criar_cartoes(cpfs):
    '''
        Descrição:
            A função cria um cartão para cada CPF(portador) cadastrado previamente na Blockchain.

        Utilização:
            criar_cartoes(lista_cpfs)

        Parâmetros:
            cpfs:
                O parâmetro deve conter uma lista de strings contendo os CPFs que servem para vincular o cartão a um portador na Blockchain.

        Retorno:
            A função retorna uma lista contendo os números dos cartões que foram cadastrados na Blockchain. 
            ATENÇÃO: Essa lista contêm valores inteiros.
    '''  
    #verificar ainda se é uma lista
    if not cpfs: 
        print('vazio')
        return

    cards = random.sample(range(1000, 9999), len(cpfs))
    
    payload_cartao = {
        '$class': 'org.conductor.blockchain.CadastrarCartao',
        'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
        'portador': ' ',
        'numCartao': ' ',
        'estado': 'ATIVO',
        'limiteCreditoMaximo': 99999,
        'senha': '1234',
        'cvv': '123',
        'bandeira': 'Visa',
        'diaVencimento': 31,
        'mesValidade': 12,
        'anoValidade': 2050
    }

    for i in range(len(cpfs)):       
        payload_cartao['portador'] = 'resource:org.conductor.blockchain.Portador#'+cpfs[i]
        payload_cartao['numCartao'] = str(cards[i])
        r = requests.post(localhost_url + '/CadastrarCartao', data=json.dumps(payload_cartao), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
        #print(r.status_code)
    print('cartoes criados:',len(cards), 'cartoes')
    return cards

# async def realizar_compras(cards):
#     '''
#         Descrição:
#             A função deve realizar uma compra para cada cartão da lista. Essas compras são feitas de forma paralela e assíncrona.

#         Utilização:
#             realizar_compras(lista_cards)

#         Parâmetros:
#             cards:
#                 O parâmetro deve conter uma lista de números de cartões.
#     '''  

#     if not cards:
#         print('vazio')
#         return

#     with concurrent.futures.ThreadPoolExecutor(max_workers=len(cards)) as executor:        
        
#         def multiplas_compras(id):               
#             #print('time ', datetime.now())
#             if id == 0:
#                 time.sleep(15)
#             dt = str(datetime.utcnow().isoformat()) 
#             valor = random.randint(20, 200)                        
#             # parcelas = str(random.randint(1, 3))
#             payload = {
#                 '$class': 'org.conductor.blockchain.RealizarCompra',
#                 'cartao': 'resource:org.conductor.blockchain.CartaoCredito#'+str(cards[id]),
#                 'destino': 'boteco',
#                 'senha': '1234',
#                 'cvv': '123',
#                 'meio': 'ECOMMERCE',
#                 'mesValidade': 12,
#                 'anoValidade': 2050,
#                 'parcelas': '1',
#                 'valor': valor,
#                 'moeda': 'BRL',
#                 'data': dt
#             }
#             #print(payload)
#             #print('id ', id)
#             return requests.post(localhost_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
        
#         loop = asyncio.get_event_loop()
#         futures = [
#             loop.run_in_executor(
#                 executor, 
#                 multiplas_compras,
#                 i
#             )
#             for i in range(len(cards))
#         ]
        
#         for response in await asyncio.gather(*futures):            
#             pass   

def realizar_compra(id, card):
    dt = str(datetime.utcnow().isoformat()) 
    valor = random.randint(20, 200)                        
    # parcelas = str(random.randint(1, 3))
    print('THREAD: ' + str(id) + ' CARDS: ' + str(len(card)))
    payload = []
    for i in range(len(card)):
        payload.append({
            '$class': 'org.conductor.blockchain.RealizarCompra',
            'cartao': 'resource:org.conductor.blockchain.CartaoCredito#' + str(card[i]),
            'destino': 'boteco',
            'senha': '1234',
            'cvv': '123',
            'meio': 'ECOMMERCE',
            'mesValidade': 12,
            'anoValidade': 2050,
            'parcelas': '1', # parcelas
            'valor': valor,
            'moeda': 'BRL',
            'data': dt
        })
    #print('Payload len of thread %s: %s' % (id, len(payload)))
    r = requests.post(localhost_url + '/RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
    print(r.status_code)
    #print(r.text)
    #print('REQUEST FINISHED IN THREAD: ', id)

def realizar_compras_1(cards):
    print('OP = 1')
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        jobs=[]
        #print(len(cards))
        for i in range(len(cards)):
            job=executor.submit(realizar_compra, i, cards[i])
            jobs.append(job)
	
    concurrent.futures.wait(jobs, timeout=None)
    print("1 - FINISHED")


def realizar_compras_2(cards):
    print('OP = 2')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs=[]
        print(len(cards))
        c = cards
        for i in range(int(len(cards)/10)):
            j = randint(1,20)
            job=executor.submit(realizar_compra, i, c[0:j])
            c = c[j:]
            jobs.append(job)
	
    concurrent.futures.wait(jobs, timeout=None)
    print("2 - FINISHED")


def realizar_compras_3(cards):
    print('OP = 3')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs=[]
        print(len(cards))
        for i in range(int(len(cards)/10)):
            job=executor.submit(realizar_compra, i, cards[i:i+20])
            jobs.append(job)
	
    concurrent.futures.wait(jobs, timeout=None)
    print("3 - FINISHED")



# auxiliares
def get_all_cards():
    '''
        Descrição:
            A função acessa a API e retorna todos os cartões cadastrados.

        Utilização:
            get_all_cards()

        Retorno:
            Retorna uma lista de strings com todos os cartões cadastrados.
    '''  
    cards = []
    r = requests.get(localhost_url + '/CadastrarCartao', headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG"})
    j = r.json()
    #print(j[0]['numCartao'])
    for i in range(len(j)):
        cards.append(j[i]['numCartao'])
    return cards

def get_all_compras():
    r = requests.get(localhost_url + '/RealizarCompra', headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG"})
    jsons = r.json()
    return jsons