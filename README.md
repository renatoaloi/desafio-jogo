# Desafio Banco Imobiliário

## Objetivo

Desenvolver um jogo, conforme as regras abaixo determinadas, imitando um jogo de tabuleiro, conhecido, chamado Banco Imobiliário.

A ideia é fazer um estudo comportamental de jogadores, analisando a quantidade de vitórias, definindo um modelo estatístico baseado em perfil de compra dos jogadores.

O resultado final é um programa de linha de comando que executa em um container Docker. Um orquestrador levanta 300 instâncias e os resultados são registrados em uma API REST de relatório do jogo, exibindo resultados solicitados pelo desafio. Veja um exemplo de saída, mais abaixo.

## Guia de Início Rápido

Para utilizar o sistema, primeiro levante a API Flask, que é responsável pelo push-notification dos containers e também por extrair os dados de saída do projeto.

```
> virtualenv env
> $env:FLASK_APP="api/app.py"
> ...
> python -m flask run --host=0.0.0.0
```

Antes de compilar o container do jogo, precisamos configurar o arquivo ```app.py``` perto da linha 40:

```
...
r = requests.post(
    "http://**ip_do_seu_pc**:5000/jogo/resultado", 
    json=jogo.serialize
)
...
```

Onde: ``` **ip_do_seu_pc** ``` é o ip do host rodando a API Flask, no caso, rodei na minha máquina, mas pode ser um ECS, um EC2, etc.

> OBS: Desde que o container rodando o jogo tenha acesso a internet, para testes em desenvolvimento. Para uma implementação em produção precisaria fechar os dois serviços em uma subnet, fechada, sem acesso a internet, por segurança.

Depois então comece a prepara o container, compilando ele:

```
> docker build -t jogo .
```

Então você já pode levantar as 300 instâncias do jogo, utilizando o comando abaixo:

```
> docker-compose up --scale jogo=300
```

> TODO: Criar script de terraform para cloud

Não se esqueça ao final de derrubar todos os containers.

```
> docker-compose down
```

A execução dos containers rodando o jogo deve demorar por volta de 1 hora, após isso basta acessar a API para extrair o relatório, no formato JSON:

```
http://localhost:5000/jogo/relatorio
```

## Exemplo de Relatório de Saída

```json
{
    "msg": "Relatório de partidas",
    "object": {
        "comportamento_vencedor": "cauteloso",
        "comportamentos": [
            {
                "impulsivo": "24.33"
            },
            {
                "exigente": "20.67"
            },
            {
                "cauteloso": "35.00"
            },
            {
                "aleatório": "20.00"
            }
        ],
        "media_turnos": 891.98,
        "partidas_por_timeout": 263,
        "partidas_totais": 300
    }
}
```

## Requisitos Técnicos

- O jogo é composto de partidas
- As partidas são compostas de rodadas dos jogadores
- Os jogadores possuem uma conta em que podem receber e retirar saldo
- Uma partida começa definindo uma ordem aleatória para os jogadores jogarem
- Cada jogador na primeira rodada recebe 300 de saldo
- O jogo possue 20 propriedades em sequencia
- Cada jogador na ordem estabelecida joga um dado de 6 faces equiprovável, se "movimentando" o número obtido no dado pelas 20 propriedades, em sequencia
- Ao "cair" em uma propriedade, o jogador:
    - Pode comprar se não tiver proprietário
    - Deve pagar aluguel se já tiver proprietário
- Cada vez que o jogador atravessa as 20 propriedades, ele volta pra primeira e recebe 100 de saldo
- O jogador com saldo negativo perde e sai do jogo
    - As propriedades do jogador perdedor podem ser compradas por outros jogadores, quando cairem na propriedade
- O jogo termina quando:
    - Restar apenas 1 jogador com saldo positivo
    - Ou, quando passarem 1000 rodadas sem que aconteça a regra acima, ganha quem tiver o maior saldo, sendo o desempate a ordem inicial de jogar.

## Regras de comportamento

Os jogadores possuem características, sendo:

- impulsivo: compra toda propriedade que "cair", se estiver disponível para venda e tiver saldo
- exigente: só compra a propriedade que "cair", se estiver disponível para venda, tiver saldo e o aluguel seja maior que 50
- cauteloso: só compra a propriedade que "cair", se estiver disponível para venda, e sobrar do saldo mais de 80
- aleatório: compra toda propriedade que "cair", se estiver disponível para venda, tiver saldo, com uma probabilidade de 50%


