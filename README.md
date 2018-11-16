## Repositório destinado aos scripts de testes - Conductor Lab

### Dependências necessárias para executar os scripts:

```sh
$ sudo apt-get install python3-pip
```
Dentro da pasta raiz do repositório clonado...

```sh
$ pip3 install -r requirements.txt
```

### Execução dos sripts

Existe dois scripts na pasta: 
- [cadastrar_cartoes.py](cadastrar_cartoes.py): realiza o cadastro de um emissor, cadastro de determinada quantidade de portadores e cartões. 
- [compras_tests.py](compras_tests.py): realiza determinada quantidade de compras a partir dos cartões previamente cadastrados.

Para executar os testes de fato:

[arquivo .csv contendo as pessoas para cadastrar](https://drive.google.com/file/d/1yrQv9hopJK63oVTV2QMF1OHISb81AtXB/view?usp=sharing)

```sh
$ python3 cadastrar_cartoes.py -csv caminho/para/csv -ini inicio_csv -qtd n_de_cartoes
$ python3 compras_tests.py -qtd n_de_compras
```

Mais informações das funções acima:

```sh
$ python3 cadastrar_cartoes.py -h
```

ou


```sh
$ python3 compras_tests.py -h
```

#### Alguns relatórios:
##### Teste Alterório
- 3 máquinas:
    - 1 peer, 1 ordenador, 1 couchdb em cada
    - Emissor criado: Renner
    - Portadores criados: 200 portadores
    - Cartoes criados: 200 cartoes
    - 16.237s
    - Criação do bloco: 10 transações ou 2 segundos

