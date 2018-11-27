# -*- coding: utf-8 -*-
import os
import time
import timeit
import asyncio
import logging
import argparse
import pandas as pd
import blockchain_tests as bt
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser(description='Script para popular a Blockchain')

parser.add_argument('-csv', action='store', dest='csv_name', default='pessoas.csv', required=False, help='Nome/caminho do .csv com os dados para popular a Blockchain.')
parser.add_argument('--inicio', action='store', type=int, dest='inicio', default='0', required=False, help='Ponto de onde deve iniciar o csv.')
parser.add_argument('--quantidade', action='store', type=int, dest='quantidade', default='10', required=False, help='Quantidade de pessoas para adicionar.')
arguments = parser.parse_args()

# print ('Arquivo .csv:',arguments.csv_name)
# print ('Ponto de início no csv igual a:',arguments.inicio)
# print ('Quantidade igual a:',arguments.quantidade)

logger = logging.getLogger('__main__')
logger.setLevel(logging.DEBUG)
if(arguments.inicio == 0):
    fh = logging.FileHandler('./logs/run.log', 'w')
else:
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

logger.info('Arquivo .csv: ' + str(arguments.csv_name))
logger.info('Ponto de início no csv: ' + str(arguments.inicio))
logger.info('Quantidade igual a: ' + str(arguments.quantidade))

i = timeit.default_timer()
logger.info('Iniciando cadastro de emissor(es)')
bt.cadastrar_emissor('Renner')
f = timeit.default_timer()
logger.info('Emissor cadastrado em: ' + str(f-i) + 's')

i = timeit.default_timer()
logger.info('Iniciando cadastro de portado(res)')
cpfs = bt.criar_portadores(arguments.csv_name, arguments.inicio, arguments.quantidade)
f = timeit.default_timer()
logger.info('Portadores cadastrados em: ' + str(f-i) + 's')

i = timeit.default_timer()
if(isinstance(cpfs, list)):
    logger.info('Iniciando cadastro de cartao(oes)')
    cards = bt.criar_cartoes(cpfs)
f = timeit.default_timer()
logger.info('Cartões cadastrados em: ' + str(f-i) + 's')

# plt.show()