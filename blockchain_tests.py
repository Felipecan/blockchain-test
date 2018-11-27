# -*- coding: utf-8 -*-
import json
import random
import timeit
import logging
import requests 
import pandas as pd 
from math import floor
from threading import Thread
from datetime import datetime
from unidecode import unidecode 
from reportlab.pdfgen import canvas
from concurrent.futures import ThreadPoolExecutor, wait 

# api_url = 'http://localhost:3000/api'
api_url = 'http://150.165.167.110/api'

logger = logging.getLogger('__main__.__blockchain_tests__')


def cadastrar_encargos():
    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "PAGOUTUDO",
        "taxa": 0,
        "expressaoSelecao": "totalPago >= totalFatura",
        "expressaoExecucao": " "
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("1 ", r.status_code)

    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "MINIMO",
        "taxa": 15,
        "expressaoSelecao": "totalPago >= totalFatura*taxa/100",
        "expressaoExecucao": " "
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("2 ", r.status_code)

    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "ROTATIVO",
        "taxa": 15.6,
        "expressaoSelecao": "totalPago >= totalFatura*taxa/100",
        "expressaoExecucao": "totalFatura += totalFatura*taxa/100"
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("3 ", r.status_code)

    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "PARCELAMENTO",
        "taxa": 10,
        "expressaoSelecao": "totalPago == (totalCompras + totalCompras*taxa/100)/4",
        "expressaoExecucao": "totalFatura = (totalFatura + totalFatura*taxa/100)/4"
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("4 ", r.status_code)

    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "EXTRA",
        "taxa": 0,
        "expressaoSelecao": "totalPago > totalFatura",
        "expressaoExecucao": " "
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("5 ", r.status_code)

    payload_encargo = {
        "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
        "nome": "INADIMPLENCIA",
        "taxa": 0,
        "expressaoSelecao": "totalPago == 0",
        "expressaoExecucao": " "
    }
    r = requests.post(api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload_encargo), headers={'content-type': 'application/json'})
    print("6 ", r.status_code)
    print("Fim...")

def cadastrar_regras():
    encargos_json = requests.get(api_url + "/org.conductor.encargo.EncargoGenerico").json()
    # print(encargos_json)
    pagoutudoID = ''
    inadID = ''
    extraID = ''
    parcelamentoID = ''
    rotativoID = ''
    minimoID = ''
    for encargos in encargos_json:
        if(encargos["nome"] == "PAGOUTUDO"):
            pagoutudoID = encargos["encargoId"]
        if(encargos["nome"] == "EXTRA"):
            extraID = encargos["encargoId"]
        if(encargos["nome"] == "INADIMPLENCIA"):
            inadID = encargos["encargoId"]
        if(encargos["nome"] == "MINIMO"):
            minimoID = encargos["encargoId"]
        if(encargos["nome"] == "PARCELAMENTO"):
            parcelamentoID = encargos["encargoId"]
        if(encargos["nome"] == "ROTATIVO"):
            rotativoID = encargos["encargoId"]
            
    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 4,  
        "encargosDepende": [' '],
        "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID)],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})    
    print('1', r.status_code)

    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 4,  
        "encargosDepende": [' '],
        "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})    
    print('2', r.status_code)

    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 3,  
        "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
        "encargosBloqueia": [' '],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(extraID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})    
    print('3', r.status_code)

    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 3,  
        "encargosDepende": [' '],
        "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID),
                    "resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(minimoID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})    
    print('4', r.status_code)

    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 2,  
        "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#"  + str(minimoID)],
        "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(rotativoID)],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(parcelamentoID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})
    print('5', r.status_code)

    payload_regra = {
        "$class": "org.conductor.regra.CadastrarRegraGenerica",
        "prioridade": 1,
        "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(minimoID)],
        "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(parcelamentoID)],
        "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(rotativoID)]
    }
    print(payload_regra)
    r = requests.post(api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload_regra), headers={'content-type': 'application/json'})
    print('6', r.status_code)


