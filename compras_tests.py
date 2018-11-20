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
parser.add_argument('-qtd', action='store', type=int, dest='qtd', default='200', required=False, help='Quantidade de compras.')
arguments = parser.parse_args()

all_cards = blockchain_tests.get_all_cards()
cards = all_cards[:arguments.qtd]

# blockchain_tests.cadastrar_emissor('Renner')
# cpfs = blockchain_tests.criar_portadores(50)
# cards = blockchain_tests.criar_cartoes(cpfs)

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
logger.info('creating an instance of auxiliary_module.Auxiliary')

i = timeit.default_timer()
op = 3 #randint(1,3)
while True:
    i = timeit.default_timer()
    if op == 1:
        blockchain_tests.realizar_compras_1(cards)
    elif op == 2:
        blockchain_tests.realizar_compras_2(cards)
    elif op ==3:
        blockchain_tests.realizar_compras_3(cards)
    else:
        print('Error: OP out of range.')
    #time.sleep(15)

    f = timeit.default_timer()
    print('fim: ', f - i)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(blockchain_tests.realizar_compras(cards))
