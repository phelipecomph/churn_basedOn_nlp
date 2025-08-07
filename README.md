# Análise de Churn Baseada em NLP

Este projeto utiliza técnicas de Processamento de Linguagem Natural (NLP) para analisar comentários de clientes e identificar padrões relacionados ao churn e satisfação do cliente, com foco na metodologia Net Promoter Score (NPS).

## Estrutura do Projeto

O projeto está organizado em 5 notebooks principais que seguem um pipeline de análise completo:

### Pipeline de Processamento e Limpeza de Dados

#### 1. Limpeza e Análise Inicial (`01_Limpeza_e_AnaliseInicial.ipynb`)

**Objetivo:** Correção de inconsistências nos dados e preparação inicial do dataset.

**Principais atividades realizadas:**
- **Correção estrutural dos dados:** Identificação e correção de 33 linhas com problemas estruturais (comentários sem fechamento de aspas, colunas divergentes)
- **Padronização de localização:** Simplificação das localidades para apenas UF (estados), corrigindo inconsistências como "Rio de Janeiro/RJ/Rio Grande do Sul"
- **Resolução de IDs duplicados:** Correção de clientes compartilhando mesmo ID (caso dos clientes Julio Santos e Gabriela Almeida)
- **Normalização de variáveis numéricas:**
  - Conversão de TMA (Tempo Médio de Atendimento) de minutos para segundos
  - Remoção da unidade "GB" da coluna de volume de dados
  - Conversão de valores "-" para 0 em campos numéricos
- **Criação de variável de churn:** Adição de flag booleana baseada na presença de data de término do contrato
- **Análise exploratória inicial:** Identificação de churn rate de apenas 4%, indicando necessidade de foco em análise de detratores

#### 2. Identificação de Promotores e Detratores (`02_Identificar_PromotorDetrator.ipynb`)

**Objetivo:** Classificação automática de comentários de clientes em Promotores, Neutros e Detratores usando LLM.

**Metodologia:**
- **Classificação via LLM:** Uso do GPT-4o-mini para classificar comentários sem necessidade de dados pré-anotados
- **Cálculo de NPS:** Implementação da fórmula tradicional de NPS
- **Análise segmentada:** Exploração do NPS por subgrupos (localização, serviço, dependentes, preço)

**Principais descobertas:**
- **NPS geral:** 0.98 pontos (na fronteira entre Zona Crítica e Zona de Aperfeiçoamento)
- **Variações regionais:** SP apresenta NPS mais baixo (-13.79), enquanto RJ e MG têm valores ligeiramente positivos
- **Diferenças por serviço:**
  - Telefonia Fixa: melhor performance (NPS 26.09)
  - TV a Cabo: maior problema (NPS -16.0)
  - Telefonia Móvel: NPS negativo (-8.7)

#### 3. Identificação de Tópicos (`03_Identificar_Topicos.ipynb`)

**Objetivo:** Descoberta de temas principais nas reclamações dos clientes usando técnicas clássicas de NLP.

**Metodologia:**
- **Pré-processamento avançado:** 
  - Remoção de acentos (unidecode)
  - Normalização para lowercase
  - Remoção de pontuação e números
  - Stemming com RSLPStemmer
  - Filtros de stopwords e palavras com menos de 4 caracteres
- **Modelagem de tópicos:** Uso do BERTopic com modelo multilíngue paraphrase-multilingual-MiniLM-L12-v2
- **Refinamento manual:** Adição do tópico "atendimento" baseado em análise qualitativa

**Tópicos identificados:**
- `internet_connection`: Problemas de conexão e velocidade de internet
- `critical_appointments`: Reclamações críticas e insultos à empresa
- `quality_tv_channels`: Qualidade dos canais de TV
- `signal`: Problemas de sinal
- `atendimento`: Questões relacionadas ao atendimento ao cliente
- `other`: Outros temas diversos

**Insights sobre relacionamento tópico-serviço:**
- Forte correlação entre tópicos e tipos de serviço
- `critical_appointments` e `atendimento` são transversais aos serviços
- Detratores concentram-se principalmente em `internet_connection`, `atendimento` e `critical_appointments`

### Análises Exploratórias Específicas

#### 4. Exploração de Tópicos de Serviço (`04_Explorar_Topicos_Servico.ipynb`)

**Objetivo:** Análise detalhada dos problemas técnicos relacionados aos serviços oferecidos.

**Principais análises e descobertas:**

