# Aula 7 - Banco de Dados Redis e Full-Text Search

## Objetivo

Entender como o Redis funciona, em quais cenários ele é útil como banco de dados em memória e como configurar uma busca textual completa com Redis Stack, RediSearch e Docker.

## 1) O que é Redis

O **Redis** é um banco de dados NoSQL do tipo chave-valor, conhecido principalmente pela baixa latência e pelo uso intensivo de memória. Em vez de organizar os dados em tabelas, como em bancos relacionais, o Redis armazena informações em chaves associadas a estruturas de dados.

Na prática, uma chave pode apontar para:

- uma string simples;
- um hash, parecido com um pequeno documento;
- uma lista;
- um conjunto;
- um conjunto ordenado;
- um stream de eventos;
- um JSON, quando o ambiente tiver suporte a RedisJSON.

Exemplo simples:

```redis
SET usuario:1:nome "Ada Lovelace"
GET usuario:1:nome
```

Nesse caso, `usuario:1:nome` é a chave, e `"Ada Lovelace"` é o valor armazenado.

## 2) Como o Redis funciona

O Redis mantém os dados principalmente em memória RAM. Isso permite leituras e escritas muito rápidas, pois evita acessar disco a cada operação. Por esse motivo, ele aparece bastante em sistemas que precisam responder em milissegundos.

Alguns usos comuns são:

- cache de respostas de APIs;
- sessões de usuários;
- filas simples;
- rankings e placares;
- controle de rate limit;
- contadores em tempo real;
- armazenamento rápido de dados temporários;
- busca textual e vetorial com os recursos de Search.

Apesar de ser lembrado como cache, o Redis também pode persistir dados. As formas mais comuns são:

- **RDB**: cria snapshots periódicos do banco;
- **AOF**: registra comandos de escrita para reconstruir o estado depois;
- **RDB + AOF**: combina snapshots com log de comandos.

Em produção, essa decisão envolve uma troca: mais persistência e segurança contra perda de dados normalmente significam mais escrita em disco e mais custo operacional.

## 3) Estruturas de dados importantes

O Redis é simples na ideia central, mas poderoso porque suas estruturas de dados já vêm prontas para operações específicas.

### String

Usada para valores simples, contadores e cache.

```redis
SET produto:1:estoque 10
DECR produto:1:estoque
GET produto:1:estoque
```

### Hash

Usado para representar objetos pequenos, como usuários, produtos, livros e documentos.

```redis
HSET livro:1 titulo "Sistemas de Banco de Dados" autor "Elmasri e Navathe" ano 2019
HGETALL livro:1
```

### Set

Usado para coleções sem repetição.

```redis
SADD usuario:1:interesses banco_de_dados python redis
SMEMBERS usuario:1:interesses
```

### Sorted set

Usado para rankings, pontuações e ordenações por valor numérico.

```redis
ZADD ranking:alunos 95 "Ana" 88 "Bruno" 91 "Carla"
ZREVRANGE ranking:alunos 0 2 WITHSCORES
```

## 4) O que é full-text search

**Full-text search** é uma técnica de busca em texto livre. Em vez de procurar apenas igualdade exata, como `titulo = 'Redis'`, a busca textual permite encontrar documentos por termos, frases, prefixos, pesos, filtros e relevância.

Por exemplo, em uma base de livros, queremos buscar por:

- livros que contenham a palavra `redis`;
- livros cujo título tenha `banco de dados`;
- livros de uma categoria específica;
- livros publicados depois de certo ano;
- resultados ordenados por relevância ou por campo numérico.

Em bancos relacionais, é comum usar `LIKE`, índices específicos ou extensões de busca textual. No Redis, esse papel é feito pelos recursos de **Search**, historicamente associados ao módulo **RediSearch** e disponíveis de forma prática no **Redis Stack**.

## 5) Como o Redis organiza uma busca textual

Para buscar texto no Redis, primeiro criamos os documentos. Depois criamos um índice com `FT.CREATE`, informando:

- o tipo de dado que será indexado, como `HASH` ou `JSON`;
- o prefixo das chaves que fazem parte do índice;
- os campos que serão buscáveis;
- o tipo de cada campo.

Tipos comuns em índices:

