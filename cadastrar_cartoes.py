# -*- coding: utf-8 -*-
'''
    Testando o teste.
'''
import time
import timeit
import asyncio
import blockchain_tests

blockchain_tests.cadastrar_emissor('Renner')
cpfs = blockchain_tests.criar_portadores(200)
cards = blockchain_tests.criar_cartoes(cpfs)