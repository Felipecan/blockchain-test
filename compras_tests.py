# -*- coding: utf-8 -*-
'''
    Testando o teste.
'''
import time
import timeit
import asyncio
import threading
import argparse
import blockchain_tests

parser = argparse.ArgumentParser(description='Script para popular a Blockchain')
parser.add_argument('-n', action='store', type=int, dest='n', default='200', required=False, help='Quantidade de compras.')
arguments = parser.parse_args()

all_cards = blockchain_tests.get_all_cards()
cards = all_cards[:arguments.n]
print('len cards ',len(cards))
# blockchain_tests.cadastrar_emissor('Renner')
# cpfs = blockchain_tests.criar_portadores(50)
# cards = blockchain_tests.criar_cartoes(cpfs)

i = timeit.default_timer()
blockchain_tests.realizar_compras(cards, i)
while(threading.activeCount() > 1):
        pass
f = timeit.default_timer()
print('fim: ', f - i)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(blockchain_tests.realizar_compras(cards))