**Telefonia Móvel:**
- **Problemas identificados:** Internet móvel instável para streaming e problemas de cobertura/qualidade de áudio
- **Análise de expectativas:** Clientes detratores usam serviços para atividades de alto consumo (streaming, filmes) com planos básicos
- **Concentração geográfica:** Problemas de cobertura concentrados no RS
- **Impacto potencial:** Resolução dos problemas técnicos poderia elevar NPS de -9 para 65

**Internet:**
- **Problemas recorrentes:** Velocidade abaixo do esperado e instabilidade de conexão
- **Perfil dos detratores:** Clientes com mais dependentes em SP e RJ, mesmo tendo planos superiores
- **Oportunidades identificadas:** Cross-selling de soluções mesh, educação do cliente sobre priorização de dispositivos
- **Impacto potencial:** Melhoria poderia elevar NPS de 3 para 61

**Telefonia Fixa:**
- **Problemas similares:** Qualidade de áudio e interrupções de chamadas
- **Concentração geográfica:** Problemas concentrados em MG
- **Análise de preços:** Detratores usam planos mais básicos comparado aos promotores
- **Impacto potencial:** Resolução + upselling poderia elevar NPS de 26 para 86

**Impacto combinado:** Implementação de todas as melhorias poderia elevar o NPS geral de 1 para 50 pontos.

#### 5. Exploração do Tópico Atendimento (`05_Explorar_Topico_Atendimento.ipynb`)

**Objetivo:** Análise específica dos problemas relacionados ao atendimento ao cliente.

**Análise de Churn:**
- **Composição:** 50% dos churns relacionados a problemas de atendimento
- **Concentração:** 75% dos churns relacionados à TV a Cabo e concentrados em MG
- **Padrão identificado:** 25% representa churn natural (cliente previamente promotor)

**Análise do Atendimento:**
- **Natureza dos problemas:** Atendimento como agravante de problemas técnicos, não problema primário
- **Características do atendimento:** Reclamações genéricas sobre ineficiência, falta de resolução

**Insights comportamentais:**
- **Promotores:** Preferem atendimentos mais longos mas resolutivos
- **Detratores:** Tendem a fazer uma reclamação e reduzem drasticamente contatos subsequentes
- **Padrão de risco:** Redução de contatos pode indicar cliente próximo ao churn

**Recomendações estratégicas:**
- Priorizar qualidade sobre velocidade no atendimento
- Implementar campanhas ativas para clientes com reclamações não resolvidas
- Focar em resolução na primeira interação

## Tecnologias Utilizadas

- **Python** com pandas para manipulação de dados
- **NLTK** para pré-processamento de texto (stopwords, stemming)
- **BERTopic** para modelagem de tópicos
- **SentenceTransformers** para embeddings multilíngues
- **OpenAI GPT-4o-mini** para classificação de sentimentos
- **Matplotlib** para visualizações

## Estrutura de Arquivos

```
├── data/
│   ├── 01_original_data.csv           # Dados originais
│   ├── 02_churn_fixed.csv            # Dados com correções estruturais
│   ├── 03_churn_cleaned.csv          # Dados limpos e normalizados
│   ├── 04_nlp_classificados.csv      # Dados com classificação NPS
│   └── 05_nlp_classificados_topicos.csv # Dados finais com tópicos
├── utils/
│   ├── cleaning.py                    # Funções de limpeza de dados
│   └── nlp_classifier.py             # Funções de classificação NLP
└── notebooks/                        # Notebooks de análise
```

## Principais Resultados e Recomendações

### Situação Atual
- **NPS Geral:** 0.98 (Zona de Aperfeiçoamento)
- **Principais problemas:** Questões técnicas regionalizadas e problemas de atendimento
- **Churn rate baixo:** 4%, indicando potencial de melhoria via satisfação

### Oportunidades de Melhoria Identificadas

1. **Resolução de Problemas Técnicos Regionais**
   - RS (Telefonia Móvel): Qualidade de sinal e cobertura
   - SP/RJ (Internet): Estabilidade para múltiplos usuários
   - MG (Telefonia Fixa): Qualidade de áudio

2. **Estratégias Comerciais**
   - Cross-selling de soluções mesh para internet
   - Upselling de planos telefonia fixa
   - Alinhamento de expectativas de uso vs. plano contratado

3. **Melhoria do Atendimento**
   - Foco em resolução na primeira interação
   - Campanhas ativas para clientes com reclamações
   - Treinamento para atendimentos mais resolutivos

### Impacto Potencial
A implementação completa das melhorias identificadas poderia elevar o NPS geral de 1 para 50 pontos, movendo a empresa da Zona de Aperfeiçoamento para a Zona de Sucesso.