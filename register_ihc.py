# -*- coding: utf-8 -*-
import os
import time
import timeit
import asyncio
import argparse
import matplotlib.pyplot as plt
from Blockchain import Blockchain

# criação e configuração dos argumentos de entrada do script. Ao iniciar, será carregada essas informações que podem ser passdas por linha de comando.
parser = argparse.ArgumentParser(description='Script para popular a Blockchain com emissor, portadores e cartões')
parser.add_argument('-csv', action='store', dest='csv_name', default='pessoas.csv', required=False, help='Nome/caminho do .csv com os dados para popular a Blockchain.')
parser.add_argument('--inicio', action='store', type=int, dest='inicio', default='0', required=False, help='Ponto de onde deve iniciar o csv.')
parser.add_argument('--quantidade', action='store', type=int, dest='quantidade', default='10', required=False, help='Quantidade de pessoas para adicionar.')
arguments = parser.parse_args()

# cria um obj do tipo Blockchain para fazer os testes e gerar os arquivos finais.
bc = Blockchain()

bc.logger.info('Arquivo .csv: {}'.format(arguments.csv_name))
bc.logger.info('Ponto de início no csv: {}'.format(arguments.inicio))
bc.logger.info('Quantidade igual a: {}'.format(arguments.quantidade))

# Por equanto, sempre que começar os testes, supõe-se que o valor de "inicio" seja 0.
# Assim, irá cadastrasr os encargos e regras.
# Deposi disso, o valor pode ser outro, pois as regras e encargos só precisam ser salvos uma única vez, no caso.
if arguments.inicio == 0:
    bc.cadastrar_encargos()
    bc.cadastrar_regras()    
else:
    bc.logger.warning('Os encargos e regras já foram cadastrados?!')

i = timeit.default_timer()
bc.logger.info('Iniciando cadastro de emissor(es)')
bc.cadastrar_emissor("Renner")
f = timeit.default_timer()
bc.logger.info('Emissor cadastrado em: {}s'.format(f-i))

i = timeit.default_timer()
bc.logger.info('Iniciando cadastro de portado(res)')
cpfs = bc.cadastrar_portadores(arguments.csv_name, arguments.inicio, arguments.quantidade)
f = timeit.default_timer()
bc.logger.info('Portadores cadastrados em: {}s'.format(f-i))
bc.gerar_grafico_pc('portadores.csv')

i = timeit.default_timer()
if(isinstance(cpfs, list)):
    bc.logger.info('Iniciando cadastro de cartao(oes)')
    cards = bc.cadastrar_cartoes(cpfs)
    f = timeit.default_timer()
    bc.logger.info('Cartões cadastrados em: {}s'.format(f-i))        
    bc.gerar_grafico_pc('cartoes.csv')
else:
    bc.logger.error('O retorno de cadastrar_portadores não é uma lista')

# no teste real, deve ser comentado.
# cards = bc.get_cards()
if(isinstance(cards, list)):
    bc.logger.info('Iniciando transacoes de compra...')
    bc.logger.info('Quantidade de cartoes total: {}'.format(len(cards)))

    op = 1 # variável contra o tipo de compra
    q = 50 # temp
    all_cards = cards
    for i in range(2):        
        file_compras = open('comprasOP{}.csv'.format(op), 'w')
        file_compras.write("quantidade;tempo;fracasso\n")
        file_compras.write("0;0;0\n")
        file_compras.flush()
        file_compras.close()

        for j in range(10):                                    
            bc.logger.info('OP selecionado: {}. Executando...'.format(op))
            bc.logger.info('Quantidade de cartoes: {}'.format(q))
            ti = timeit.default_timer()
            if op == 1:
                bc.realizar_compras_1(all_cards)                
            elif op == 2:
                bc.realizar_compras_2(all_cards)                
            elif op == 3:
                cards = all_cards[:q]
                bc.realizar_compras_3(cards)
                bc.gerar_grafico_c('comprasOP{}.csv'.format(op))
                bc.criar_relatorio()
                q += 50
            else:
                bc.logger.error('Error: OP out of range.')
            #time.sleep(15)
            f = timeit.default_timer()
            bc.logger.info('Transacoes realizadas em: {}s'.format(f-ti))

        bc.gerar_grafico_c('comprasOP{}.csv'.format(op))
        op += 1    

    bc.criar_relatorio()
else:
    bc.logger.error('O retorno de cadastrar_cartoes não é uma lista')
