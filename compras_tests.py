# -*- coding: utf-8 -*-
'''
    Testando o teste.
'''
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
fh.setLevel(logging.INFO)
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
while True:
    op = 1 #randint(1,3)
    logger.info('OP selecionado: ' + str(op) + '. Executando...')
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