- `TEXT`: campo de texto livre, adequado para título, descrição e conteúdo;
- `TAG`: campo categórico, adequado para categoria, status e autor quando se quer correspondência exata;
- `NUMERIC`: campo numérico, adequado para ano, preço, nota e quantidade;
- `GEO`: campo geográfico;
- `VECTOR`: campo vetorial, usado em busca semântica com embeddings.

Exemplo conceitual:

```redis
FT.CREATE idx:livros
  ON HASH
  PREFIX 1 livro:
  SCHEMA
    titulo TEXT WEIGHT 3.0
    descricao TEXT
    categoria TAG
    ano NUMERIC SORTABLE
```

Esse índice diz ao Redis:

- indexe hashes cujas chaves começam com `livro:`;
- trate `titulo` e `descricao` como texto pesquisável;
- dê mais peso ao campo `titulo`;
- trate `categoria` como valor categórico;
- permita filtros e ordenação pelo campo `ano`.

## 6) Exemplo prático com Docker

Para facilitar a aula, vamos usar a imagem `redis/redis-stack`, que já vem com os recursos de busca habilitados. Ela também expõe o RedisInsight, uma interface visual útil para explorar os dados.

### Criar um `docker-compose.yml`

```yaml
services:
  redis-stack:
    image: redis/redis-stack:latest
    container_name: redis-stack-aula7
    ports:
      - "6379:6379"
      - "8001:8001"
    volumes:
      - redis-stack-data:/data

volumes:
  redis-stack-data:
```

### Subir o ambiente

```bash
docker compose up -d
```

Depois disso:

- Redis estará disponível em `localhost:6379`;
- RedisInsight estará disponível em `http://localhost:8001`.

### Acessar o Redis pelo terminal

```bash
docker exec -it redis-stack-aula7 redis-cli
```

## 7) Inserindo documentos de exemplo

Vamos criar uma pequena base de livros usando hashes. Cada chave começa com `livro:`, o que facilita a indexação por prefixo.

```redis
HSET livro:1 titulo "Redis para Banco de Dados" autor "Ana Silva" categoria "banco_dados" ano 2024 descricao "Introducao ao Redis como banco NoSQL em memoria com estruturas de dados eficientes"

HSET livro:2 titulo "Busca Textual com Redis" autor "Bruno Costa" categoria "busca" ano 2025 descricao "Exemplo pratico de full-text search usando Redis Stack e indices RediSearch"

HSET livro:3 titulo "Sistemas Distribuidos Modernos" autor "Carla Rocha" categoria "arquitetura" ano 2023 descricao "Conceitos de escalabilidade replicacao particionamento cache e consistencia"

HSET livro:4 titulo "APIs Rapidas com Cache" autor "Diego Lima" categoria "backend" ano 2022 descricao "Como usar cache para reduzir latencia em aplicacoes web e servicos distribuidos"
```

## 8) Criando o índice de full-text search

Agora criamos o índice `idx:livros`.

```redis
FT.CREATE idx:livros
  ON HASH
  PREFIX 1 livro:
  LANGUAGE portuguese
  SCHEMA
    titulo TEXT WEIGHT 3.0
    autor TAG
    categoria TAG
    ano NUMERIC SORTABLE
    descricao TEXT
```

Explicação:

- `idx:livros`: nome do índice;
- `ON HASH`: os documentos estão armazenados como hashes;
- `PREFIX 1 livro:`: apenas chaves que começam com `livro:` entram no índice;
- `LANGUAGE portuguese`: usa regras de linguagem para português;
- `titulo TEXT WEIGHT 3.0`: o título pesa mais na relevância do resultado;
- `autor TAG`: permite busca exata por autor;
- `categoria TAG`: permite filtro por categoria;
- `ano NUMERIC SORTABLE`: permite filtro numérico e ordenação;
- `descricao TEXT`: campo textual comum.

Se o índice já existir, o Redis retornará erro informando que ele já foi criado. Para apagar o índice sem apagar os documentos:

```redis
FT.DROPINDEX idx:livros
```

Para apagar o índice e também os documentos indexados:

```redis
FT.DROPINDEX idx:livros DD
```

## 9) Fazendo buscas

### Buscar qualquer documento

```redis
FT.SEARCH idx:livros "*"
```

