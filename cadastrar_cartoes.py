# -*- coding: utf-8 -*-
'''
    Testando o teste.

    Teste:
    - 3 máquinas:
    	* 1 peer, 1 ordenador, 1 couchdb em cada
    - Emissor criado: Renner
    - Portadores criados: 200 portadores
    - Cartoes criados: 200 cartoes
    - 16m16.237s
    - Criação do bloco: 10 transações ou 2 segundos

'''
import time
import timeit
import asyncio
import argparse
import blockchain_tests

parser = argparse.ArgumentParser(description='Script para popular a Blockchain')

parser.add_argument('-csv', action='store', dest='csv_name', default='pessoas.csv', required=False, help='Nome/caminho do .csv com os dados para popular a Blockchain.')
parser.add_argument('-n', action='store', type=int, dest='n', default='10', required=False, help='Quantidade de pessoas para adicionar.')
arguments = parser.parse_args()

print ('Assumindo arquivo .csv como:',arguments.csv_name)
print ('Assumindo quantidade igual a:',arguments.n)

blockchain_tests.cadastrar_emissor('Renner')
cpfs = blockchain_tests.criar_portadores(arguments.n, arguments.csv_name)
cards = blockchain_tests.criar_cartoes(cpfs)