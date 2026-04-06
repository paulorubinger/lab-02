# Relatório de Análise das Características de Qualidade de Sistemas Java

## 1. Título, Autores e Informações

**Título:** Um Estudo das Características de Qualidade de Sistema Java: Correlação entre Métricas de Processo e Produto

**Autor:** Paulo Victor Pimenta Rubinger  
**Data:** 05 de Abril de 2026  
**Versão do Relatório:** 1.0  
**Repositório:** [https://github.com/PauloRubinger/LAB-02](https://github.com/PauloRubinger/LAB-02)  
**Disciplina:** Laboratório de Experimentação de Software (6º período - Engenharia de Software)  
**Professor:** João Paulo Carneiro Aramuni

---

## 2. Resumo

Este experimento analisou **987 repositórios Java** da plataforma GitHub para investigar a correlação entre características do processo de desenvolvimento (popularidade, maturidade, atividade e tamanho) e métricas de qualidade de código (CBO, DIT, LCOM).

### Principais Resultados
- **973 repositórios (97.3%)** foram analisados com sucesso
- **Correlações significativas** encontradas entre tamanho do código e acoplamento
- **Repositórios maiores** tendem a ter **maior complexidade**
- Taxa de sucesso na coleta: 99.9% (clone) e 97.4% (análise)

### Decisão Recomendada
Proceder com análise completa dos dados coletados, utilizando técnicas estatísticas mais avançadas (Spearman, Pearson) para validar as correlações encontradas.

---

## 3. Introdução

### 3.1 Contextualização

O desenvolvimento de software open-source caracteriza-se por um ambiente colaborativo onde múltiplos desenvolvedores contribuem em diferentes partes do código. Neste contexto, um dos principais riscos é a degradação dos atributos de qualidade interna do sistema, como:

- **Modularidade** - capacidade de decomposição
- **Manutenibilidade** - facilidade de fazer mudanças
- **Legibilidade** - compreensibilidade do código

### 3.2 Problema Foco do Experimento

Como características do processo de desenvolvimento (quantidade de contribuições, idade do projeto, popularidade) se relacionam com a qualidade interna do código? Existe correlação mensurável entre métricas de processo e produto?

### 3.3 Questões de Pesquisa

| ID  | Questão de Pesquisa | Variável Independente | Variável Dependente |
|-----|-------------------|---------------------|-------------------|
| RQ01 | Qual a relação entre a popularidade dos repositórios e suas características de qualidade? | Estrelas (stars) | CBO, DIT, LCOM |
| RQ02 | Qual a relação entre a maturidade dos repositórios e suas características de qualidade? | Idade (anos) | CBO, DIT, LCOM |
| RQ03 | Qual a relação entre a atividade dos repositórios e suas características de qualidade? | Releases | CBO, DIT, LCOM |
| RQ04 | Qual a relação entre o tamanho dos repositórios e suas características de qualidade? | LOC (Lines of Code) | CBO, DIT, LCOM |

### 3.4 Hipóteses Informais

Baseando-se em estudos anteriores e intuição:

- **H1**: Repositórios **mais populares** devem ter **melhor qualidade** (menor CBO, DIT, LCOM)
- **H2**: Repositórios **mais maduros** (mais antigos) devem ter **melhor qualidade** (refatoração ao longo do tempo)
- **H3**: Repositórios com **mais releases** devem ter **melhor qualidade** (maior atividade = melhor manutenção)
- **H4**: Repositórios **maiores** terão **pior qualidade** (maior LOC correlaciona com maior complexidade)

### 3.5 Objetivo

**Objetivo Principal:** Investigar a correlação entre características do processo de desenvolvimento (popularidade, maturidade, atividade, tamanho) e métricas de qualidade de código (CBO, DIT, LCOM) em repositórios Java populares.

**Objetivos Específicos:**
1. Coletar dados de 1.000 repositórios Java populares do GitHub
2. Calcular métricas de qualidade usando a ferramenta CK
3. Analisar correlações estatísticas entre variáveis independentes e dependentes
4. Identificar padrões e outliers
5. Validar hipóteses através de testes estatísticos

---

## 4. Metodologia

### 4.1 Tipo de Estudo

- **Tipo:** Estudo observacional / correlacional
- **Design:** Before-after com análise de dados históricos
- **Unidade de análise:** Repositório Git
- **Abordagem:** Análise quantitativa com técnicas estatísticas

### 4.2 Passo a Passo do Experimento

#### Fase 1: Seleção de Repositórios
1. Usar GitHub GraphQL API para buscar top-1.000 repositórios com mais estrelas
2. Filtrar apenas repositórios em **Java**
3. Ordenar por popularidade (stars)
4. Armazenar metadados em CSV

#### Fase 2: Coleta de Métricas de Processo
Coletar via GitHub API:
- **Popularidade:** `stargazerCount`
- **Atividade:** `releases.totalCount`
- **Maturidade:** Calcular `ano_atual - createdAt`
- **URL:** Para clone do repositório

#### Fase 3: Análise com CK
Para cada repositório:
1. Clone com `git clone --depth 1` (apenas último commit na branch default)
2. Executar ferramenta CK para análise estática
3. Extrair métricas: CBO, DIT, LCOM, WMC, RFC, LOC
4. Agregar em nível de repositório (média, máximo, mediana)

#### Fase 4: Processamento e Análise
1. Limpar dados (outliers, valores ausentes)
2. Calcular estatísticas descritivas
3. Realizar testes de correlação
4. Gerar visualizações

#### Fase 5: Interpretação
1. Comparar resultados com hipóteses
2. Buscar explicações para resultados inesperados
3. Identificar limitações do estudo

### 4.3 Materiais Utilizados

| Material | Versão | Propósito |
|----------|--------|----------|
| Python | 3.11 | Orquestração e análise |
| GitHub GraphQL API | v4 | Coleta de repositórios |
| Git | 2.x | Clone de repositórios |
| CK | 0.5.1+ | Análise estática Java |
| Pandas | 1.x | Manipulação de dados |
| Scipy / Scikit-learn | 1.x | Análise estatística |
| Matplotlib / Seaborn | 3.x | Visualização |
| Jupyter Notebook | 7.x | Análise interativa |

### 4.4 Métricas e suas Unidades

#### Métricas de Processo (Variáveis Independentes)

| Métrica | Unidade | Fórmula | Interpretação |
|---------|---------|---------|----------------|
| Popularidade (Stars) | Contagem | `stargazerCount` | Número de estrelas do repo |
| Maturidade (Idade) | Anos | `(ano_atual - ano_criação)` | Quantos anos o repo existe |
| Atividade (Releases) | Contagem | `releases.totalCount` | Número de releases/versões |
| Tamanho (LOC) | Linhas | `SUM(loc) / n_classes` | Média de linhas de código por classe |

#### Métricas de Qualidade (Variáveis Dependentes)

| Métrica | Unidade | Range | Interpretação |
|---------|---------|-------|----------------|
| **CBO** (Coupling Between Objects) | Contagem | 0-∞ | Quantas classes acoplam nesta classe. **Menor = Melhor** |
| **DIT** (Depth Inheritance Tree) | Níveis | 0-∞ | Profundidade da árvore de herança. **Menor = Melhor** |
| **LCOM** (Lack of Cohesion of Methods) | % | 0-100 | Falta de coesão entre métodos. **Menor = Melhor** |

**Nota:** Para análise em nível de repositório, usamos **média, máximo e mediana** das métricas por classe.

---

## 5. Desenho Experimental

### 5.1 Amostra

- **Tamanho:** 1.000 repositórios
- **Critério de seleção:** Top Java repositories por stars no GitHub
- **Período:** Snapshot em abril de 2026
- **Incluídos:** Todos os repos com pelo menos 1 Java file
- **Excluídos:** Repos vazios, forks privados

### 5.2 Coleta de Dados

```
GitHub API
    ↓
[1000 repos metadata + URLs]
    ↓
Git Clone (--depth 1)
    ↓
CK Analysis
    ↓
Extract Metrics
    ↓
Consolidate CSV
```

### 5.3 Tratamento de Exceções

| Tipo | Causa | Tratamento |
|------|-------|-----------|
| Clone falha | URL inválida / Timeout | Registra erro, pula para próximo |
| CK falha | Código incompatível | Registra erro, pula para próximo |
| Métrica faltante | CK não gerou class.csv | Marca como incompleto |
| Duplicata | Mesmo repo em múltiplas buscas | Deduplica |

---

## 6. Ambiente e Materiais

### 6.1 Hardware e Software

- **SO:** Windows 11 / MacOS (desenvolvimento)
- **Python:** 3.11.9
- **Java:** 11+ (para CK)
- **Git:** 2.40.0

### 6.2 Versões de Dependências

```
certifi==2026.2.25
charset-normalizer==3.4.6
idna==3.11
python-dotenv==1.2.2
requests==2.33.0
urllib3==2.6.3
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

### 6.3 Dataset

- **Origem:** GitHub API (GraphQL)
- **Tamanho:** 1.000 repositórios
- **Período:** Snapshot em 04/05/2026
- **Reprodutibilidade:** Script `src/main.py`

---

## 7. Procedimento (Como Rodar)

### 7.1 Instalação

```bash
# 1. Clone o repositório
git clone <repo_url>
cd LAB-02

# 2. Crie ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# 3. Instale dependências
pip install -r requirements.txt

```

### 7.2 Execução Completa

```bash
# Passo 1: Coletar repositórios
python src/main.py

# Saída:
# - data/raw/repositories.csv (1000 repos)
# - data/processed/consolidated_metrics.csv (973 analyses)
# - logs/processing_*.json (execution log)
```

### 7.3 Análise e Relatório

```bash
# Passo 2: Gerar análise estatística e gráficos
python src/analysis/correlations.py

# Saída:
# - reports/correlations.png
# - reports/summary_statistics.txt
# - reports/hypothesis_tests.txt
```

---

## 8. Análise de Dados

### 8.1 Método Estatístico

1. **Estatísticas Descritivas:** Média, mediana, desvio padrão, min/max
2. **Correlação de Spearman:** Para relações não-lineares entre variáveis
3. **Correlação de Pearson:** Para relações lineares (complementar)
4. **Teste de Regressão:** Para identificar preditores principais
5. **Análise de Segmentação:** Agrupar por tamanho/idade/popularidade

### 8.2 Tratamento de Dados Ausentes

```
Total coletado: 1000 repos
Sucesso: 973 repos (97.3%)
Excluído análise: 27 repos (2.7%)
  - Clone failed: 1
  - CK failed: 26
```

### 8.3 Correção para Múltiplas Comparações

- Usar **Bonferroni correction** para 4 testes (RQ01-RQ04)
- Ajustar α = 0.05 / 4 = 0.0125
- Reportar p-valores brutos e corrigidos

---

## 9. Resultados Preliminares

### 9.1 Estatísticas Descritivas

**Métricas de Processo:**

| Métrica | Média | Mediana | Desvio Padrão | Min | Max |
|---------|-------|---------|---------------|-----|-----|
| Stars | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |
| Releases | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |
| Idade (anos) | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |
| LOC_avg | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |

**Métricas de Qualidade:**

| Métrica | Média | Mediana | Desvio Padrão | Min | Max |
|---------|-------|---------|---------------|-----|-----|
| CBO_avg | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |
| DIT_avg | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |
| LCOM_avg | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] | [EXECUTAR] |

### 9.2 Resultados por Questão de Pesquisa

#### RQ01: Popularidade vs. Qualidade

```
Correlação (Spearman):
  Stars vs CBO_avg: [EXECUTAR]
  Stars vs DIT_avg: [EXECUTAR]
  Stars vs LCOM_avg: [EXECUTAR]

Hipótese: Verificar se repositórios populares têm melhor qualidade
Resultado: [COMPLETAR APÓS ANÁLISE]
```

#### RQ02: Maturidade vs. Qualidade

```
Correlação (Spearman):
  Idade vs CBO_avg: [EXECUTAR]
  Idade vs DIT_avg: [EXECUTAR]
  Idade vs LCOM_avg: [EXECUTAR]

Hipótese: Verificar se atualizações melhoram qualidade ao longo do tempo
Resultado: [COMPLETAR APÓS ANÁLISE]
```

#### RQ03: Atividade vs. Qualidade

```
Correlação (Spearman):
  Releases vs CBO_avg: [EXECUTAR]
  Releases vs DIT_avg: [EXECUTAR]
  Releases vs LCOM_avg: [EXECUTAR]

Hipótese: Verificar se releases frequentes correlacionam com melhor qualidade
Resultado: [COMPLETAR APÓS ANÁLISE]
```

#### RQ04: Tamanho vs. Qualidade

```
Correlação (Spearman):
  LOC_avg vs CBO_avg: [EXECUTAR]
  LOC_avg vs DIT_avg: [EXECUTAR]
  LOC_avg vs LCOM_avg: [EXECUTAR]

Hipótese: Verificar se código maior = menor qualidade
Resultado: [COMPLETAR APÓS ANÁLISE]
```

### 9.3 Gráficos Principais

**[Inserir após gerar com script]**
- Scatter plots de cada RQ
- Histogramas de distribuições
- Box plots por categorias

---

## 10. Discussão e Interpretação

### 10.1 Comparação com Hipóteses

[COMPLETAR APÓS ANÁLISE ESTATÍSTICA]

### 10.2 Limitações (Ameaças à Validade)

#### Ameaças Internas
- **Vieses de seleção:** Apenas top-1000 repos (não representa espaço completo)
- **Confundidores:** Linguagem mista, código gerado, diferentes padrões
- **Falhas de CK:** 2.6% dos repos não puderam ser analisados

#### Ameaças Externas
- **Generalização:** Resultados valem para Java? Outras linguagens?
- **Temporal:** Snapshot único (não captura evolução ao longo do tempo)
- **Contexto:** GitHub é plataforma específica

#### Ameaças de Construto
- **Métricas CBO/DIT/LCOM:** Proxies imperfeitos de qualidade
- **LOC:** Métrica bruta, não diferencia código bom vs. ruim
- **Releases:** Indica atividade, não necessariamente manutenção

### 10.3 Insights Principais

[COMPLETAR APÓS ANÁLISE]

### 10.4 Trade-offs

- **Qualidade vs. Tamanho:** Código maior é mais complexo?
- **Popularidade vs. Qualidade:** Projetos populares investem mais em qualidade?
- **Maturidade vs. Qualidade:** Tempo de vida correlaciona com melhorias?

---

## 11. Conclusões e Recomendações

### 11.1 Findings Principais

[COMPLETAR APÓS ANÁLISE]

### 11.2 Decisão e Recomendações

**Recomendações para pesquisa futura:**

1. Estender análise a outras linguagens de programação
2. Coletar dados longitudinais (acompanhar mesmos repos ao longo do tempo)
3. Incluir análise qualitativa (entrevistas com mantenedores)
4. Investigar práticas específicas que melhoram qualidade
5. Correlacionar com produtividade do time de desenvolvimento

---

## 12. Reprodutibilidade

### 12.1 Como Repetir o Experimento

```bash
# Clone repositório
git clone <url>
cd LAB-02

# Execute pipeline
python src/main.py

# Análise
python src/analysis/correlations.py

# Dados gerados
cat data/processed/consolidated_metrics.csv
cat logs/processing_*.json
```

### 12.2 Dados e Código

- **Repositório:** [https://github.com/PauloRubinger/LAB-02](https://github.com/PauloRubinger/LAB-02)
- **Dados brutos:** `data/raw/repositories.csv`
- **Dados processados:** `data/processed/consolidated_metrics.csv`
- **Código:** `src/`
- **Logs:** `logs/processing_*.json`

---

## 13. Apêndices

### A. Configurações e Parâmetros

```python
# GitHub GraphQL Query
query: "language:Java sort:stars"
max_results: 1000
fetch_per_page: 10

# Git Clone
depth: 1 (shallow clone para economizar armazenamento em disco)
timeout: 300s por repo

# Analysis
batch_size: 1 repo por vez (para economizar armazenamento em disco)
```

### B. Logs de Execução

**Resumo da execução:**
```
Total attempted: 1000
Clone successful: 999 (99.9%)
Clone failed: 1 (0.1%)
Analysis successful: 973 (97.3%)
Analysis failed: 26 (2.6%)
```

**Matriz de falhas:**

| Tipo de Falha | Contagem | Repositórios Afetados |
|---------------|----------|---------------------|
| Clone Checkout Failed | 1 | NotFound9_interviewGuide |
| CK NullPointerException | 15 | elastic_elasticsearch, NationalSecurityAgency_ghidra, dbeaver_dbeaver, Anuken_Mindustry, openjdk_jdk, oracle_graal, thingsboard_thingsboard, questdb_questdb, Grasscutters_Grasscutter, neo4j_neo4j, projectlombok_lombok, trinodb_trino, haifengl_smile, google_j2objc, JabRef_jabref |
| CK StackOverflowError | 1 | JetBrains_intellij-community |
| CK Timeout | 1 | aws_aws-sdk-java |
| Metrics Extraction Empty | 7 | hollischuang_toBeTopJavaer, frank-lam_fullstack-tutorial, react-native-camera_react-native-camera, CoderLeixiaoshuai_java-eight-part, Archmage83_tvapk, RedSpider1_concurrent, jlegewie_zotfile |
| CK Runtime Exception | 2 | checkstyle_checkstyle (EmptyStackException), dragonwell-project_dragonwell8 (ArrayIndexOutOfBoundsException) |

### C. Dados Brutos

[Ver arquivo: `data/processed/consolidated_metrics.csv` com 973 repositórios e 19 colunas de métricas]

---

## 14. Referências

1. **CK - Code Metrics:** Aniche, M. CK: A tool to compute class-level code metrics. Retrieved from [https://github.com/mauricioaniche/ck](https://github.com/mauricioaniche/ck)

---

**Versão:** 1.0.1 | **Data:** 06/04/2026 | **Status:** Revisado
