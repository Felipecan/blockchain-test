## Repositório destinado aos scripts de testes - Conductor Lab

### Configurando e instalando as dependências necessárias para executar os scripts:

Instale o [minconda3](https://conda.io/en/latest/miniconda.html) de acordo com o seu sistema.

Clone o repositório atual, nele ira conter o arquivo [cdtlab-env.yml](cdtlab-env.yml), que descreve as configurações de ambiente que será usada.

No terminal, dê o seguinte comando para criar o ambiente:

```sh
$ conda env create --file cdtlab-env.yml
```

Após a criado o ambiente, para ativá-lo use o comando no terminal do Linux:
```sh
$ source activate cdtlab-env
```
Para Windows:
```sh
$ activate cdtlab-env
```

### Execução dos sripts

Existe dois arquivos importantes na pasta: 
- [Blockchain.py](Blockchain.py): classe responsável por lidar com as funções que acessam a blockchain e assim testá-la. Serve de apoio para os scripts de teste. 
- [register_ihc.py](register_ihc.py): realiza cadastros de encargos, regras, emissor(es), portadores, cartões e realiza as compras. O script em questão faz todo o teste da blockchain de uma vez e por fim, gera um relatório em PDF e um log de tudo que aconteceu durate o teste.

Para executar os testes de fato:

[**arquivo .csv contendo as pessoas para popular a blockchain**](https://drive.google.com/file/d/1yrQv9hopJK63oVTV2QMF1OHISb81AtXB/view?usp=sharing)

```sh
$ python register_ihc.py -csv caminho/para/csv --inicio inicio_csv --quantidade n_de_cartoes_desejado
```

Mais informações das funções acima:

```sh
$ python register_ihc.py -h
```

ou


```sh
$ python
>> import Blockchain
>> help(Blockchain) 
```



Para desativar o ambiente virtual:
```sh
$ source deactivate
```
Ou no Windows:
```sh
$ deactivate
```
Obs: Os scripts, mesmo que funcionais, ainda estão sendo aprimorados para um melhor aproveitamento geral. Também vale ressaltar que este tutorial vai ser atualizado conforme essas alterações, acrescentando mais informações que ainda não foram inclusas.