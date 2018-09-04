# -*- coding: utf-8 -*-
import json
import requests
import asyncio
import concurrent.futures
from datetime import datetime

from threading import Thread
import csv
import random

localhost_url = 'http://localhost:3000/api'

headers = {'content-type': 'application/json'}

# cadastra o emissor
payload_emissor = {
    '$class': 'org.conductor.blockchain.Emissor',
    'emissorId': 'Renner',
    'cnpj': '99999999999999'
}
r = requests.post(localhost_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload_emissor), headers=headers)

# deve retornar um vetor contendo os CPFS (retornando em string).
def criar_portadores(quantidade):
    
    if quantidade > 200: 
        quantidade = 200
    
    cpfs = []

    with open('pessoas.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')           
       
        for i in range(quantidade+1):
            if i == 0:
                row = spamreader.__next__()
                continue 
            
            row = spamreader.__next__()
            row[0] = row[0].replace(' ', '')
            row[1] = row[1].replace(' ', '')
            row[2] = row[2].replace('.', '').replace('-', '')            
            #print(row)
            cpfs.append(row[2])
            payload_portador = {
                '$class': 'org.conductor.blockchain.CadastrarPortador',
                'cpf': row[2],
                'nome': row[0],
                'sobrenome': row[1],
                'endereco': 'CI'
            }
            r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)
    
    return cpfs

# deve retornar um vetor contendo os numeros dos cartoes (retornando em inteiro).
def criar_cartoes(cpfs):
    
    cards = random.sample(range(1000, 9999), len(cpfs))

    for i in range(len(cpfs)):       
        payload_cartao = {
            '$class': 'org.conductor.blockchain.CadastrarCartao',
            'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
            'portador': 'resource:org.conductor.blockchain.Portador#'+cpfs[i],
            'numCartao': str(cards[i]),
            'estado': 'ATIVO',
            'limiteCreditoMaximo': 99999,
            'senha': '1234',
            'cvv': '123',
            'bandeira': 'Visa',
            'diaVencimento': 31,
            'mesValidade': 12,
            'anoValidade': 2050
        }
        r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload_cartao), headers=headers)

    return cards

# 
async def realizar_compras(cards):

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(cards)) as executor:        
        
        def multiplas_compras(id):               
            dt = str(datetime.utcnow().isoformat()) 
            valor = random.randint(20, 200)
            # parcelas = str(random.randint(1, 3))
            payload = {
                '$class': 'org.conductor.blockchain.RealizarCompra',
                'cartao': 'resource:org.conductor.blockchain.CartaoCredito#'+str(cards[id]),
                'destino': 'boteco',
                'senha': '1234',
                'cvv': '123',
                'meio': 'ECOMMERCE',
                'mesValidade': 12,
                'anoValidade': 2050,
                'parcelas': '1',
                'valor': valor,
                'moeda': 'BRL',
                'data': dt
            }
            #print(payload)
            return requests.post(localhost_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
        
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                multiplas_compras,
                i
            )
            for i in range(len(cards))
        ]
        for response in await asyncio.gather(*futures):
            pass    


cpfs = criar_portadores(20)
cards = criar_cartoes(cpfs)
loop = asyncio.get_event_loop()
loop.run_until_complete(realizar_compras(cards))

'''
def realizar_compras(id, num_card):
    dt = str(datetime.utcnow().isoformat()) 
    temp = 'resource:org.conductor.blockchain.CartaoCredito#' + num_card
    payload = {
        '$class': 'org.conductor.blockchain.RealizarCompra',
        'cartao': temp,
        'destino': 'boteco',
        'senha': '1234',
        'cvv': '123',
        'meio': 'ECOMMERCE',
        'mesValidade': 12,
        'anoValidade': 2050,
        'parcelas': '1',
        'valor': id,
        'moeda': 'BRL',
        'data': dt
    }
    r = requests.post(localhost_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
    print(payload)
    print(r)

arr_t = []
arr_num_card = ['5555555555555555', '6666666666666666', '7777777777777777', '8888888888888888', '9999999999999999']
for i in range(5):
    arr_t.append(Thread(target=realizar_compras,args=[(i+1), arr_num_card[i]]))

for i in range(5):
    arr_t[i].start()
'''
