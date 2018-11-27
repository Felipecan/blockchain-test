# -*- coding: utf-8 -*-
'''
    Testando o teste.
'''
import os
import time
import timeit
import asyncio
import logging
import threading
import argparse
import blockchain_tests
from random import randint

parser = argparse.ArgumentParser(description='Script para popular a Blockchain')
parser.add_argument('--quantidade', action='store', type=int, dest='quantidade', default='200', required=False, help='Quantidade de compras.')
arguments = parser.parse_args()

logger = logging.getLogger('__main__')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./logs/run.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter(fmt='%(asctime)s - [%(levelname)s] - [%(module)s.%(funcName)s:%(lineno)d] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
f = logging.Formatter()
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Quantidade de cartoes selecionada: ' + str(arguments.quantidade))

all_cards = blockchain_tests.get_all_cards()
cards = all_cards[:arguments.quantidade]

logger.info('Iniciando transacoes de compra...')

file_compras = open('compras.csv', 'w')
file_compras.write("quantidade;tempo;fracasso\n")
file_compras.write("0;0;0\n")
file_compras.flush()
file_compras.close()

q = 0
for i in range(6):
    op = 1 #randint(1,3)
    # q += 100
    # cards = all_cards[:q]
    logger.info('OP selecionado: ' + str(op) + '. Executando...')
    logger.info('Quantidade de cartoes: ' + str(q))
    i = timeit.default_timer()
    if op == 1:
        blockchain_tests.realizar_compras_1(cards)
    elif op == 2:
        blockchain_tests.realizar_compras_2(cards)
    elif op ==3:
        blockchain_tests.realizar_compras_3(cards)
    else:
        logger.error('Error: OP out of range.')
    #time.sleep(15)
    f = timeit.default_timer()
    logger.info('Transacoes realizadas em: ' + str(f-i) + 's')

