# -*- coding: utf-8 -*-
import json
import math
import random
import timeit
import logging
import requests 
import statistics
import pandas as pd 
from threading import Thread
from datetime import datetime
import matplotlib.pyplot as plt
from unidecode import unidecode 
from reportlab.pdfgen import canvas
from concurrent.futures import ThreadPoolExecutor, wait 

class Blockchain:


    def __init__(self):

        self.api_url = "http://localhost:3000/api"
        # self.api_url = "http://150.165.167.110/api"           
        self.configure_logger() 
        self.dado_relatorio = {
            "portadores_cadastrados": 0,
            "cartoes_cadastrados": 0,
            "portadores_total": 0,
            "cartoes_total": 0,
            "portadores_erro_medio": [],
            "cartoes_erro_medio": []
        }             


    def cadastrar_encargo(self, payload):
        '''
            Descrição:
                O método cadastra um único encargo, que é passado no parâmetro(payload).
                Geralmente, o método é usado dentro de outro método mais generalista.

            Utilização:
                cadastrar_encargo(payload_encargo)

            Parâmetros:
                payload:
                    O parâmetro carrega as informações que vão ser enviadas no método para a blockchain.
        '''   
        
        r = requests.post(self.api_url + "/org.conductor.encargo.CadastrarEncargoGenerico", data=json.dumps(payload), headers={'content-type': 'application/json'})
        if(r.status_code >= 200 and r.status_code < 300):
            self.logger.debug('Encargo {} cadastrado'.format(payload['nome']))
        else:
            self.logger.error('Encargo {} não cadastrado'.format(payload['nome']))


    def cadastrar_encargos(self):
        '''
            Descrição:
                O método cadastra automáticamente todos os encargos necessários para o teste.
                Porém, se for necessário mais algum, o mesmo deverá ser acrescentado aqui.

            Utilização:
                cadastrar_encargos()          
        '''   

        self.logger.info('Cadastrando encargos...')
        # Esse primeiro encargo tem como nome "EMPTY", pois ele auxilia no tratamento das regras cujo encargo não exista (Não tem nada especificando), no momento do post.
        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "EMPTY",
            "taxa": 0,
            "expressaoSelecao": "totalPago >= totalFatura",
            "expressaoExecucao": " " # o valor " " para essa expressão vai indicar que é um valor nulo, no momento do post desse encargo.
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "PAGOUTUDO",
            "taxa": 0,
            "expressaoSelecao": "totalPago >= totalFatura",
            "expressaoExecucao": " "
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "MINIMO",
            "taxa": 15,
            "expressaoSelecao": "totalPago >= totalFatura*taxa/100",
            "expressaoExecucao": " "
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "ROTATIVO",
            "taxa": 15.6,
            "expressaoSelecao": "totalPago >= totalFatura*taxa/100",
            "expressaoExecucao": "totalFatura += totalFatura*taxa/100"
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "PARCELAMENTO",
            "taxa": 10,
            "expressaoSelecao": "totalPago == (totalCompras + totalCompras*taxa/100)/4",
            "expressaoExecucao": "totalFatura = (totalFatura + totalFatura*taxa/100)/4"
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "EXTRA",
            "taxa": 0,
            "expressaoSelecao": "totalPago > totalFatura",
            "expressaoExecucao": " "
        }
        self.cadastrar_encargo(payload_encargo)

        payload_encargo = {
            "$class": "org.conductor.encargo.CadastrarEncargoGenerico",
            "nome": "INADIMPLENCIA",
            "taxa": 0,
            "expressaoSelecao": "totalPago == 0",
            "expressaoExecucao": " "
        }
        self.cadastrar_encargo(payload_encargo)
        self.logger.info('Fim de cadastramento de encargos')


    def cadastrar_regra(self, payload):
        '''
            Descrição:
                O método cadastra somente uma regra por vez. De maneira geral, é utilizado dentro de outro método somente.

            Utilização:
                cadastrar_regra(payload)

            Parâmetros:
                payload:
                    Parâmetro contendo as informações da regra a ser salva.
        '''           
        
        r = requests.post(self.api_url + "/org.conductor.regra.CadastrarRegraGenerica", data=json.dumps(payload), headers={'content-type': 'application/json'})    
        if(r.status_code >= 200 and r.status_code < 300):
            self.logger.debug('Regra cadastrada: {}'.format(payload))
        else:
            self.logger.error('Regra não cadastrada {}'.format(payload))


    def cadastrar_regras(self):
        '''
            Descrição:
                O método cadastra todas as regras necessárias para o teste. Basicamente associa os encargos.
                Caso seja necessário adicionar uma nova regra, deve ser criada aqui dentro.

            Utilização:
                cadastrar_regras()            
        '''   

        self.logger.info('Iniciando cadastramento das regras...')
        self.logger.info('GET nos encargos genéricos...')

        # Busca na blockchain os encargos que vão ser associados as regras. Em seguida salva seus IDs para serem inseridos no payload.
        # Obs: Se duas regras forem adicionadas com o mesmo nome, não se sabe ainda como vai ser quando for pegar seus IDs. rsrs
        encargos_json = requests.get(self.api_url + "/org.conductor.encargo.EncargoGenerico").json()    
        pagoutudoID = ''
        inadID = ''
        extraID = ''
        parcelamentoID = ''
        rotativoID = ''
        minimoID = ''
        emptyID = ''
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
            if(encargos["nome"] == "EMPTY"):
                emptyID = encargos["encargoId"]
        
        self.logger.info('Cadastrando regras...')            
        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 4,  
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(emptyID)], # eesse é um encargo espcial, pois indica que ele deve ser vazio na blockchain.
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)]
        }
        self.cadastrar_regra(payload_regra)    

        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 4,  
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(emptyID)],
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID)]
        }
        self.cadastrar_regra(payload_regra)    

        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 3,  
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(emptyID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(extraID)]
        }
        self.cadastrar_regra(payload_regra)    

        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 3,  
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(emptyID)],
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(inadID),
                        "resource:org.conductor.encargo.EncargoGenerico#" + str(pagoutudoID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(minimoID)]
        }
        self.cadastrar_regra(payload_regra)    

        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 2,  
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#"  + str(minimoID)],
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(rotativoID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(parcelamentoID)]
        }
        self.cadastrar_regra(payload_regra)    

        payload_regra = {
            "$class": "org.conductor.regra.CadastrarRegraGenerica",
            "prioridade": 1,
            "encargosDepende": ["resource:org.conductor.encargo.EncargoGenerico#" + str(minimoID)],
            "encargosBloqueia": ["resource:org.conductor.encargo.EncargoGenerico#" + str(parcelamentoID)],
            "encargosExecutar": ["resource:org.conductor.encargo.EncargoGenerico#" + str(rotativoID)]
        }
        self.cadastrar_regra(payload_regra)    
        self.logger.info('Fim de cadastramento das regras...')


    def cadastrar_emissor(self, emissor):
        '''
            Descrição:
                O método cadastra um único emissor por vez. Esse método é único e só usado ele mesmo (Não como auxiliar de outros métodos).

            Utilização:
                cadastrar_emissor(nome_emissor)

            Parâmetros:
                emissor:
                    O parâmetro deve conter o nome do emissor a ser cadastrado.
        '''   
        
        # Acessa a blockchain e busca todos os emissores já cadastrados lá. Em seguida verifica se de fato há algum emissor cadastrado.
        emissores_json = requests.get(self.api_url + "/org.conductor.emissor.Emissor").json()           
        if(len(emissores_json) > 0):            
            emissores = []
            for em in emissores_json:
                emissores.append(em['emissorId'])

            # Se já houve algum emissor cadastrado, verifica na lista de nomes do emissor (emissorId) se tem um emissor com o nome do emissor que vai ser cadastrado.
            if(not(emissor in emissores)):

                # Ao cadastrar um nome emissor, antes é preciso vincular os encargos a ele. Então busca-se na blockchain a lista e em seguida o coloca no payload.
                encargos_json = requests.get(self.api_url + "/org.conductor.encargo.EncargoGenerico").json()
                encargos = []
                for encargo in encargos_json:
                    encargos.append("resource:org.conductor.encargo.EncargoGenerico#" + str(encargo["encargoId"]))

                payload_emissor = {
                    '$class': 'org.conductor.emissor.CadastrarEmissor',
                    'emissorId': emissor,
                    'cnpj': str(random.randint(10000000000000, 99999999999999)),
                    'encargoGenerico': encargos
                }
                r = requests.post(self.api_url + "/org.conductor.emissor.CadastrarEmissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})           
                self.logger.info('Emissor cadastrado: {}'.format(emissor))
            else:
                self.logger.warning('Emissor {} já cadastrado anteriormente.'.format(emissor))
        else:
            # Cadastro do primeiro emissor da blockchain...
            encargos_json = requests.get(self.api_url + "/org.conductor.encargo.EncargoGenerico").json()
            encargos = []
            for encargo in encargos_json:
                encargos.append("resource:org.conductor.encargo.EncargoGenerico#" + str(encargo["encargoId"]))   

            payload_emissor = {
                '$class': 'org.conductor.emissor.CadastrarEmissor',
                'emissorId': emissor,
                'cnpj': str(random.randint(10000000000000, 99999999999999)),
                'encargoGenerico': encargos
            }
            r = requests.post(self.api_url + "/org.conductor.emissor.CadastrarEmissor", data=json.dumps(payload_emissor), headers={'content-type': 'application/json'})        
            self.logger.info('Emissor cadastrado: {}'.format(emissor))


    def cadastrar_portador(self, payload):    
        '''
            Descrição:
                O método cadastra um único portador na blockchain. Normalmente, utlizando dentro de outro método mais geral.

            Utilização:
                cadastrar_portador(payload)

            Parâmetros:
                payload:
                    Parâmetro contendo as informações do portadores a ser cadastrado na blockchain.

            Retorno:
                A funcao retorna a resposta do método request.post(...), contendo as informações sobre a requisição.
        '''   

        return requests.post(self.api_url + '/org.conductor.portador.CadastrarPortador', data=json.dumps(payload), headers={'content-type': 'application/json'})

        
    def cadastrar_portadores(self, csv_name='', inicio=0, quantidade=20):
        '''
            Descrição:
                A função lê um arquvo csv e cria certa quantidade de portadores na Blockchain. 
                Por enquanto a função está limitada a criação de no máximo 351749 portadores, de acordo com o csv sugerido.

            Utilização:
                cadastrar_portadores('caminho/para/arquivo/nome.csv', 0, 20)

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
            self.logger.error('Não foi possivel ler o arquivo[{}] corretamente. Encerrando programa...'.format(csv_file))
            return 0    
        # len == 351749
        # verifica se a quantidade inserida de onde começar no csv e a quantidade a ser cadastrada não ultrapassa a quantidade de linhas no csv.
        if (inicio+quantidade) > csv_file.__len__():
            self.logger.error('Quantidade maior que a capacidade do csv')
            return 0
        
        if inicio < 0:
            self.logger.warning('Variável início menor que zero. Mudando para valor igual 0.')
            inicio = 0
        
        # exclui linhas no csv onde tenham cpf e nome invalidos, assim como cpsf duplicados.
        csv_file = csv_file.dropna(subset=['cpf', 'nome'])
        csv_file = csv_file.drop_duplicates(subset=['cpf'])

        file_portadores = open('portadores.csv', 'w')
        file_portadores.write("quantidade;tempo\n")
        file_portadores.write("0;0\n")

        cpfs = []    
        payload_portador = {
            '$class': 'org.conductor.portador.CadastrarPortador',
            'cpf': ' ',
            'nome': ' ',
            'sobrenome': ' ',
            'endereco': 'CI'
        }

        temp = 0 # Auxiliar que controla quando vai começar a ler o csv de fato.
        total = quantidade
        time_beg = timeit.default_timer() # variável que captura o início do tempo para cada 10 portador cadastrado.
        for row in csv_file.itertuples():
            time_ii = timeit.default_timer() # A variável usada somente no log, serve pra calcular o tempo para cada portador com erro.

            # Se a quantidade zerar, é porque já tentou adicionar a quantidade de portadores pedido.
            if quantidade == 0:
                break
            
            # Controle de onde deve começar a cadastrar os portadores, até que temp seja igual a inicio, o csv só pula as linhas.
            if temp < inicio:
                temp += 1
                time_beg = timeit.default_timer()
                continue

            # muda o valor * do cpf para zero e separa a string com o nome completo em duas.
            cpf = row.cpf.replace('*', '0')
            nome = row.nome.split(' ')
            
            # carrega o payload com os dados atuais...
            payload_portador['nome'] = unidecode(nome[0])
            payload_portador['cpf'] = cpf
            if len(nome) == 1:
                payload_portador['sobrenome'] = 'seminiguem'
            else:
                payload_portador['sobrenome'] = unidecode(nome[1])
            
            r = self.cadastrar_portador(payload_portador)
            quantidade -= 1

            if(r.status_code >= 200 and r.status_code < 300):                
                self.logger.debug('{}/{} cadastrado. Portador: {}'.format((total-quantidade), total, payload_portador['nome']))
                cpfs.append(cpf)
                self.dado_relatorio["portadores_cadastrados"] += 1
            else:   
                self.dado_relatorio["portadores_erro_medio"].append(timeit.default_timer()-time_ii)         
                self.logger.debug('Não foi possível cadastradar o portador: {}'.format(payload_portador['nome']))            
                self.logger.debug('Codigo de erro: {}. ERRO: {}'.format(r.status_code, r.json()['error']['message']))
            
            # Aqui é feito a escrita no csv para o gráficos e afins... Vale salientar que é escrito a cada 10 cadastro.            
            if(quantidade%10 == 0):
                time_end = timeit.default_timer() # Tempo do último décimo portador cadastrado.               
                file_portadores.write(str(total-quantidade)+";"+str(time_end-time_beg)+'\n')            
                # atualiza o tempo inicial para os próximos 10       
                time_beg = time_end 

        self.dado_relatorio["portadores_total"] = total
        self.logger.info('{} portadores cadastrados de {}'.format(len(cpfs), total))
        file_portadores.flush()
        file_portadores.close()
        return cpfs


    def cadastrar_cartao(self, payload):  
        '''
            Descrição:
                O método cadastra somente um cartão para o o usuário em questão. É usada principalmente dentro do método mais geral de cadastro.

            Utilização:
                cadastrar_cartoes(payload_card)

            Parâmetros:
                payload:
                    O parâmetro deve conter as informções para cadastrar um cartão na Blockchain.

            Retorno:
                O método retorna a resposta do request.post(...).
        '''    

        return requests.post(self.api_url + '/org.conductor.cartaocredito.CadastrarCartao', data=json.dumps(payload), headers={'content-type': 'application/json'})    

    def cadastrar_cartoes(self, cpfs):
        '''
            Descrição:
                A função cria um cartão para cada CPF(portador) cadastrado previamente na Blockchain.

            Utilização:
                cadastrar_cartoes(lista_cpfs)

            Parâmetros:
                cpfs:
                    O parâmetro deve conter uma lista de strings contendo os CPFs que servem para vincular o cartão a um portador na Blockchain.

            Retorno:
                A função retorna uma lista contendo os números dos cartões que foram cadastrados na Blockchain. 
                ATENÇÃO: Essa lista contêm valores inteiros.
        '''  

        # verificar ainda se é uma lista
        if not cpfs: 
            self.logger.error('Lista de cpfs vazia. Encerrando programa...')
            return
        
        file_cartoes = open('cartoes.csv', 'w')
        file_cartoes.write("quantidade;tempo\n")
        file_cartoes.write("0;0\n")
        
        # Busca na blockchain os cartões já cadastrados, se não houve, cria simplesmente a quantidade de cartões aletórios.
        # Caso já tenha cartões, é feito uma tentativa de embaralhar mais os números e criar cartões únicos.
        c = self.get_cards()
        if len(c) <= 0:
            cards = random.sample(range(1000, 3000), len(cpfs))
        else:
            random.seed()
            beg = random.randint(1, 50)
            end = random.randint(50, 75)
            random.seed()
            cards = random.sample(range(beg*3000, end*5000), len(cpfs))
            
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

        crs = [] # A lista vai conter ao final todos os cards cadastrados de fato na blockchain.
        time_beg = timeit.default_timer()
        for i in range(len(cpfs)):   
            time_ii = timeit.default_timer() # A variável usada somente no log, serve pra calcular o tempo para cada portador com erro.

            payload_cartao['portador'] = 'resource:org.conductor.portador.Portador#'+cpfs[i]
            payload_cartao['numCartao'] = str(cards[i])

            r = self.cadastrar_cartao(payload_cartao)            
            if(r.status_code >= 200 and r.status_code < 300):  
                crs.append(cards[i]) # caso tenha sido adicionado com sucesso, insere na lista final o cartão em questão.
                self.logger.debug('{}/{} cadastrado. Cartao: {}'.format(len(crs), len(cards), cards[i]))  
                self.dado_relatorio["cartoes_cadastrados"] += 1                
            else:
                self.dado_relatorio["cartoes_erro_medio"].append(timeit.default_timer()-time_ii)   
                self.logger.debug('Não foi possível cadastradar o cartao: {}'.format(cards[i]))
                self.logger.debug('Codigo de erro: {}. ERRO: {}'.format(r.status_code, r.json()['error']['message']))                        
                
            # Aqui é feito a escrita no csv para o gráficos e afins... Vale salientar que é escrito a cada 10 cadastro. 
            if((i+1)%10 == 0):
                time_end = timeit.default_timer() 
                file_cartoes.write(str(i+1)+";"+str(time_end-time_beg)+"\n") 
                # atualiza o tempo incial, para o final atual.
                time_beg = time_end  
        
        self.dado_relatorio["cartoes_total"] = len(cards)
        self.logger.info('{} cartoes cadastrados de {}'.format(len(crs), len(cards)))  
        file_cartoes.flush()  
        file_cartoes.close()
        cards = crs
        return cards


    def realizar_compra(self, id, card):
        '''
            Descrição:
                O método simplesmente faz compras com determinado cartão.

            Utilização:
                cadastrar_portadores(0, card_number/list).

            Parâmetros:
                id:
                    Parâmetro que passa um id qualquer. Esse parâmetro serve somente pra visualisar melhor as threads lançadas.
                card:
                    Parametro deve conter o número do cartão ou uma lista de cartões em que vai ser feito uma compra, pois o restante das informações são padrão.
                
            Retorno:
                O método retorna a resposta do método request.post(...) da requisição.
        '''   

        dt = str(datetime.utcnow().isoformat()) 
        valor = random.randint(20, 200)                        
        parcelas = str(random.randint(1, 6))    
        payload = []

        # cria todos os payloads com os dados para cada cartão a ser feita a compra.
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
        self.logger.debug('Thread id: {}. Quantidade de cartoes: {}'.format(id, len(card)))                 
        r = requests.post(self.api_url + '/org.conductor.compra.RealizarCompra', data=json.dumps(payload), headers={"X-Access-Token":"jf8NmdLwG6DYDegnkZU81f2IMal9AUZ3O1wLvvUzvXbcx8RmfsujqP8bbsusCaAG","content-type": "application/json"})    
        self.logger.debug('Thread id: {} finalizada. STATUS_CODE: {}'.format(id, r.status_code))
        return r


    def realizar_compras_1(self, cards):  
        '''
            Descrição:
                O método realiza diversas compras paralelamente. 
                Por exemplo, caso tenha 100 cartões, o método dispara 100 threads com uma compra cada.

            Utilização:
                cadastrar_portadores(card_list).

            Parâmetros:                
                cards:
                    Parametro deve conter uma lista de cartões em que vai ser feito uma compra, pois o restante das informações são padrão.
        '''   

        file_compras = open('comprasOP1.csv', 'a')     
        time_beg = timeit.default_timer() # tempo inicial para fazer todas as compras.

        # Cria um pool de threas com a quantidade igual a quantidade de cartões passados na chamada do método.
        with ThreadPoolExecutor(max_workers=len(cards)) as executor:        
            self.logger.debug('Disparando {} threads'.format(len(cards)))
            jobs=[]                         
            for i in range(len(cards)):            
                # criando cada trabalho com o método de realizar compras e jogando no pool de threads para serem disparadas.
                job=executor.submit(self.realizar_compra, i, cards[i:i+1])
                jobs.append(job)   

        # Espera todas as threads terminarem e calcula o tempo final.
        wait(jobs, timeout=None)
        time_end = timeit.default_timer()

        success = 0
        failure = 0
        # de acordo com a respota, calcula a taxa de sucesso e falha.
        for response in jobs:        
            if(response.result(timeout=None).status_code >= 200 and response.result(timeout=None).status_code < 300):   
                success += 1
            else:
                failure += 1

        file_compras.write(str(len(cards))+";"+str(time_end-time_beg)+";"+str(failure)+"\n")
        file_compras.flush()  
        file_compras.close()
        self.logger.info('{} foram realizadas com sucesso - {} falharam.'.format(success, failure))
        self.logger.debug('Finalizando execucao da OP1...')


    def realizar_compras_2(self, cards):
        '''
            Descrição:
                O método realiza diversas compras paralelamente. 
                Por exemplo, caso tenha 100 cartões, o método dispara sempre 10 threads, porém com uma quantidade compra aleatória com base
                na quantidade de cartões. No caso de 100, será no máximo 10 cartões por thread.

            Utilização:
                cadastrar_portadores(card_list).

            Parâmetros:                
                cards:
                    Parametro deve conter uma lista de cartões em que vai ser feito uma compra, pois o restante das informações são padrão.
        '''   

        file_compras = open('comprasOP2.csv', 'a')
        time_beg = timeit.default_timer() # tempo inicial para fazer todas as compras.

        # Cria um pool de threas com a quantidade 10.
        with ThreadPoolExecutor(max_workers=10) as executor:
            self.logger.debug('Disparando {} threads'.format(10))
            jobs=[]
            q_cards = math.floor(len(cards)/10) # calcula a quantidade de cartões máximas para cada thread, com base na quantidade de cartões da chamada do método.
            c = cards
            tx = 0 # grava a quantidae de cartão para cada thread.
            for i in range(10):
                j = random.randint(1,q_cards) # escolhe um número aleatório para cada thread, onde o máximo é o q_cards.
                tx += j
                job=executor.submit(self.realizar_compra, i, c[0:j])
                c = c[j:] # atualiza os cards, de onde foi escolhido aleatoriamente, até o final.
                jobs.append(job)            
        
        # Espera todas as threads finalizarem para calcular o tempo..
        wait(jobs, timeout=None)
        time_end = timeit.default_timer()

        success = 0
        failure = 0
        # de acordo com a respota, calcula a taxa de sucesso e falha.
        for response in jobs:        
            if(response.result(timeout=None).status_code >= 200 and response.result(timeout=None).status_code < 300):   
                success += 1
            else:
                failure += 1

        file_compras.write(str(tx)+";"+str(time_end-time_beg)+";"+str(failure)+"\n")
        file_compras.flush()  
        file_compras.close()
        self.logger.info('{} foram realizadas com sucesso - {} falharam.'.format(success, failure))
        self.logger.debug('Finalizando execucao da OP2...')


    def realizar_compras_3(self, cards):
        file_compras = open('comprasOP3.csv', 'a')     
        time_beg = timeit.default_timer()
        with ThreadPoolExecutor(max_workers=len(cards)) as executor:        
            self.logger.debug('Disparando {} threads'.format(len(cards)))
            jobs=[]             
            for i in range(len(cards)):            
                job=executor.submit(self.realizar_compra, i, cards[i:i+1])
                jobs.append(job)   

        wait(jobs, timeout=None)
        time_end = timeit.default_timer()

        success = 0
        failure = 0
        for response in jobs:        
            if(response.result(timeout=None).status_code >= 200 and response.result(timeout=None).status_code < 300):   
                success += 1
            else:
                failure += 1

        file_compras.write(str(len(cards))+";"+str(time_end-time_beg)+";"+str(failure)+"\n")
        file_compras.flush()  
        file_compras.close()
        self.logger.info('{} foram realizadas com sucesso - {} falharam.'.format(success, failure))
        self.logger.debug('Finalizando execucao da OP3...')

        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     self.logger.debug('Disparando ' + str(10) + ' threads')
        #     jobs=[]
        #     q_cards = len(cards)/10
        #     index = 0        
        #     for i in range(10):            
        #         job=executor.submit(self.realizar_compra, i, cards[index:index+q_cards])
        #         jobs.append(job)
        #         index += 20            
        
        # wait(jobs, timeout=None)
        # success = 0
        # failure = 0
        # for response in jobs:
        #     if(response.result(timeout=None).status_code >= 300 and response.result(timeout=None).status_code <= 100):   
        #         failure += 1
        #     else:
        #         success += 1
        # self.logger.info('{} foram realizadas com sucesso - {} falharam.'.format(success, failure))
        # self.logger.debug('Finalizando execucao da OP3...')


    def realizar_compras_4(self, cards):
        w = int(len(cards)/20)
        with ThreadPoolExecutor(max_workers=w) as executor:
            self.logger.debug('Disparando ' + str(w) + ' threads')
            jobs=[]
            q_cards = w
            c = cards
            for i in range(w):
                j = random.randint(1,q_cards)
                job=executor.submit(self.realizar_compra, i, c[0:j])
                c = c[j:]
                jobs.append(job)
        
        wait(jobs, timeout=None)
        success = 0
        failure = 0
        for response in jobs:
            if(response.result(timeout=None).status_code >= 300 and response.result(timeout=None).status_code <= 100):   
                failure += 1
            else:
                success += 1
        self.logger.info('{} foram realizadas com sucesso - {} falharam.'.format(success, failure))
        self.logger.debug('Finalizando execucao da OP4...')


    ################## auxiliares ##################
    def configure_logger(self, logger_name='run.log'):
        '''
            Descrição:
                O método configura o log que será salvo ao final dos testes.

            Utilização:
                configure_logger("run.log").

            Parâmetros:                
                logger_name:
                    Parâmetro opcional de como será salvo o log.
        '''   

        self.logger = logging.getLogger('__main__')        
        self.logger.setLevel(logging.DEBUG)        
        fh = logging.FileHandler('./logs/run_{}.log'.format(datetime.today()), 'w')        
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter(fmt='%(asctime)s - [%(levelname)s] - [%(module)s.%(funcName)s:%(lineno)d] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        

    def get_cards(self):
        '''
            Descrição:
                A função acessa a API e retorna todos os cartões cadastrados.

            Utilização:
                get_cards()

            Retorno:
                Retorna uma lista de strings com todos os cartões cadastrados.
        '''  

        cards = []
        r = requests.get(self.api_url + '/org.conductor.cartaocredito.CartaoCredito')
        jsons = r.json()        
        for json in jsons:        
            cards.append(json['numeroCartao'])
            # cards.append(json['limiteDisponivel'])
        return cards    

    def get_compras(self):
        '''
            Descrição:
                A função acessa a API e retorna todos as comras realizadas.

            Utilização:
                get_compras()

            Retorno:
                Retorna uma lista com todos as compras em formato json.
        '''  

        r = requests.get(self.api_url + '/org.conductor.compra.Compra')
        jsons = r.json()
        return jsons

    def get_portadores(self):
        '''
            Descrição:
                A função acessa a API e retorna todos os poratadores cadastrados.

            Utilização:
                get_portadores()

            Retorno:
                Retorna uma lista com todos os portadores em formato json.
        '''  

        r = requests.get(self.api_url + '/org.conductor.portador.Portador')
        jsons = r.json()
        return jsons  

    def gerar_grafico_pc(self, csv_name):
        '''
            Descrição:
                Método auxiliar para gerar o gŕafico para portadores e cartões.

            Utilização:
                gerar_grafico_pc("portadores.csv")            
        '''  

        csv = pd.read_csv(csv_name, sep=';', encoding='ISO-8859-1')
        
        xticks = ['' for _ in range(len(csv.index))] # cria uma lista de acordo com a quantidade de linhas com valor ""
        v = 50
        xticks[0] = '0'
        for i in range(1, len(xticks)): # substituindo o valor '' a cada 50, onde no csv seria a cada 5 linha.
            if(i%5 == 0):
                xticks[i] = str(v)
                v += 50

        ax = csv.plot.bar(x='quantidade', y='tempo', rot=0, color="blue", alpha=0.7, width=0.4)
        m = csv["tempo"].mean()
        mx = csv["tempo"].max()
        ax.set_ylim(m-15.5, mx+10.5) # calcula e set o melhor espaço de valores plotado no gráfico.
        ax.set_xticklabels(xticks) 
        file_name, _ = csv_name.split('.')
        ax.set_title("Cadastro de {}".format(file_name))
        ax.set_xlabel("Quantidade de transações para cadastro{}".format(file_name))
        ax.set_ylabel("Tempo gasto em segundos")
        # plt.draw()
        plt.savefig('{}.png'.format(file_name))


    def gerar_grafico_c(self, csv_name):
        '''
            Descrição:
                Método auxiliar para gerar o gŕafico para as compras.

            Utilização:
                gerar_grafico_c("compras.csv")            
        '''  

        csv = pd.read_csv(csv_name, sep=';', encoding='ISO-8859-1')
        ax = csv.plot.bar(x='quantidade', y='tempo', rot=0, color="red", alpha=0.7, width=0.4)
        
        # cria uma lista de acordo com a quantidade de linhas com valor ""
        xticks = ['' for _ in range(len(csv.index))]
        yticks = ['' for _ in range(len(csv.index))]

        # preenche os pontos em y de acordo com o csv.
        y = '{:1.2f}'.format(csv["tempo"].ix[0])
        yticks[0] = y    
        for i in range(1, len(yticks)):        
            y = '{:1.2f}'.format(csv["tempo"].ix[i])
            yticks[i] = y            
        ax.set_yticklabels(yticks)

        # m = csv["tempo"].mean()
        # mx = csv["tempo"].max()
        
        # preenche os pontos em x de acordo com o csv.
        x = '{:1.0f}'.format(csv["quantidade"].ix[0])
        xticks[0] = x    
        for i in range(1, len(yticks)):        
            x = '{:1.0f}'.format(csv["quantidade"].ix[i])
            xticks[i] = x            
        ax.set_xticklabels(xticks)

        file_name, _ = csv_name.split('.')
        ax.set_title("Compras - {} - Total de compras {:1.0f}".format(file_name, csv["quantidade"].sum()))
        ax.set_xlabel("Quantidade de compras - {}".format(file_name))
        ax.set_ylabel("Tempo gasto em segundos")
        # plt.draw()
        plt.savefig('{}.png'.format(file_name))


    def criar_relatorio(self):
        '''
            Descrição:
                Método auxiliar para gerar o relatório final de testes.

            Utilização:
                criar_relatorio()            
        ''' 

        if(len(self.dado_relatorio["portadores_erro_medio"]) <= 0):
            portador_erro_media = 0
        else:    
            portador_erro_media = statistics.mean(self.dado_relatorio["portadores_erro_medio"])

        if(len(self.dado_relatorio["cartoes_erro_medio"]) <= 0):
            cartao_erro_media = 0
        else:    
            cartao_erro_media = statistics.mean(self.dado_relatorio["cartoes_erro_medio"])
        

        csv_portador = pd.read_csv('portadores.csv', sep=';', encoding='ISO-8859-1')
        csv_portador = csv_portador.drop(csv_portador.index[0])                
        media_tempo_portador = csv_portador["tempo"].mean()
        desvio_tempo_portador = csv_portador["tempo"].std()
        total_tempo_portador = csv_portador["tempo"].sum()        
        
        csv_cartao = pd.read_csv('cartoes.csv', sep=';', encoding='ISO-8859-1')
        csv_cartao = csv_cartao.drop(csv_cartao.index[0])                
        media_tempo_cartao = csv_cartao["tempo"].mean()
        desvio_tempo_cartao = csv_cartao["tempo"].std()
        total_tempo_cartao = csv_cartao["tempo"].sum()
        
        csv_comprasop1 = pd.read_csv('comprasOP1.csv', sep=';', encoding='ISO-8859-1')
        csv_comprasop1 = csv_comprasop1.drop(csv_comprasop1.index[0])
        tempo_medio_comprasop1 = csv_comprasop1["tempo"].mean()        
        media_comprasop1_segundo = csv_comprasop1["quantidade"].ix[1]/tempo_medio_comprasop1
        tempo_medio_total_comprasop1 = csv_comprasop1["quantidade"].sum()/csv_comprasop1["tempo"].sum()
        erro_total_comprasop1 = csv_comprasop1["fracasso"].sum()

        csv_comprasop2 = pd.read_csv('comprasOP2.csv', sep=';', encoding='ISO-8859-1')
        csv_comprasop2 = csv_comprasop2.drop(csv_comprasop2.index[0])
        tempo_medio_comprasop2 = csv_comprasop2["tempo"].mean()
        media_comprasop2 = csv_comprasop2["quantidade"].mean()        
        media_comprasop2_segundo = csv_comprasop2["quantidade"].mean()/tempo_medio_comprasop2
        tempo_medio_total_comprasop2 = csv_comprasop2["quantidade"].sum()/csv_comprasop2["tempo"].sum()
        erro_total_comprasop2 = csv_comprasop2["fracasso"].sum()

        try:
            nome_pdf = "./reports/relatorio_{}".format(datetime.today()) #input('Informe o nome do PDF: ')
            pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
            pdf.setTitle(nome_pdf)

            maquinas = 0
            orderes = 0
            peers = 0
            cas = 0
            kafkas = 0
            zookeeper = 0
            couchdb = 0
            qtd_portador = self.dado_relatorio["portadores_total"]
            qtd_cartao = self.dado_relatorio["cartoes_total"]
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
            pdf.drawString(50, 210, 'Aquivo log gerado: run_[...].log')
            pdf.showPage()

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(165, 760, 'TESTE – CADASTRAR PORTADOR')
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 710, 'Para o teste “CADASTRAR PORTADOR” foram obtidas as seguintes métricas:')
            pdf.drawString(60, 690, '- Cadastrado {} de um total de {} com {} falhas'.format(self.dado_relatorio["portadores_cadastrados"], self.dado_relatorio["portadores_total"], (self.dado_relatorio["portadores_total"]-self.dado_relatorio["portadores_cadastrados"])))
            pdf.drawString(60, 670, '- Tempo médio para cadastra de {} em {} portadores – Tx: {:1.3f} s'.format(10, 10, media_tempo_portador))
            pdf.drawString(60, 650, '- Tempo de Cadastros para 1 transação de um total de {} – Tx: {:1.3f} s'.format(10, media_tempo_portador/10))
            pdf.drawString(60, 630, '- Taxa de Cadastros por segundos para 1 transação de um total de {} - {:1.3f} s'.format(self.dado_relatorio["portadores_total"], total_tempo_portador/self.dado_relatorio["portadores_total"]))
            pdf.drawString(60, 610, '- Desvio Padrão dos tempos medidos foi de  +/-{:1.3f} segundos'.format(desvio_tempo_portador))
            pdf.drawString(60, 590, '- Tempo médio de uma transação com falhas - {:1.3f} segundos'.format(portador_erro_media))
            pdf.drawImage("portadores.png", 66, 100, width=640/1.3, height=480/1.3)
            pdf.showPage()

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(165, 760, 'TESTE – CADASTRAR CARTÕES')
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 710, 'Para o teste “CADASTRAR CARTÕES” foram obtidas as seguintes métricas:')
            pdf.drawString(60, 690, '- Cadastrado {} de um total de {} com {} falhas'.format(self.dado_relatorio["cartoes_cadastrados"], self.dado_relatorio["cartoes_total"], (self.dado_relatorio["cartoes_total"]-self.dado_relatorio["cartoes_cadastrados"])))
            pdf.drawString(60, 670, '- Tempo médio para cadastra de {} em {} cartões – Tx: {:1.3f} s'.format(10, 10, media_tempo_cartao))
            pdf.drawString(60, 650, '- Tempo de Cadastros para 1 transação de um total de {} – Tx: {:1.3f} s'.format(10, media_tempo_cartao/10))
            pdf.drawString(60, 630, '- Taxa de Cadastros por segundos para 1 transação de um total de {} - {:1.3f} s'.format(self.dado_relatorio["cartoes_total"], total_tempo_cartao/self.dado_relatorio["cartoes_total"]))
            pdf.drawString(60, 610, '- Desvio Padrão dos tempos medidos foi de  +/-{:1.3f} segundos'.format(desvio_tempo_cartao))
            pdf.drawString(60, 590, '- Tempo médio de uma transação com falhas - {:1.3f} segundos'.format(cartao_erro_media))
            pdf.drawImage("cartoes.png", 66, 100, width=640/1.3, height=480/1.3)
            pdf.showPage()

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(165, 760, 'TESTE – COMPRAS OP1')
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 710, 'Para o teste “COMPRAS OP1" foram obtidas as seguintes métricas:')
            pdf.drawString(60, 690, '- Total de compras: {:1.0f}. Compras realizadas: {:1.0f}. Total de falhas: {:1.0f}'.format(csv_comprasop1["quantidade"].sum(), csv_comprasop1["quantidade"].sum()-erro_total_comprasop1, erro_total_comprasop1))
            pdf.drawString(60, 670, '- Tempo médio de compras de {:1.0f} em {:1.0f} Transações – Tx: {:1.3f} s'.format(100, 100, tempo_medio_comprasop1))
            pdf.drawString(60, 650, '- Média de compras por segundo (De um total de 100): {:1.3f} s.'.format(media_comprasop1_segundo))
            pdf.drawString(60, 630, '- Média de compras por segundo (De um total de {}): {:1.3f} s.'.format(csv_comprasop1["quantidade"].sum(), tempo_medio_total_comprasop1))
            pdf.drawImage("comprasOP1.png", 66, 100, width=640/1.3, height=480/1.3)
            pdf.showPage()

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(165, 760, 'TESTE – COMPRAS OP2')
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 710, 'Para o teste “COMPRAS OP2" foram obtidas as seguintes métricas:')
            pdf.drawString(60, 690, '- Total de compras: {:1.0f}. Compras realizadas: {:1.0f}. Total de falhas: {:1.0f}'.format(csv_comprasop2["quantidade"].sum(), csv_comprasop2["quantidade"].sum()-erro_total_comprasop2, erro_total_comprasop2))
            pdf.drawString(60, 670, '- Tempo médio de compras de quantidade aleatoria: Transações - : {:1.3f} s'.format(tempo_medio_comprasop2))
            pdf.drawString(60, 650, '- Média de compras por segundo (De um total medio de {}): {:1.3f} s.'.format(media_comprasop2 ,media_comprasop2_segundo))
            pdf.drawString(60, 630, '- Média de compras por segundo (De um total de {}): {:1.3f} s.'.format(csv_comprasop2["quantidade"].sum(), tempo_medio_total_comprasop2))
            pdf.drawImage("comprasOP2.png", 66, 100, width=640/1.3, height=480/1.3)
            pdf.showPage()

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(165, 760, 'TESTE – COMPRAS OP3')
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 710, 'Para o teste “COMPRAS OP3" foram obtidas as seguintes métricas:')
            pdf.drawString(60, 690, '- Total de compras: {:1.0f}. Compras realizadas: {:1.0f}. Total de falhas: {:1.0f}'.format(csv_comprasop2["quantidade"].sum(), csv_comprasop2["quantidade"].sum()-erro_total_comprasop2, erro_total_comprasop2))
            pdf.drawString(60, 670, '- Tempo médio de compras de quantidade aleatoria: Transações - : {:1.3f} s'.format(tempo_medio_comprasop2))
            pdf.drawString(60, 650, '- Média de compras por segundo (De um total medio de {}): {:1.3f} s.'.format(media_comprasop2 ,media_comprasop2_segundo))
            pdf.drawString(60, 630, '- Média de compras por segundo (De um total de {}): {:1.3f} s.'.format(csv_comprasop2["quantidade"].sum(), tempo_medio_total_comprasop2))
            pdf.drawImage("comprasOP2.png", 66, 100, width=640/1.3, height=480/1.3)
            pdf.showPage()


            pdf.save()

            print('{}.pdf criado com sucesso!'.format(nome_pdf))
        except:
            print('Erro ao gerar {}.pdf'.format(nome_pdf))
    
    