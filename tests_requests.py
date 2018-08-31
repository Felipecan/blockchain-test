# -*- coding: utf-8 -*-
import json
import requests
import asyncio
import concurrent.futures
from datetime import datetime

from threading import Thread

localhost_url = 'http://localhost:3000/api'

# deve retornar um vetor contendo os CPFS 
# def criar_portadores(quantidade, emissor):
    # a partir da quantidade, gerar nomes e cpfs aleatorios para os portadores

# deve retornar um vetor contendo os numeros dos cartoes
# def criar_cartoes(cpfs):
    # a partir do vetor com os cpfs, criar os cartoes para eles.

# Cadastrar Emissor
headers = {'content-type': 'application/json'}

payload_emissor = {
    '$class': 'org.conductor.blockchain.Emissor',
    'emissorId': 'Renner',
    'cnpj': '99999999999999'
}
r = requests.post(localhost_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload_emissor), headers=headers)

# Cadastrar Portador
payload_portador = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '00000000000',
    'nome': 'Ze',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)

payload_portador = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '11111111111',
    'nome': 'Joao',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)

payload_portador = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '22222222222',
    'nome': 'Luiz',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)

payload_portador = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '33333333333',
    'nome': 'Silvia',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)

payload_portador = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '44444444444',
    'nome': 'Maria',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload_portador), headers=headers)

# Cadastrar Cartão
payload_cartao = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#00000000000',
    'numCartao': '5555555555555555',
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

payload_cartao = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#11111111111',
    'numCartao': '6666666666666666',
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

payload_cartao = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#22222222222',
    'numCartao': '7777777777777777',
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

payload_cartao = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#33333333333',
    'numCartao': '8888888888888888',
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

payload_cartao = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#44444444444',
    'numCartao': '9999999999999999',
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

# Realizar compras
async def main():
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        loop = asyncio.get_event_loop()
        
        def multiplas_compras(id):
            arr_num_card = ['5555555555555555', '6666666666666666', '7777777777777777', '8888888888888888', '9999999999999999']            
            dt = str(datetime.utcnow().isoformat())    
            card = 'resource:org.conductor.blockchain.CartaoCredito#' + arr_num_card[id]
            payload = {
                '$class': 'org.conductor.blockchain.RealizarCompra',
                'cartao': card,
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
            print(payload)
            return requests.post(localhost_url + '/org.conductor.blockchain.RealizarCompra', data=json.dumps(payload), headers={'content-type': 'application/json'})
       
        futures = [
            loop.run_in_executor(
                executor, 
                multiplas_compras,
                i
            )
            for i in range(5)
        ]
        for response in await asyncio.gather(*futures):
            pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

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