## Paradigma da OOP

Objetos identificados pelo paradigma da OOP com base nos requisitos acima.

- ```Jogo```
    - descr: 
        - Entidade base do jogo
    - props:
        - data_inicio: data de início do jogo
        - data_fim: data de fim do jogo
        - qtde_rodadas: quantidade de rodadas
        - qtde_jogadores: quantidade de jogadores
        - vencedor: jogador que venceu a partida
    - actions:
        - criar: cria a partida, sorteia a ordem dos jogadores etc.
        - jogar: executa uma rodada do jogo, rotina principal
- ```Jogador```
    - descr: 
        - Entidade do jogador
    - props:
        - comportamento: comportamento do jogador
- ```Partida```
    - descr: 
        - Entidade da partida, que envolve várias rodadas
    - props:
        - jogo: qual jogo a partida pertence
        - jogador: o jogador da partida
        - posicao_atual: onde o jogador está atualmente no tabuleiro
        - ordem: ordem de jogar (definido aleatoriamente no inicio da partida)
        - eliminado: booleano para indicar se o jogador foi eliminado
    - actions:
        - criar: cria uma nova partida
- ```Rodada```
    - descr: 
        - Entidade da rodada, que representa um jogador jogando os dados na sua vez
    - props: 
        - jogo_id: qual jogo é essa rodada
        - numero: numero da rodada na partida
    - actions:
        - jogar: jogar o dado pra "andar as casas"
- ```Propriedade```
    - props:
        - descricao: nome da propriedade
        - valor_venda: valor que o jogador precisa pagar para comprar
        - ordem: posição no tabuleiro
        - valor_aluguel: valor que o jogador precisa pagar de aluguel
- ```Mercado Imobiliário```
    - props:
        - partida: qual partida se refere
        - propriedade: qual propriedade está sendo negociada
        - proprietario: jogador que comprou a propriedade
        - operação: compra, venda ou aluguel
        - numero: numero sequencial de operação para identificar a operação efetuada
    - actions:
        - comprar: comprar a propriedade
        - vender: disponibiliza a propriedade de volta ao banco, quando um jogador perde
        - alugar: paga o aluguel referente a propriedade
- ```Operação```
    - props:
        descricao: nome da operação
- ```Conta Corrente (Saldo)```
    - props:
        - jogo: qual jogo o saldo se refere
        - jogador: qual jogador esse saldo se refere
        - saldo: valor disponível na conta
    - actions:
        - sacar: tirar dinheiro da conta, subtraindo do saldo
        - depositar: colocar dinheiro na conta, adicionando ao saldo
- ```Dado (6 faces equiprováveis)```
    - props:
        - resultado: valor obtido ao jogar o dado
    - actions:
        - jogar: sortear face para obter o resultado
- ```Comportamento```
    - props: 
        - descricao: nome do comportamento
        - regra: regra do comportamento
    - actions:
        - validar: verifica a regra e retorna verdadeiro/falso

## Arquitetura

- API de Relatório das partidas em Python utilizando o framework Flask.
- Programa executável Python (linha de comando), para rodar as simulações de jogos.
- Docker para levantar 300 instâncias do programa executável
- Banco de dados relacional sqlite3.
- Design patterns:
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    - Abstract Factory para a conexão com o banco de dados, visando desacoplar o banco
    - Singleton para o gerenciamento de conexões, garantindo uma única conexão estatica, compartilhada entre as instâncias do jogo.
    - Abstração em 3 camadas, acesso a dados, ORM e domain.

## Estrutura do Código

- src
    - ```api```: API REST do relatório de execução do jogo
    - ```jogo```: aplicativo de linha de comando do jogo em si
        - ```dao```: classes de acesso a dados
        - ```models```: modelos de dados ORM
        - ```domain```: controladoras
        - ```util.py```: funções de sorteio randomico
    - ```tests```: testes unitários
    - ```app.py```: programa principal
    - ```Dockerfile```: arquivo de compilação do docker
    - ```docker-compose.yml```: arquivo de configuração do orquestrador de docker
    - ```README.md```: este arquivo
    - ```requirements.txt```: dependências a serem instaladas pelo gerenciador de pacotes