def cadastrar_emissor(emissor):       
    emissores_json = requests.get(api_url + "/org.conductor.emissor.Emissor").json()        
    if(len(emissores_json) > 0):            
        emissores = []
        for em in emissores_json:
            emissores.append(em['emissorId'])
        if(not(emissor in emissores)):
            encargos_json = requests.get(api_url + "/org.conductor.encargo.EncargoGenerico").json()
            encargos = []
            for encargo in encargos_json:
                encargos.append("resource:org.conductor.encargo.EncargoGenerico#" + str(encargo["encargoId"]))
            payload_emissor = {
                '$class': 'org.conductor.emissor.CadastrarEmissor',
                'emissorId': emissor,
                'cnpj': str(random.randint(10000000000000, 99999999999999)),
                'encargoGenerico': encargos
            }
            r = requests.post(api_url + "/org.conductor.emissor.CadastrarEmissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})           
            logger.info('Emissor cadastrado: ' + emissor)
        else:
            logger.warning('Emissor ' + emissor + ' já cadastrado anteriormente.')
    else:
        encargos_json = requests.get(api_url + "/org.conductor.encargo.EncargoGenerico").json()
        encargos = []
        for encargo in encargos_json:
            encargos.append("resource:org.conductor.encargo.EncargoGenerico#" + str(encargo["encargoId"]))            
        payload_emissor = {
            '$class': 'org.conductor.emissor.CadastrarEmissor',
            'emissorId': emissor,
            'cnpj': str(random.randint(10000000000000, 99999999999999)),
            'encargoGenerico': encargos
        }
        r = requests.post(api_url + "/org.conductor.emissor.CadastrarEmissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})        
        logger.info('Emissor cadastrado: ' + emissor)   

def criar_portador(payload):
    r = requests.post(api_url + '/org.conductor.blockchain.CadastrarPortador', data=json.dumps(payload), headers={'content-type': 'application/json'})
    # ret = []
    # ret.append(r)
    # ret.append(payload)    
    # return ret
    
def criar_portadores(csv_name='', inicio=0, quantidade=20):
    '''
        Descrição:
            A função lê um arquvo csv e cria certa quantidade de portadores na Blockchain. 
            Por enquanto a função está limitada a criação de no máximo 200 portadores.

        Utilização:
            criar_portdores('caminho/para/arquivo/nome.csv', 0, 20)

        Parâmetros:
            csv_name:
                O parâmetro especifica o caminho/nome para o arquivo csv contendo as informações que serão inseridas na Blockchain. 
                ATENÇÃO: O arquivo deve conter, na sequência: nome, sobrenome e cpf.
            inicio:
                Parametro especifica o ponto inicial, no csv, de onde vai ser criado os portadores.
            quantidade:
                O parâmetro especifica a quantidade de portadores a ser criado.            

        Retorno:
            A funcao retorna uma lista com os CPFs inseridos na Blockchain.
    '''    
    try:
        csv_file = pd.read_csv(csv_name, sep='|', encoding='ISO-8859-1', low_memory=False)
    except IOError:
        logger.error('Não foi possivel ler o arquivo corretamente. Encerrando programa...')
        return 0    
    # len == 351749
    if (inicio+quantidade) > csv_file.__len__():
        logger.error('Quantidade maior que a capacidade do csv')
        return 0

    if inicio < 0:
        inicio = 0

    file_portadores = open('portadores.csv', 'w')
    file_portadores.write("quantidade;tempo\n")
    file_portadores.write("0;0\n")

    csv_file = csv_file.dropna(subset=['cpf', 'nome'])
    csv_file = csv_file.drop_duplicates(subset=['cpf'])

    cpfs = []
    payloads = []
    payload_portador = {
        '$class': 'org.conductor.portador.CadastrarPortador',
        'cpf': ' ',
        'nome': ' ',
        'sobrenome': ' ',
        'endereco': 'CI'
    }

    temp = 0
    total = quantidade
    time_beg = timeit.default_timer()
    for row in csv_file.itertuples():
        if quantidade == 0:
            break

        if temp < inicio:
            temp += 1
            time_beg = timeit.default_timer()
            continue

        cpf = row.cpf.replace('*', '0')
        nome = row.nome.split(' ')
        
        payload_portador['nome'] = unidecode(nome[0])
        payload_portador['cpf'] = cpf
        if len(nome) == 1:
            payload_portador['sobrenome'] = 'seminiguem'
        else:
            payload_portador['sobrenome'] = unidecode(nome[1])
        
        # cpfs.append(cpf)
        # payloads.append(payload_portador)
        quantidade -= 1
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        r = requests.post(api_url + '/org.conductor.portador.CadastrarPortador', data=json.dumps(payload_portador), headers={'content-type': 'application/json'})    
        if(r.status_code < 300 and r.status_code > 100):    
            logger.debug(str(total-quantidade) + '/' + str(total) + ' cadastrado. Portador: ' + payload_portador['nome'])
            cpfs.append(cpf)
        else:            
            logger.debug('Não foi possível cadastradar o portador: ' + payload_portador['nome'])
            logger.debug('Codigo de erro: ' + str(r.status_code) + '. ERRO: ' + str(r.json()['error']['message']))
        if(quantidade%10 == 0):
            time_end = timeit.default_timer()                
            file_portadores.write(str(total-quantidade)+";"+str(time_end-time_beg)+'\n')            
            time_beg = time_end
    
    # pool = ThreadPoolExecutor(floor(len(payloads)/2))
    # futures = []
    # for payload in payloads:
    #     futures.append(pool.submit(criar_portador, payload))
    
    # w = wait(futures, timeout=None)    
    # for response in futures:        
    #     ret = response.result(timeout=None)
    #     if(ret[0].status_code != 200):
    #         print('remove from cpfs')
    #         print(ret[1]['cpf'])
    #         cpfs.remove(ret[1]['cpf'])            

    ####### diretamente com Threads #######
    # list_t = []
    # for payload in payloads:
    #     list_t.append(Thread(target=criar_portador, args=[payload]))

    # for i in range(len(payloads)):
    #     list_t[i].start()

    # for i in range(len(cards)):
    #     list_t[i].join()

    logger.info(str(len(cpfs)) + ' portadores cadastrados de ' + str(total))
    file_portadores.flush()
    file_portadores.close()
    return cpfs

def criar_cartao(payload):    
    r = requests.post(api_url + '/org.conductor.blockchain.CadastrarCartao', data=json.dumps(payload), headers={'content-type': 'application/json'})
    # return
    # print(r.status_code)

def criar_cartoes(cpfs):
    '''
        Descrição:
            A função cria um cartão para cada CPF(portador) cadastrado previamente na Blockchain.

        Utilização:
            criar_cartoes(lista_cpfs)

        Parâmetros:
            cpfs:
                O parâmetro deve conter uma lista de strings contendo os CPFs que servem para vincular o cartão a um portador na Blockchain.

        Retorno:
            A função retorna uma lista contendo os números dos cartões que foram cadastrados na Blockchain. 
            ATENÇÃO: Essa lista contêm valores inteiros.
    '''  

    # verificar ainda se é uma lista
    if not cpfs: 
        logger.error('Lista de cpfs vazia. Encerrando programa...')
        return
       
    file_cartoes = open('cartoes.csv', 'w')
    file_cartoes.write("quantidade;tempo\n")
    file_cartoes.write("0;0\n")
    
    c = get_all_cards()
    if len(c) <= 0:
        cards = random.sample(range(1000, 3000), len(cpfs))
    else:
        random.seed()
        beg = random.randint(1, 50)
        end = random.randint(50, 75)
        random.seed()
        cards = random.sample(range(beg*3000, end*5000), len(cpfs))
    
    payloads = []
    payload_cartao = {
        '$class': 'org.conductor.cartaocredito.CadastrarCartao',        
        'portador': ' ',
        'numCartao': ' ',
        'estado': 'ATIVO',
        'limiteCreditoMaximo': 9999999,
        'senha': '1234',
        'cvv': '123',
        'bandeira': 'Visa',
        'diaVencimento': 31,
        'mesValidade': 12,
        'anoValidade': 2050
    }

    r = []
    time_beg = timeit.default_timer()
    for i in range(len(cpfs)):       
        payload_cartao['portador'] = 'resource:org.conductor.portador.Portador#'+cpfs[i]
        payload_cartao['numCartao'] = str(cards[i])
        # payloads.append(payload_cartao)
        # a linha abaixo deve ser comentada ao ser possível usar threads ou algo semelhante
        r.append(requests.post(api_url + '/org.conductor.cartaocredito.CadastrarCartao', data=json.dumps(payload_cartao), headers={'content-type': 'application/json'}))
        if((i+1)%10 == 0):
            time_end = timeit.default_timer()
            file_cartoes.write(str(i+1)+";"+str(time_end-time_beg)+"\n") 
            time_beg = time_end  

    total = len(cards)
    for i in range(len(r)):
        if(r[i].status_code >= 300 and r[i].status_code <= 100):    
            logger.debug('Não foi possível cadastradar o cartao: ' + cards[i])
            logger.debug('Codigo de erro: ' + str(r[i].status_code) + '. ERRO: ' + str(r[i].json()['error']['message']))
            cards.remove(cards[i])
        else:
            logger.debug(str(total-(total-i)+1) + '/' + str(total) + ' cadastrado. Cartao: ' + str(cards[i]))                   
    
    # pool = ThreadPoolExecutor(floor(len(payloads)/2))
    # futures = []
    # for payload in payloads:
    #     futures.append(pool.org.conductor.blockchain.Portador

    # w = wait(futures, timeouorg.conductor.blockchain.Portador
    # for response in futures:org.conductor.blockchain.Portador
    #     print(response.result(timeout=0))

    ####### diretamente com Threads #######
    # list_t = []
    # for payload in payloads:
    #     list_t.append(Thread(target=criar_cartao, args=[payload]))

    # for i in range(len(payloads)):
    #     list_t[i].start()

    # for i in range(len(payloads)):
    #     list_t[i].join()

    logger.info(str(len(cards)) + ' cartoes cadastrados de ' + str(total))  
    file_cartoes.flush()  
    file_cartoes.close()
    return cards

def realizar_compra(id, card):
    dt = str(datetime.utcnow().isoformat()) 
    valor = random.randint(20, 200)                        
    parcelas = str(random.randint(1, 6))    
    payload = []
    for i in range(len(card)):
        payload.append({
            '$class': 'org.conductor.compra.RealizarCompra',
            'cartao': 'resource:org.conductor.cartaocredito.CartaoCredito#' + str(card[i]),
            'destino': 'boteco',
            'senha': '1234',
            'cvv': '123',
            'meio': 'ECOMMERCE',
            'mesValidade': 12,
            'anoValidade': 2050,
            'parcelas': str(parcelas),
            'valor': valor,
            'moeda': 'BRL',
            'data': dt
        })
    logger.debug('Thread id: ' + str(id) + '. Quantidade de cartoes: ' + str(len(card)))            
    # r = requests.post(api_url + '/RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})
    r = requests.post(api_url + '/org.conductor.compra.RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})    
    logger.debug('Thread id: ' + str(id) + ' finalizada. STATUS_CODE: ' + str(r.status_code))
    return r.status_code

def realizar_compras_1(cards):  
    file_compras = open('comprasOP1.csv', 'a')     
    time_beg = timeit.default_timer()
    with ThreadPoolExecutor(max_workers=len(cards)) as executor:        
        logger.debug('Disparando ' + str(len(cards)) + ' threads')
        jobs=[]             
        for i in range(len(cards)):            
            job=executor.submit(realizar_compra, i, cards[i:i+1])
            jobs.append(job)   

    wait(jobs, timeout=None)
    time_end = timeit.default_timer()

    success = 0
    failure = 0
    for response in jobs:        
        if(response.result(timeout=None) >= 300 and response.result(timeout=None) <= 100):   
            failure += 1
        else:
            success += 1

    file_compras.write(str(len(cards))+";"+str(time_end-time_beg)+";"+str(failure)+"\n")
    file_compras.flush()  
    file_compras.close()
    logger.info(str(success) + ' foram realizadas com sucesso - ' + str(failure) + ' falharam.')
    logger.debug('Finalizando execucao da OP1...')


def realizar_compras_2(cards):
    file_compras = open('comprasOP2.csv', 'a')
    time_beg = timeit.default_timer()
    with ThreadPoolExecutor(max_workers=10) as executor:
        logger.debug('Disparando ' + str(10) + ' threads')
        jobs=[]
        q_cards = len(cards)/10
        c = cards
        tx = 0
        for i in range(10):
            j = random.randint(1,q_cards)
            tx += j
            job=executor.submit(realizar_compra, i, c[0:j])
            c = c[j:]
            jobs.append(job)            
	
    wait(jobs, timeout=None)
    time_end = timeit.default_timer()

    success = 0
    failure = 0
    for response in jobs:
        if(response.result(timeout=None) >= 300 and response.result(timeout=None) <= 100):   
            failure += 1
        else:
            success += 1

    file_compras.write(str(tx)+";"+str(time_end-time_beg)+";"+str(failure)+"\n")
    file_compras.flush()  
    file_compras.close()
    logger.info(str(success) + ' foram realizadas com sucesso - ' + str(failure) + ' falharam.')
    logger.debug('Finalizando execucao da OP2...')


def realizar_compras_3(cards):
    with ThreadPoolExecutor(max_workers=10) as executor:
        logger.debug('Disparando ' + str(10) + ' threads')
        jobs=[]
        q_cards = len(cards)/10
        index = 0        
        for i in range(10):            
            job=executor.submit(realizar_compra, i, cards[index:index+q_cards])
            jobs.append(job)
            index += 20            
	
    wait(jobs, timeout=None)
    success = 0
    failure = 0
    for response in jobs:
        if(response.result(timeout=None) >= 300 and response.result(timeout=None) <= 100):   
            failure += 1
        else:
            success += 1
    logger.info(str(success) + ' foram realizadas com sucesso - ' + str(failure) + ' falharam.')
    logger.debug('Finalizando execucao da OP3...')


def realizar_compras_4(cards):
    w = int(len(cards)/20)
    with ThreadPoolExecutor(max_workers=w) as executor:
        logger.debug('Disparando ' + str(w) + ' threads')
        jobs=[]
        q_cards = w
        c = cards
        for i in range(w):
            j = random.randint(1,q_cards)
            job=executor.submit(realizar_compra, i, c[0:j])
            c = c[j:]
            jobs.append(job)
	
    wait(jobs, timeout=None)
    success = 0
    failure = 0
    for response in jobs:
        if(response.result(timeout=None) >= 300 and response.result(timeout=None) <= 100):   
            failure += 1
        else:
            success += 1
    logger.info(str(success) + ' foram realizadas com sucesso - ' + str(failure) + ' falharam.')
    logger.debug('Finalizando execucao da OP4...')


################## auxiliares ##################
def get_all_cards():
    '''
        Descrição:
            A função acessa a API e retorna todos os cartões cadastrados.

        Utilização:
            get_all_cards()

        Retorno:
            Retorna uma lista de strings com todos os cartões cadastrados.
    '''  
    cards = []
    r = requests.get(api_url + '/org.conductor.cartaocredito.CartaoCredito')
    jsons = r.json()        
    for json in jsons:        
        cards.append(json['numeroCartao'])
        # cards.append(json['limiteDisponivel'])
    return cards    

def get_all_compras():
    r = requests.get(api_url + '/org.conductor.compra.Compra')
    jsons = r.json()
    return jsons

def get_all_portadores():
    r = requests.get(api_url + '/org.conductor.portador.Portador')
    jsons = r.json()
    return jsons  

def gerar_grafico(csv_name):
    csv = pd.read_csv(csv_name, sep=';', encoding='ISO-8859-1')
    xticks = ['' for _ in range(len(csv.index))]
    v = 50
    xticks[0] = '0'
    for i in range(1, len(xticks)):
        if(i%5 == 0):
            xticks[i] = str(v)
            v += 50
    ax = csv.plot.bar(x='quantidade', y='tempo', rot=0, color="blue", alpha=0.7, width=0.4, legend=False)
    ax.set_ylim(21, 25)
    ax.set_xticklabels(xticks)
    # ajeitar o csv_name para pegar somente o nome portadores e fazer os labels corretamente.
    ax.set_label("Cadastro de portadores")
    ax.set_xlabel("Quantidade de transações para cadastro de portadores")
    ax.set_ylabel("Tempo gasto em segundos")
    plt.draw()

def criar_relatorio():

    #media
    #import statistics
    #statistics.mean()
    #moda
    #statistics.mode()
    #desvio padrão
    #vetor.std()

    try:
        nome_pdf = "RELATORIO" #input('Informe o nome do PDF: ')
        pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
        pdf.setTitle(nome_pdf)

        maquinas = 0
        orderes = 0
        peers = 0
        cas = 0
        kafkas = 0
        zookeeper = 0
        couchdb = 0
        qtd_portador = 0
        qtd_cartao = 0
        qtd_compra = 0

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(150, 760, 'Relatório de desempenho da blockchain')
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, 710, 'Especificações:')
        pdf.drawString(90, 690, '- ' + str(maquinas) + ' Máquinas com as seguintes configurações:')
        pdf.drawString(130, 670, '- CPU - Intel Core I5-6500 @ 3.20GHz x 4')
        pdf.drawString(130, 650, '- Memória RAM - 7.7 GiB')
        pdf.drawString(130, 630, '- Disco Rígido - 500 GB')
        pdf.drawString(130, 610, '- S.O. - Ubuntu 16.04 LTS')
        pdf.drawString(130, 590, '- Docker Version 17.06.2-ee.17, build 66834de')
        pdf.drawString(170, 570, '- Imagens Docker:')
        pdf.drawString(210, 550, '- hyperledger/fabric-peer:1.2.0')
        pdf.drawString(210, 530, '- hyperledger/fabric-orderer:1.2.0')
        pdf.drawString(210, 510, '- hyperledger/fabric-ca:1.2.0')
        pdf.drawString(210, 490, '- hyperledger/fabric-couchdb:0.4.14')
        pdf.drawString(210, 470, '- hyperledger/fabric-kafka:0.4.14')
        pdf.drawString(210, 450, '- hyperledger/fabric-zookeeper:0.4.14')
        pdf.drawString(170, 430, '- Containers:')
        pdf.drawString(210, 410, '- peers: ' + str(peers))
        pdf.drawString(210, 390, '- orderers: ' + str(orderes))
        pdf.drawString(210, 370, '- cas: ' + str(cas))
        pdf.drawString(210, 350, '- couchdb: ' + str(couchdb))
        pdf.drawString(210, 330, '- kafkas: ' + str(kafkas))
        pdf.drawString(210, 310, '- zookeepers: ' + str(zookeeper))
        pdf.drawString(50, 290, 'Casos de testes:')
        pdf.drawString(90, 270, 'Cadastro de portadores: ' + str(qtd_portador))
        pdf.drawString(90, 250, 'Cadastro de cartões: ' + str(qtd_cartao))
        pdf.drawString(90, 230, 'Transações de compras: ' + str(qtd_compra))
        pdf.showPage()

        #onde tiver xxx trocar por variavel correspondente

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(165, 760, 'TESTE – CADASTRAR_PORTADOR')
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, 710, 'Para o teste “CADASTRAR_PORTADOR” obtivemos as seguintes métricas:')
        pdf.drawString(90, 690, '- Foram cadastrado um total de xxx de xxx com um total de xxx falhas')
        pdf.drawString(90, 670, '- Tempo médio para cadastra de xxx em xxx portadores – xxx/s')
        pdf.drawString(90, 650, '- Taxa de Cadastros por segundos – xxx/s')
        pdf.drawString(90, 630, '- Desvio Padrão do tempo médio de  +/- xxx segundos')
        pdf.drawImage("portadores.png", 66, 100, width=640/1.3, height=480/1.3)

        pdf.showPage()

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(165, 760, 'TESTE – CADASTRAR_CARTÕES')
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, 710, 'Para o teste “CADASTRAR_CARTÕES” obtivemos as seguintes métricas:')
        pdf.drawString(90, 690, '- Foram cadastrado um total de xxx de xxx com um total de xxx falhas')
        pdf.drawString(90, 670, '- Tempo médio para cadastra de xxx em xxx cartões – xxx/s')
        pdf.drawString(90, 650, '- Taxa de Cadastros por segundos – xxx/s')
        pdf.drawString(90, 630, '- Desvio Padrão do tempo médio de  +/- xxx segundos')
        pdf.drawImage("cartoes.png", 66, 100, width=640/1.3, height=480/1.3)

        pdf.showPage()
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(nome_pdf))
    except:
        print('Erro ao gerar {}.pdf'.format(nome_pdf))

