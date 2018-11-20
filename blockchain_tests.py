# -*- coding: utf-8 -*-
import json
import random
# import timeit
import logging
import requests 
import pandas as pd 
from math import floor
from threading import Thread
from datetime import datetime
from unidecode import unidecode 
from concurrent.futures import ThreadPoolExecutor, wait 

api_url = 'http://localhost:3000/api'
# api_url = 'http://150.165.167.110/api'

def cadastrar_emissor(emissor):    
    jsons = requests.get(api_url + "/org.conductor.blockchain.Emissor").json()    
    if(len(jsons) > 0):    
        emissores = []
        for em in jsons:
            emissores.append(em['emissorId'])
        if(not(emissor in emissores)):
            payload_emissor = {
                '$class': 'org.conductor.blockchain.Emissor',
                'emissorId': emissor,
                'cnpj': '99999999999999'
            }
            r = requests.post(api_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})
            print('Emissor criado:', emissor)
        else:
            print('Emissor já cadastrado.')
    else:
        payload_emissor = {
            '$class': 'org.conductor.blockchain.Emissor',
            'emissorId': emissor,
            'cnpj': '99999999999999'
        }
        r = requests.post(api_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})
        print ('Emissor criado:', emissor)

def criar_portador(payload):
    r = requests.post(api_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload), headers={'content-type': 'application/json'})
    # ret = []
    # ret.append(r)
    # ret.append(payload)    
    # return ret
    
def criar_portadores(csv_name='', inicio=0, quantidade=20):
    '''
        Descrição:
            A função lê um arquvo csv e cria certa quantidade de portadores na Blockchain. 
            Por enquanto a função está limitada a criação de no máximo 200 portadores.

        Utilização:
            criar_portdores('caminho/para/arquivo/nome.csv', 0, 20)

        Parâmetros:
            csv_name:
                O parâmetro especifica o caminho/nome para o arquivo csv contendo as informações que serão inseridas na Blockchain. 
                ATENÇÃO: O arquivo deve conter, na sequência: nome, sobrenome e cpf.
            inicio:
                Parametro especifica o ponto inicial, no csv, de onde vai ser criado os portadores.
            quantidade:
                O parâmetro especifica a quantidade de portadores a ser criado.            

        Retorno:
            A funcao retorna uma lista com os CPFs inseridos na Blockchain.
    '''    
       
    csv_file = pd.read_csv(csv_name, sep='|', encoding='ISO-8859-1', low_memory=False)
    csv_file = csv_file.dropna(subset=['cpf', 'nome'])
    csv_file = csv_file.drop_duplicates(subset=['cpf'])
    # len == 351749
    if (inicio+quantidade) > csv_file.__len__():
        print('Quantidade maior que a capacidade do csv')
        return -1

    if inicio < 0:
        inicio = 0

    cpfs = []
    payloads = []
    payload_portador = {
        '$class': 'org.conductor.blockchain.CadastrarPortador',
        'cpf': ' ',
        'nome': ' ',
        'sobrenome': ' ',
        'endereco': 'CI'
    }

    temp = 0
    for row in csv_file.itertuples():
        if quantidade == 0:
            break

        if temp < inicio:
            temp += 1
            continue

        cpf = row.cpf.replace('*', '0')
        nome = row.nome.split(' ')
        
        payload_portador['nome'] = unidecode(nome[0])
        payload_portador['cpf'] = cpf
        if len(nome) == 1:
            payload_portador['sobrenome'] = 'seminiguem'
        else:
            payload_portador['sobrenome'] = unidecode(nome[1])
        
        # cpfs.append(cpf)
        payloads.append(payload_portador)
        quantidade -= 1
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        r = requests.post(api_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers={'content-type': 'application/json'})    
        if(r.status_code < 300 and r.status_code > 100):    
            cpfs.append(cpf)
    
    # pool = ThreadPoolExecutor(floor(len(payloads)/2))
    # futures = []
    # for payload in payloads:
    #     futures.append(pool.submit(criar_portador, payload))
    
    # w = wait(futures, timeout=None)    
    # for response in futures:        
    #     ret = response.result(timeout=None)
    #     if(ret[0].status_code != 200):
    #         print('remove from cpfs')
    #         print(ret[1]['cpf'])
    #         cpfs.remove(ret[1]['cpf'])            

    ####### diretamente com Threads #######
    # list_t = []
    # for payload in payloads:
    #     list_t.append(Thread(target=criar_portador, args=[payload]))

    # for i in range(len(payloads)):
    #     list_t[i].start()

    # for i in range(len(cards)):
    #     list_t[i].join()

    print('portadores criados:',len(cpfs), 'portadores')
    return cpfs

