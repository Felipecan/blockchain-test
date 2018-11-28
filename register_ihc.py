# -*- coding: utf-8 -*-
import os
import time
import timeit
import asyncio
import argparse
import matplotlib.pyplot as plt
from Blockchain import Blockchain

parser = argparse.ArgumentParser(description='Script para popular a Blockchain com emissor, portadores e cartões')

parser.add_argument('-csv', action='store', dest='csv_name', default='pessoas.csv', required=False, help='Nome/caminho do .csv com os dados para popular a Blockchain.')
parser.add_argument('--inicio', action='store', type=int, dest='inicio', default='0', required=False, help='Ponto de onde deve iniciar o csv.')
parser.add_argument('--quantidade', action='store', type=int, dest='quantidade', default='10', required=False, help='Quantidade de pessoas para adicionar.')
arguments = parser.parse_args()


bc = Blockchain()

bc.logger.info('Arquivo .csv: {}'.format(arguments.csv_name))
bc.logger.info('Ponto de início no csv: {}'.format(arguments.inicio))
bc.logger.info('Quantidade igual a: {}'.format(arguments.quantidade))


# if arguments.inicio == 0:
#     bc.cadastrar_encargos()
#     bc.cadastrar_regras()    
# else:
#     bc.logger.warning('Os encargos e regras já foram cadastrados?!')

# i = timeit.default_timer()
# bc.logger.info('Iniciando cadastro de emissor(es)')
# bc.cadastrar_emissor("Renner")
# f = timeit.default_timer()
# bc.logger.info('Emissor cadastrado em: {}s'.format(f-i))

i = timeit.default_timer()
bc.logger.info('Iniciando cadastro de portado(res)')
cpfs = bc.cadastrar_portadores(arguments.csv_name, arguments.inicio, arguments.quantidade)
f = timeit.default_timer()
bc.logger.info('Portadores cadastrados em: {}s'.format(f-i))
bc.gerar_grafico('portadores.csv')

i = timeit.default_timer()
if(isinstance(cpfs, list)):
    bc.logger.info('Iniciando cadastro de cartao(oes)')
    cards = bc.cadastrar_cartoes(cpfs)
    f = timeit.default_timer()
    bc.logger.info('Cartões cadastrados em: {}s'.format(f-i))        
    bc.gerar_grafico('cartoes.csv')

    bc.logger.info("Criando o relatório...")
    bc.criar_relatorio()
    bc.logger.info("Crianado(ou não)")
else:
    bc.logger.error('O retorno de cadastrar_portadores não é uma lista')

# if(isinstance(cards, list)):
#     bc.logger.info('Iniciando transacoes de compra...')
#     bc.logger.info('Quantidade de cartoes total: {}'.format(len(cards)))

#     q = 0
#     op = 1
#     for i in range(2):        
#         file_compras = open('comprasOP{}.csv'.format(op), 'w')
#         file_compras.write("quantidade;tempo;fracasso\n")
#         file_compras.write("0;0;0\n")
#         file_compras.flush()
#         file_compras.close()
#         for j in range(6):
#             #randint(1,3)
#             # q += 100
#             # cards = all_cards[:q]
#             bc.logger.info('OP selecionado: {}. Executando...'.format(op))
#             bc.logger.info('Quantidade de cartoes: {}'.format(q))
#             ti = timeit.default_timer()
#             if op == 1:
#                 bc.realizar_compras_1(cards)
#             elif op == 2:
#                 bc.realizar_compras_2(cards)
#             elif op ==3:
#                 bc.realizar_compras_3(cards)
#             else:
#                 bc.logger.error('Error: OP out of range.')
#             #time.sleep(15)
#             f = timeit.default_timer()
#             bc.logger.info('Transacoes realizadas em: {}s'.format(f-ti))
            
#             # bc.gerar_grafico('comprasOP{}.csv'.format(op))

#     bc.criar_relatorio()
# else:
#     bc.logger.error('O retorno de cadastrar_cartoes não é uma lista')
