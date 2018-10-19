# -*- coding: utf-8 -*-
'''
    Testando o teste.
'''
import time
import timeit
import asyncio
import argparse
import threading
import blockchain_tests

parser = argparse.ArgumentParser(description='Script para realizar compras na Blockchain')
parser.add_argument('-n', action='store', type=int, dest='n', default='20', required=False, help='Quantidades de compras a se realizar.')
arguments = parser.parse_args()

all_cards = blockchain_tests.get_all_cards()

if arguments.n > len(all_cards):
    print("Quantidade maior que os cartões já cadastrados")
    exit(-1)
else:
    cards = all_cards[0:arguments.n]

i = timeit.default_timer()
blockchain_tests.realizar_compras(cards, i)
while(threading.activeCount() > 1):
        pass
f = timeit.default_timer()
print('fim: ', f - i)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(blockchain_tests.realizar_compras(cards))
