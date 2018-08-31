# -*- coding: utf-8 -*-
import json
import requests
import asyncio
import concurrent.futures
from datetime import datetime

from threading import Thread

localhost_url = 'http://localhost:3000/api'

# Cadastrar Emissor
headers = {'content-type': 'application/json'}

payload = {
    '$class': 'org.conductor.blockchain.Emissor',
    'emissorId': 'Renner',
    'cnpj': '99999999999999'
}
r = requests.post(localhost_url + "/org.conductor.blockchain.Emissor", data=json.dumps(payload), headers=headers)

# Cadastrar Portador
payload = {
    '$class': 'org.conductor.blockchain.CadastrarPortador',
    'cpf': '00000000000',
    'nome': 'Ze',
    'sobrenome': 'Silva',
    'endereco': 'CI'
}
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload), headers=headers)

# Cadastrar Cartão
payload = {
    '$class': 'org.conductor.blockchain.CadastrarCartao',
    'emissor': 'resource:org.conductor.blockchain.Emissor#Renner',
    'portador': 'resource:org.conductor.blockchain.Portador#00000000000',
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
r = requests.post(localhost_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload), headers=headers)

# Realizar compras
# async def main():
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

#         loop = asyncio.get_event_loop()
#         payload = {
#             '$class': 'org.conductor.blockchain.RealizarCompra',
#             'cartao': 'resource:org.conductor.blockchain.CartaoCredito#6666666666666666',
#             'destino': 'boteco',
#             'senha': '1234',
#             'cvv': '123',
#             'meio': 'ECOMMERCE',
#             'mesValidade': 12,
#             'anoValidade': 2050,
#             'parcelas': '1',
#             'valor': 0,
#             'moeda': 'BRL',
#             'data': ''
#         }
#         def multiplas_compras(arg_url):
#             dt = str(datetime.utcnow().isoformat())    
#             payload['data'] = dt
#             payload['valor'] += 1
#             print(payload)
#             return requests.post(localhost_url + arg_url, data=json.dumps(payload), headers={'content-type': 'application/json'})

#         # futures = []        
#         # for i in range(20):
#         #     futures.append(loop.run_in_executor(executor, multiplas_compras, '/org.conductor.blockchain.RealizarCompra')
#         futures = [
#             loop.run_in_executor(
#                 executor, 
#                 multiplas_compras,
#                 '/org.conductor.blockchain.RealizarCompra'
#             )
#             for i in range(20)
#         ]
#         for response in await asyncio.gather(*futures):
#             pass


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

def realizar_compras(id):
    dt = str(datetime.utcnow().isoformat()) 
    payload = {
        '$class': 'org.conductor.blockchain.RealizarCompra',
        'cartao': 'resource:org.conductor.blockchain.CartaoCredito#6666666666666666',
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
for i in range(20):
    arr_t.append(Thread(target=realizar_compras,args=[i]))

for i in range(20):
    arr_t[i].start()
