# -*- coding: utf-8 -*-
import json
import random
# import timeit
import requests 
import pandas as pd 
from math import floor
from threading import Thread
from datetime import datetime
from unidecode import unidecode 
from concurrent.futures import ThreadPoolExecutor, wait 

localhost_url = 'http://localhost:3000/api'

def cadastrar_emissor(emissor):
    payload_emissor = {
        '$class': 'org.conductor.blockchain.Emissor',
        'emissorId': emissor,
        'cnpj': '99999999999999'
    }
    r = requests.post(localhost_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})
    print ('Emissor criado:', emissor)

def criar_portador(payload):
    r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload), headers={'content-type': 'application/json'})
    # print(r.status_code)
    return r.status_code
    # print(r.status_code)

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
    
    cpfs = []
    payloads = []
    payload_portador = {
        '$class': 'org.conductor.blockchain.CadastrarPortador',
        'cpf': ' ',
        'nome': ' ',
        'sobrenome': ' ',
        'endereco': 'CI'
    }
    
    csv_file = pd.read_csv(csv_name, sep='|', encoding='ISO-8859-1', low_memory=False)
    csv_file = csv_file.dropna(subset=['cpf', 'nome'])
    csv_file = csv_file.drop_duplicates(subset=['cpf'])

    # len == 351749
    if quantidade > csv_file.__len__():
        print('Quantidade maior que a capacidade do csv')
        return -1

    for row in csv_file.itertuples():
        if quantidade == 0:
            break

        cpf = row.cpf.replace('*', '0')
        nome = row.nome.split(' ')
        
        payload_portador['nome'] = unidecode(nome[0])
        payload_portador['cpf'] = cpf
        if len(nome) == 1:
            payload_portador['sobrenome'] = 'seminiguem'
        else:
            payload_portador['sobrenome'] = unidecode(nome[1])
        
        cpfs.append(cpf)
        payloads.append(payload_portador)
        quantidade -= 1
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        # r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers={'content-type': 'application/json'})    
            
    
    pool = ThreadPoolExecutor(floor(len(payloads)/2))
    futures = []
    for payload in payloads:
        futures.append(pool.submit(criar_portador, payload))

    i = 0
    w = wait(futures, timeout=None)    
    for response in futures:
        if(response.result(timeout=None) != 200):
            print('remove from cpfs')
        i += 1
        
    
    print('response 0')
    temp = futures[0].result(timeout=None)
    print(temp)

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
    return requests.post(localhost_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload), headers={'content-type': 'application/json'})
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

    cards = random.sample(range(1000, 9999), len(cpfs))
    payloads = []
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
        # payloads.append(payload_cartao)
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload_cartao), headers={'content-type': 'application/json'})

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

def realizar_compra(id, card, t_i):
    dt = str(datetime.utcnow().isoformat()) 
    valor = random.randint(20, 200)                        
    # parcelas = str(random.randint(1, 3))
    payload = {
        '$class': 'org.conductor.blockchain.RealizarCompra',
        'cartao': 'resource:org.conductor.blockchain.CartaoCredito#'+str(card),
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
    }
    r = requests.post(localhost_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
    
    # print('ID: ', id)
    # print('time: ', timeit.default_timer() - t_i)
    # print('response: ', r.status_code)

def realizar_compras(cards, t_i):
    list_t = []

    for i in range(len(cards)):
        list_t.append(Thread(target=realizar_compra, args=[(i+1), cards[i], t_i]))
    
    for i in range(len(cards)):
        list_t[i].start()

    # for i in range(len(cards)):
    #     list_t[i].join()


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
    r = requests.get(localhost_url + '/org.conductor.blockchain.CadastrarCartao')
    j = r.json()
    for i in range(len(j)):
        cards.append(j[i]['numCartao'])
    return cards

def get_all_compras():
    r = requests.get(localhost_url + '/org.conductor.blockchain.RealizarCompra')
    jsons = r.json()
    return jsons