def criar_cartao(payload):    
    r = requests.post(api_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload), headers={'content-type': 'application/json'})
    # return
    # print(r.status_code)

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

    # verificar ainda se é uma lista
    if not cpfs: 
        print('vazio')
        return
    
    c = get_all_cards()
    if len(c) <= 0:
        cards = random.sample(range(1000, 3000), len(cpfs))
    else:
        random.seed()
        beg = random.randint(1, 50)
        end = random.randint(50, 75)
        random.seed()
        cards = random.sample(range(beg*3000, end*5000), len(cpfs))
    
    payloads = []
    payload_cartao = {
        '$class': 'org.conductor.blockchain.CadastrarCartao',
        'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
        'portador': ' ',
        'numCartao': ' ',
        'estado': 'ATIVO',
        'limiteCreditoMaximo': 9999999,
        'senha': '1234',
        'cvv': '123',
        'bandeira': 'Visa',
        'diaVencimento': 31,
        'mesValidade': 12,
        'anoValidade': 2050
    }

    r = []
    for i in range(len(cpfs)):       
        payload_cartao['portador'] = 'resource:org.conductor.blockchain.Portador#'+cpfs[i]
        payload_cartao['numCartao'] = str(cards[i])
        # payloads.append(payload_cartao)
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        r.append(requests.post(api_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload_cartao), headers={'content-type': 'application/json'}))

    for i in range(len(r)):
        if(r[i].status_code >= 300 and r[i].status_code <= 100):    
            cards.remove(cards[i])
    
    # pool = ThreadPoolExecutor(floor(len(payloads)/2))
    # futures = []
    # for payload in payloads:
    #     futures.append(pool.submit(criar_cartao, payload))

    # w = wait(futures, timeout=None)    
    # for response in futures:
    #     print(response.result(timeout=0))

    ####### diretamente com Threads #######
    # list_t = []
    # for payload in payloads:
    #     list_t.append(Thread(target=criar_cartao, args=[payload]))

    # for i in range(len(payloads)):
    #     list_t[i].start()

    # for i in range(len(payloads)):
    #     list_t[i].join()

    print('cartoes criados:',len(cards), 'cartoes')
    return cards

# def realizar_compra(card):
#     dt = str(datetime.utcnow().isoformat()) 
#     valor = random.randint(20, 200)                        
#     # parcelas = str(random.randint(1, 3))
#     payload = {
#         '$class': 'org.conductor.blockchain.RealizarCompra',
#         'cartao': 'resource:org.conductor.blockchain.CartaoCredito#'+str(card),
#         'destino': 'boteco',
#         'senha': '1234',
#         'cvv': '123',
#         'meio': 'ECOMMERCE',
#         'mesValidade': 12,
#         'anoValidade': 2050,
#         'parcelas': '1', # parcelas
#         'valor': valor,
#         'moeda': 'BRL',
#         'data': dt
#     }
#     r = requests.post(api_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
    
#     # print('ID: ', id)
#     # print('time: ', timeit.default_timer() - t_i)
#     # print('response: ', r.status_code)

# def realizar_compras(cards):
#     pool = ThreadPoolExecutor(floor(len(cards)/2))
#     futures = []
#     for card in cards:
#         futures.append(pool.submit(realizar_compra, card))
    
#     w = wait(futures, timeout=None)    
#     for response in futures:        
#         ret = response.result(timeout=None)
#         print(ret)

def realizar_compra(id, card):
    dt = str(datetime.utcnow().isoformat()) 
    valor = random.randint(20, 200)                        
    # parcelas = str(random.randint(1, 3))
    print('THREAD: ' + str(id) + ' CARDS: ' + str(len(card)) + ' CARDS: ' + str(card))
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
    # r = requests.post(api_url + '/RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
    r = requests.post(api_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
    print(r.status_code)
    #print(r.text)
    #print('REQUEST FINISHED IN THREAD: ', id)

def realizar_compras_1(cards):
    print('OP = 1')
    with ThreadPoolExecutor(max_workers=len(cards)) as executor:
        jobs=[]
        #print(len(cards))        
        for i in range(len(cards)):            
            job=executor.submit(realizar_compra, i, cards[i:i+1])
            jobs.append(job)            
	
    wait(jobs, timeout=None)
    print("1 - FINISHED")


def realizar_compras_2(cards):
    print('OP = 2')
    with ThreadPoolExecutor(max_workers=10) as executor:
        jobs=[]
        print(len(cards))
        c = cards
        for i in range(int(len(cards)/10)):
            j = random.randint(1,20)
            job=executor.submit(realizar_compra, i, c[0:j])
            c = c[j:]
            jobs.append(job)
	
    wait(jobs, timeout=None)
    print("2 - FINISHED")


def realizar_compras_3(cards):
    print('OP = 3')
    with ThreadPoolExecutor(max_workers=10) as executor:
        jobs=[]
        print(len(cards))
        index = 0
        for i in range(int(len(cards)/10)):
            if index >= len(cards):
                break
            job=executor.submit(realizar_compra, i, cards[index:index+20])
            jobs.append(job)
            index += 20            
	
    wait(jobs, timeout=None)
    print("3 - FINISHED")

################## auxiliares ##################
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
    r = requests.get(api_url + '/org.conductor.blockchain.CartaoCredito')
    jsons = r.json()        
    for json in jsons:        
        cards.append(json['numeroCartao'])
        # cards.append(json['limiteDisponivel'])
    return cards    

def get_all_compras():
    r = requests.get(api_url + '/org.conductor.blockchain.Compra')
    jsons = r.json()
    return jsons

def get_all_portadores():
    r = requests.get(api_url + '/org.conductor.blockchain.Portador')
    jsons = r.json()
    return jsons  