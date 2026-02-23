# Aula 1 - Léxico Conceitual

## Objetivo

Consolidar o vocabulário essencial de Banco de Dados, Big Data e Análise de Dados para nivelar a turma no início da disciplina, com foco em aplicação prática.

## Termos essenciais

1. **Banco de Dados**: conjunto organizado de dados persistentes, modelado para permitir armazenamento, consulta, atualização e recuperação eficiente. Um banco de dados existe para suportar operações do negócio com confiabilidade e histórico.  
   Exemplo: base de clientes, pedidos e pagamentos de um e-commerce.

2. **SGBD (Sistema Gerenciador de Banco de Dados)**: software que intermedeia o acesso aos dados, controlando concorrência, segurança, backup, recuperação e desempenho. O SGBD implementa regras para garantir integridade e disponibilidade.  
   Exemplo: PostgreSQL, MySQL, MongoDB, Oracle.

3. **SQL (Structured Query Language)**: linguagem declarativa padrão para bancos relacionais, usada em DDL (estrutura), DML (dados), DCL (controle) e TCL (transação). O foco é dizer "o que" deseja obter, não "como" executar internamente.  
   Exemplo: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN`.

4. **NoSQL**: família de bancos não relacionais (documento, chave-valor, coluna, grafo) que priorizam flexibilidade de schema, distribuição e escalabilidade horizontal. É comum em cenários de alto volume e mudança frequente de estrutura de dados.  
   Exemplo: MongoDB (documento), Redis (chave-valor), Neo4j (grafo).

5. **Big Data**: contexto de dados com alto volume, variedade e velocidade (3Vs), muitas vezes estendido para veracidade e valor. Exige arquiteturas distribuídas para ingestão, processamento e análise em escala.  
   Exemplo: logs de milhões de acessos por dia em plataforma digital.

6. **Dados Estruturados**: dados organizados em formato tabular e schema fixo, com tipos e regras bem definidos. Facilitam validação, integridade e consultas analíticas tradicionais.  
   Exemplo: tabela `vendas(data, produto, quantidade, valor)`.

7. **Dados Não Estruturados**: dados sem estrutura tabular rígida, como texto livre, imagem, áudio, vídeo e documentos diversos. Requerem técnicas específicas de indexação, extração e enriquecimento para gerar análise.  
   Exemplo: comentários de clientes, PDFs e mensagens de chat.

8. **Schema (Esquema de Dados)**: definição formal da estrutura dos dados, incluindo entidades, campos, tipos, relacionamentos e restrições. Em SQL tende a ser estrito; em NoSQL pode ser mais flexível (schema-on-read).  
   Exemplo: regra de que `email` deve ser único e não nulo.

9. **Pipeline de Dados**: sequência organizada de etapas de processamento em que os dados passam por coleta, validação, transformação e entrega. É um fluxo padronizado para garantir repetibilidade, qualidade e rastreabilidade.  
   Exemplo: ingestão diária de dados de vendas, limpeza automática e publicação no ambiente de BI.

10. **ETL (Extract, Transform, Load)**: processo em que a transformação ocorre antes da carga final, entregando dados já limpos e padronizados no destino. É comum quando o ambiente de destino exige estrutura analítica pronta.  
   Exemplo: consolidar ERP + CRM e carregar tabelas tratadas em um Data Warehouse.

11. **ELT (Extract, Load, Transform)**: processo em que os dados são carregados primeiro e transformados dentro da própria plataforma de destino, aproveitando seu poder de processamento. É útil para manter dados brutos e flexibilizar novas transformações.  
   Exemplo: carregar dados no lakehouse e modelar visões analíticas com SQL.

12. **KDD (Knowledge Discovery in Databases)**: processo completo para descobrir conhecimento útil em dados, incluindo seleção, limpeza, transformação, mineração e interpretação. Data mining é uma etapa dentro do KDD.  
   Exemplo: descobrir perfis de clientes com maior propensão de cancelamento.

13. **Mineração de Dados**: aplicação de algoritmos para encontrar padrões, correlações, anomalias e grupos em grandes conjuntos de dados. O objetivo é gerar conhecimento acionável para decisão.  
   Exemplo: regras de associação do tipo "quem compra A tende a comprar B".

14. **Machine Learning**: área que cria modelos capazes de aprender padrões a partir de dados para prever, classificar ou recomendar. Pode ser supervisionado, não supervisionado ou por reforço, dependendo do problema.  
   Exemplo: modelo de classificação para prever inadimplência.

15. **Business Intelligence (BI)**: conjunto de processos e ferramentas para transformar dados em informação gerencial por meio de métricas, visualizações e análises. O foco central é apoiar decisão com evidência.  
   Exemplo: painel com faturamento, margem e ticket médio por região.

16. **Data Warehouse**: repositório corporativo orientado à análise histórica, com dados integrados, consistentes e modelados para consulta. Prioriza leitura e agregação, não transações operacionais do dia a dia.  
   Exemplo: base consolidada para relatórios executivos mensais.

17. **Data Lake**: repositório de grande escala para dados brutos e semiestruturados, preservando o formato original para uso futuro. É adequado para exploração, ciência de dados e cenários com requisitos variáveis.  
   Exemplo: armazenamento central de logs, JSON, CSV, imagens e eventos.

18. **Dashboard**: interface visual que sintetiza KPIs, tendências e alertas para monitoramento contínuo. Deve ser claro, objetivo e alinhado a decisões de negócio, evitando excesso de gráficos sem contexto.  
   Exemplo: painel diário de vendas com metas e variação percentual.

19. **Escalabilidade**: capacidade do sistema de manter desempenho ao aumentar carga de usuários, dados ou transações. Pode ser vertical (mais recurso na mesma máquina) ou horizontal (mais máquinas/nós).  
   Exemplo: adicionar novos nós para suportar pico de acessos.

20. **Latência**: tempo entre a solicitação e a resposta de um sistema; impacta diretamente a experiência do usuário e a eficiência de processos. Em dados, envolve leitura, escrita, rede e processamento.  
   Exemplo: consulta de dashboard que demora 10 ms vs 3 s.

21. **Consistência de Dados**: propriedade que garante dados corretos e coerentes após operações e transações, respeitando regras de negócio. Em sistemas distribuídos, pode variar entre consistência forte e eventual.  
   Exemplo: saldo bancário atualizado corretamente após transferência.