### Buscar por uma palavra

```redis
FT.SEARCH idx:livros "redis"
```

Essa consulta procura documentos que tenham o termo `redis` nos campos `TEXT` indexados.

### Buscar por frase

```redis
FT.SEARCH idx:livros "\"banco de dados\""
```

### Buscar em um campo específico

```redis
FT.SEARCH idx:livros "@titulo:Redis"
```

### Buscar por categoria

Campos `TAG` usam uma sintaxe própria:

```redis
FT.SEARCH idx:livros "@categoria:{busca}"
```

### Buscar por faixa numérica

```redis
FT.SEARCH idx:livros "@ano:[2024 2025]"
```

### Combinar texto e filtro

```redis
FT.SEARCH idx:livros "redis @ano:[2024 2025]"
```

### Ordenar por ano

```redis
FT.SEARCH idx:livros "*" SORTBY ano DESC
```

### Retornar apenas alguns campos

```redis
FT.SEARCH idx:livros "redis" RETURN 3 titulo autor ano
```

### Ver score de relevância

```redis
FT.SEARCH idx:livros "redis" WITHSCORES
```

## 10) Exemplo com script de carga

Para repetir o experimento de forma simples, crie um arquivo chamado `carga.redis`:

```redis
HSET livro:1 titulo "Redis para Banco de Dados" autor "Ana Silva" categoria "banco_dados" ano 2024 descricao "Introducao ao Redis como banco NoSQL em memoria com estruturas de dados eficientes"
HSET livro:2 titulo "Busca Textual com Redis" autor "Bruno Costa" categoria "busca" ano 2025 descricao "Exemplo pratico de full-text search usando Redis Stack e indices RediSearch"
HSET livro:3 titulo "Sistemas Distribuidos Modernos" autor "Carla Rocha" categoria "arquitetura" ano 2023 descricao "Conceitos de escalabilidade replicacao particionamento cache e consistencia"
HSET livro:4 titulo "APIs Rapidas com Cache" autor "Diego Lima" categoria "backend" ano 2022 descricao "Como usar cache para reduzir latencia em aplicacoes web e servicos distribuidos"

FT.CREATE idx:livros ON HASH PREFIX 1 livro: LANGUAGE portuguese SCHEMA titulo TEXT WEIGHT 3.0 autor TAG categoria TAG ano NUMERIC SORTABLE descricao TEXT
```

Execute:

```bash
docker exec -i redis-stack-aula7 redis-cli < carga.redis
```

Depois teste:

```bash
docker exec -it redis-stack-aula7 redis-cli FT.SEARCH idx:livros "redis"
```

## 11) Boas práticas

- use prefixos claros nas chaves, como `livro:`, `produto:` e `usuario:`;
- crie índices apenas para os campos realmente consultados;
- use `TEXT` para texto livre e `TAG` para filtros exatos;
- use `NUMERIC SORTABLE` somente quando precisar filtrar ou ordenar por números;
- defina pesos (`WEIGHT`) quando alguns campos forem mais importantes que outros;
- avalie consumo de memória, pois índices melhoram consulta, mas ocupam espaço;
- planeje persistência, backup e replicação quando o Redis guardar dados importantes;
- em produção, evite usar `latest` sem controle de versão da imagem Docker.

## 12) Fechamento

O Redis é mais do que um cache: ele é um banco NoSQL rápido, com estruturas de dados úteis para problemas práticos de backend e análise de dados. Com Redis Stack e os recursos de Search, ele também consegue trabalhar com busca textual, filtros, ordenação e relevância.

O fluxo principal da aula é:

1. subir o Redis Stack com Docker;
2. inserir documentos como hashes;
3. criar um índice com `FT.CREATE`;
4. consultar os dados com `FT.SEARCH`;
5. combinar busca textual com filtros por categoria e ano.

## Referências

- Documentação oficial do Redis sobre `FT.CREATE`: <https://redis.io/docs/latest/commands/ft.create/>
- Documentação oficial do Redis sobre `FT.SEARCH`: <https://redis.io/docs/latest/commands/ft.search/>
- Documentação oficial do Redis sobre campos e tipos de índices: <https://redis.io/docs/latest/develop/ai/search-and-query/indexing/field-and-type-options/>
