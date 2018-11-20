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
import logging
import argparse
import blockchain_tests as bt

parser = argparse.ArgumentParser(description='Script para popular a Blockchain')

parser.add_argument('-csv', action='store', dest='csv_name', default='pessoas.csv', required=False, help='Nome/caminho do .csv com os dados para popular a Blockchain.')
parser.add_argument('-ini', action='store', type=int, dest='ini', default='0', required=False, help='Ponto de onde deve iniciar o csv.')
parser.add_argument('-qtd', action='store', type=int, dest='qtd', default='10', required=False, help='Quantidade de pessoas para adicionar.')
arguments = parser.parse_args()

print ('Assumindo arquivo .csv como:',arguments.csv_name)
print ('Assumindo o ponto de início no csv igual a:',arguments.ini)
print ('Assumindo quantidade igual a:',arguments.qtd)

bt.cadastrar_emissor('Renner')
cpfs = bt.criar_portadores(arguments.csv_name, arguments.ini, arguments.qtd)
cards = bt.criar_cartoes(cpfs)