# Relatório de Análise das Características de Qualidade de Sistemas Java

## 1. Título, Autores e Informações

**Título:** Um Estudo das Características de Qualidade de Sistema Java: Correlação entre Métricas de Processo e Produto

**Autor:** Paulo Victor Pimenta Rubinger  
**Data:** 05 de Abril de 2026  
**Versão do Relatório:** 2.0.0  
**Repositório:** [https://github.com/PauloRubinger/LAB-02](https://github.com/PauloRubinger/LAB-02)  
**Disciplina:** Laboratório de Experimentação de Software (6º período - Engenharia de Software)  
**Professor:** João Paulo Carneiro Aramuni

---

## 2. Resumo

Este experimento analisou **974 repositórios Java** da plataforma GitHub para investigar a correlação entre características do processo de desenvolvimento (popularidade, maturidade, atividade e tamanho) e métricas de qualidade de código (CBO, DIT, LCOM).

### Principais Resultados
- **974 repositórios (97.4%)** foram analisados com sucesso
- **Correlações significativas** encontradas entre tamanho do código e todas as métricas de qualidade
- **Repositórios maiores** tendem a ter **maior acoplamento e menor coesão**
- **Atividade (releases)** correlaciona positivamente com piores métricas de qualidade
- **Popularidade (stars)** não apresenta correlação significativa com qualidade

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
3. Extrair métricas: CBO, DIT, LCOM, LOC
4. Agregar em nível de repositório (média, mediana, desvio padrão)

#### Fase 4: Processamento e Análise
1. Limpar dados (valores ausentes)
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
| Python | 3.14.3 | Orquestração e análise |
| GitHub GraphQL API | v4 | Coleta de repositórios |
| Git | 2.40.0 | Clone de repositórios |
| CK | 0.7.1-SNAPSHOT | Análise estática de código Java |
| requests | 2.33.0 | Requisições HTTP para coleta via API |
| python-dotenv | 1.2.2 | Carregamento de variáveis de ambiente |
| pandas | >=2.0.0 | Manipulação e consolidação de dados |
| numpy | >=1.24.0 | Suporte numérico para análise |
| scipy | >=1.10.0 | Testes estatísticos e correlações |
| matplotlib | >=3.7.0 | Geração de gráficos |
| seaborn | >=0.12.0 | Visualizações estatísticas |

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
| **LCOM*** (Lack of Cohesion of Methods) | Razão | 0–1 | Falta de coesão entre métodos (normalizada). **Menor = Melhor** |

**Nota:** Utilizamos a versão normalizada LCOM* (0–1), mais confiável que o LCOM original. Para análise em nível de repositório, usamos **média, mediana e desvio padrão** das métricas por classe.

---

## 5. Desenho Experimental

### 5.1 Amostra

- **Tamanho:** 1.000 repositórios
- **Critério de seleção:** Top Java repositories por stars no GitHub
- **Período:** Snapshot 4 de abril de 2026
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
- **Python:** 3.14.3
- **Java:** 21.0.3
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
- **Período:** Snapshot em 04/04/2026
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
Sucesso: 974 repos (97.4%)
Excluído análise: 26 repos (2.6%)
  - CK failed: 26
```

### 8.3 Correção para Múltiplas Comparações

- Usar **Bonferroni correction** para 4 testes (RQ01-RQ04)
- Ajustar α = 0.05 / 4 = 0.0125
- Reportar p-valores brutos e corrigidos

---

## 9. Resultados Preliminares

### 9.1 Estatísticas Descritivas

**Métricas de Processo (n = 974):**

| Métrica | Média | Mediana | Desvio Padrão | Min | Max |
|---------|-------|---------|---------------|-----|-----|
| Stars | 9.442,41 | 5.786,50 | 10.714,38 | 3.473 | 125.017 |
| Releases | 41,01 | 11,00 | 89,95 | 0 | 1.000 |
| Idade (anos) | 10,14 | 10,31 | 3,18 | 0,56 | 17,47 |
| LOC_avg | 50,93 | 44,23 | 31,45 | 2,00 | 406,33 |

**Métricas de Qualidade (n = 974):**

| Métrica | Média | Mediana | Desvio Padrão | Min | Max |
|---------|-------|---------|---------------|-----|-----|
| CBO_avg | 5,38 | 5,33 | 1,87 | 0,00 | 21,89 |
| DIT_avg | 1,46 | 1,39 | 0,35 | 1,00 | 4,39 |
| LCOM*_avg | 0,24 | 0,25 | 0,09 | 0,00 | 0,75 |

### 9.2 Resultados por Questão de Pesquisa

#### RQ01: Popularidade vs. Qualidade

| Correlação | Spearman r | p-valor | Significância |
|-----------|------------|---------|---------------|
| Stars vs CBO_avg | 0,0273 | 3,94e-01 | Não significativo |
| Stars vs DIT_avg | −0,0439 | 1,71e-01 | Não significativo |
| Stars vs LCOM*_avg | −0,0093 | 7,72e-01 | Não significativo |

**Hipótese H1:** Repositórios mais populares devem ter melhor qualidade (menor CBO, DIT, LCOM*).

**Resultado:** **H1 rejeitada.** Não foram encontradas correlações estatisticamente significativas entre popularidade (stars) e nenhuma das métricas de qualidade (p > 0,05 em todos os casos). A popularidade de um repositório no GitHub não é um indicador de qualidade interna do código.

#### RQ02: Maturidade vs. Qualidade

| Correlação | Spearman r | p-valor | Significância |
|-----------|------------|---------|---------------|
| Idade vs CBO_avg | 0,0051 | 8,73e-01 | Não significativo |
| Idade vs DIT_avg | 0,2857 | 9,56e-20 | Significativo (p < 0,001) |
| Idade vs LCOM*_avg | 0,0010 | 9,75e-01 | Não significativo |

**Hipótese H2:** Repositórios mais maduros devem ter melhor qualidade (refatoração ao longo do tempo).

**Resultado:** **H2 parcialmente rejeitada.** A maturidade não mostrou correlação significativa com CBO (acoplamento) nem com LCOM* (coesão). Porém, repositórios mais antigos apresentam maior DIT (r=0,29, p < 0,001), sugerindo que projetos mais antigos tendem a acumular herança mais profunda. A ausência de correlação com LCOM* indica que a coesão não se degrada necessariamente com o tempo.

#### RQ03: Atividade vs. Qualidade

| Correlação | Spearman r | p-valor | Significância |
|-----------|------------|---------|---------------|
| Releases vs CBO_avg | 0,3997 | 1,16e-38 | Significativo (p < 0,001) |
| Releases vs DIT_avg | 0,2095 | 4,03e-11 | Significativo (p < 0,001) |
| Releases vs LCOM*_avg | 0,1847 | 6,36e-09 | Significativo (p < 0,001) |

**Hipótese H3:** Repositórios com mais releases devem ter melhor qualidade (maior atividade = melhor manutenção).

**Resultado:** **H3 rejeitada.** Todas as correlações são positivas e altamente significativas, indicando que projetos com mais releases apresentam **pior** qualidade interna: maior acoplamento (CBO, r=0,40), herança mais profunda (DIT, r=0,21) e menor coesão (LCOM*, r=0,18). Isso pode refletir que projetos mais ativos são também maiores e mais complexos.

#### RQ04: Tamanho vs. Qualidade

| Correlação | Spearman r | p-valor | Significância |
|-----------|------------|---------|---------------|
| LOC_avg vs CBO_avg | 0,4257 | 3,76e-44 | Significativo (p < 0,001) |
| LOC_avg vs DIT_avg | 0,3748 | 7,54e-34 | Significativo (p < 0,001) |
| LOC_avg vs LCOM*_avg | 0,5930 | 1,48e-93 | Significativo (p < 0,001) |

**Hipótese H4:** Repositórios maiores terão pior qualidade (maior LOC correlaciona com maior complexidade).

**Resultado:** **H4 confirmada.** Todas as correlações são positivas e altamente significativas. A correlação mais forte é entre LOC e LCOM* (r=0,59 — moderada a forte), seguida de LOC e CBO (r=0,43 — moderada) e LOC e DIT (r=0,37 — moderada). Classes maiores apresentam consistentemente pior coesão, maior acoplamento e herança mais profunda.

### 9.3 Gráficos Principais

#### Distribuição das Métricas de Qualidade

![Distribuição das Métricas de Qualidade](figures/distributions.png)

As distribuições revelam que CBO apresenta distribuição assimétrica à direita, com a maioria dos repositórios concentrada em valores baixos. DIT é fortemente concentrada próxima de 1, indicando que a maioria dos projetos utiliza pouca herança. LCOM* distribui-se de forma relativamente uniforme entre 0 e 0,5, com poucos repositórios acima de 0,6.

#### Correlações: LOC_avg vs Métricas de Qualidade

![Correlações LOC_avg vs Qualidade](figures/correlations_scatter.png)

Os scatter plots evidenciam a relação positiva entre tamanho do código (LOC) e as métricas de qualidade. A correlação mais forte é entre LOC e LCOM* (Spearman r=0,59), seguida de LOC e CBO (r=0,43) e LOC e DIT (r=0,38).

---

## 10. Discussão

### 10.1 Comparação entre Hipóteses e Resultados

| Hipótese | Expectativa | Resultado | Veredito |
|----------|------------|-----------|----------|
| **H1** (Popularidade → Qualidade) | Mais stars = melhor qualidade | Nenhuma correlação significativa | **Rejeitada** |
| **H2** (Maturidade → Qualidade) | Mais antigo = melhor qualidade | Apenas DIT aumenta com idade | **Parcialmente rejeitada** |
| **H3** (Atividade → Qualidade) | Mais releases = melhor qualidade | Mais releases = pior qualidade | **Rejeitada** |
| **H4** (Tamanho → Qualidade) | Maior LOC = pior qualidade | Todas as métricas pioram com LOC | **Confirmada** |

### 10.2 Interpretação dos Resultados

**Popularidade não indica qualidade (RQ01).** O número de estrelas reflete interesse da comunidade, utilidade percebida ou marketing do projeto — não a qualidade interna do código. Isso é consistente com a literatura, que sugere que stars medem popularidade social, não excelência técnica.

**Maturidade tem efeito limitado (RQ02).** A única correlação significativa foi entre idade e DIT (r=0,29). Projetos mais antigos acumulam hierarquias de herança mais profundas ao longo do tempo, possivelmente por extensões incrementais via subclasses. A ausência de correlação com CBO e LCOM* sugere que acoplamento e coesão são mais influenciados por decisões de design do que pelo tempo de existência do projeto.

**Atividade correlaciona com complexidade, não com qualidade (RQ03).** Projetos com mais releases tendem a ser maiores e mais complexos, o que explica as correlações positivas com CBO (r=0,40), DIT (r=0,21) e LCOM* (r=0,18). A hipótese de que mais releases implicaria melhor manutenção não se confirmou — provavelmente porque projetos ativos crescem em escopo, aumentando a complexidade estrutural.

**Tamanho é o melhor preditor de qualidade (RQ04).** LOC apresentou as correlações mais fortes e consistentes: LCOM* (r=0,59), CBO (r=0,43) e DIT (r=0,37). Classes maiores tendem a acumular mais responsabilidades (baixa coesão), mais dependências (alto acoplamento) e hierarquias mais profundas. Este resultado reforça o princípio do Single Responsibility e a importância de manter classes pequenas.

### 10.3 Limitações

1. **Snapshot único:** Os dados representam o estado dos repositórios em abril de 2026, sem análise temporal.
2. **Métricas agregadas:** Utilizamos médias por repositório, o que pode mascarar variações entre classes individuais.
3. **LCOM* normalizado:** Embora mais confiável que o LCOM original, a versão normalizada pode perder nuances em projetos muito grandes.
4. **26 repositórios excluídos:** 2,6% dos repositórios falharam na análise CK, potencialmente introduzindo viés de seleção.
5. **Causalidade:** Correlações não implicam causalidade — não podemos afirmar que LOC *causa* pior qualidade, apenas que estão associados.

---

## 11. Conclusão

Este estudo analisou 974 dos 1.000 repositórios Java mais populares do GitHub, investigando a relação entre métricas de processo (popularidade, maturidade, atividade e tamanho) e métricas de qualidade de código (CBO, DIT, LCOM*).

Os principais achados são:

1. **Tamanho do código (LOC) é o fator mais associado à qualidade interna**, com correlações moderadas a fortes com todas as métricas de qualidade analisadas.
2. **Atividade (releases) também se associa a piores métricas**, possivelmente como efeito indireto do crescimento do projeto.
3. **Popularidade (stars) não é um indicador confiável de qualidade de código.**
4. **Maturidade tem efeito limitado**, afetando apenas a profundidade de herança (DIT).

Para projetos que buscam manter boa qualidade interna, os resultados reforçam a importância de manter classes pequenas e focadas, independentemente da popularidade ou idade do repositório.

#### Matriz de Correlação de Spearman

![Matriz de Correlação](figures/correlation_heatmap.png)

A matriz de correlação mostra que todas as métricas de qualidade estão positivamente correlacionadas entre si, com destaque para LOC-LCOM* (r=0,59) e LOC-CBO (r=0,43). Isso sugere que a degradação de qualidade tende a ocorrer simultaneamente em múltiplas dimensões.

---

## 10. Discussão e Interpretação

### 10.1 Comparação com Hipóteses

| Hipótese | Resultado | Justificativa |
|----------|-----------|---------------|
| **H1**: Repos populares têm melhor qualidade | **Rejeitada** | Nenhuma correlação significativa entre stars e CBO, DIT ou LCOM* (p > 0,05) |
| **H2**: Repos mais maduros têm melhor qualidade | **Parcialmente rejeitada** | Sem correlação com CBO ou LCOM*, mas correlação positiva com DIT (r=0,29) — repos mais antigos têm herança mais profunda |
| **H3**: Mais releases = melhor qualidade | **Rejeitada** | Correlações positivas significativas com CBO (r=0,40), DIT (r=0,21) e LCOM* (r=0,18) — mais atividade = *pior* qualidade |
| **H4**: Repos maiores têm pior qualidade | **Confirmada** | Correlação moderada-forte LOC-LCOM* (r=0,59), moderada LOC-CBO (r=0,43) e LOC-DIT (r=0,37) |

### 10.2 Limitações (Ameaças à Validade)

#### Ameaças Internas
- **Vieses de seleção:** Apenas top-1000 repos (não representa espaço completo)
- **Confundidores:** Linguagem mista, código gerado, diferentes padrões
- **Falhas de CK:** 2.5% dos repos não puderam ser analisados

#### Ameaças Externas
- **Generalização:** Resultados valem apenas para Java? E outras linguagens?
- **Temporal:** Snapshot único (não captura evolução ao longo do tempo)
- **Contexto:** GitHub é plataforma específica

#### Ameaças de Construto
- **Métricas CBO/DIT/LCOM:** Proxies imperfeitos de qualidade
- **LOC:** Métrica bruta, não diferencia código bom vs. ruim
- **Releases:** Indica atividade, não necessariamente manutenção

### 10.3 Insights Principais

1. **Popularidade não é proxy de qualidade:** A quantidade de estrelas no GitHub não tem relação estatística com as métricas de qualidade interna do código. Projetos populares podem ter código bom ou ruim indistintamente.

2. **Tamanho é o principal preditor de degradação:** LOC apresentou as correlações mais fortes e consistentes com todas as métricas de qualidade (Spearman r entre 0,37 e 0,59), confirmando que classes maiores degradam sistematicamente em coesão, acoplamento e profundidade de herança.

3. **LCOM* tem distribuição relativamente uniforme:** A média (0,24) e a mediana (0,25) são próximas, indicando distribuição simétrica sem outliers extremos — ao contrário do LCOM original, que era altamente assimétrico.

4. **Atividade e maturidade correlacionam com pior qualidade:** Contrariando as hipóteses iniciais, projetos mais ativos (mais releases) e mais antigos tendem a ter herança mais profunda e maior acoplamento, possivelmente devido ao crescimento do escopo ao longo do tempo.

5. **Métricas de qualidade são intercorrelacionadas:** A matriz de correlação mostra que LCOM*, CBO e DIT se correlacionam positivamente, sugerindo que a degradação ocorre simultaneamente em múltiplas dimensões.

---

## 11. Conclusões e Recomendações

### 11.1 Findings Principais

Com base na análise de **974 repositórios Java** populares do GitHub:

1. **RQ01 — Popularidade vs. Qualidade:** Não há correlação significativa. A popularidade (stars) não prediz a qualidade interna do código.

2. **RQ02 — Maturidade vs. Qualidade:** Repositórios mais antigos apresentam herança mais profunda (DIT, r=0,29), mas sem impacto significativo no acoplamento (CBO) ou coesão (LCOM*).

3. **RQ03 — Atividade vs. Qualidade:** Projetos com mais releases têm pior qualidade em todas as métricas (CBO r=0,40; DIT r=0,21; LCOM* r=0,18), sugerindo crescimento de complexidade com a atividade.

4. **RQ04 — Tamanho vs. Qualidade:** O tamanho do código (LOC) é o preditor mais forte de degradação da qualidade, com correlação moderada-forte com LCOM* (r=0,59) e moderada com CBO (r=0,43) e DIT (r=0,37).

**Conclusão geral:** O tamanho das classes é o fator dominante na qualidade do código Java. Projetos devem priorizar classes menores e mais coesas para manter bons indicadores de qualidade interna.

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
timeout: 600s por repo

# Analysis
batch_size: 1 repo por vez (para economizar armazenamento em disco)
```

### B. Logs de Execução

**Resumo da execução:**
```
Total attempted: 1000
Clone successful: 1000 (100%)
Clone failed: 0 (0%)
Analysis successful: 974 (97.4%)
Analysis failed: 26 (2.6%)
```

**Matriz de falhas:**

| Tipo de Falha | Contagem | Repositórios Afetados |
|---------------|----------|---------------------|
| CK NullPointerException | 12 | elastic_elasticsearch, NationalSecurityAgency_ghidra, dbeaver_dbeaver, oracle_graal, thingsboard_thingsboard, questdb_questdb, Grasscutters_Grasscutter, neo4j_neo4j, projectlombok_lombok, trinodb_trino, haifengl_smile, JabRef_jabref |
| CK IOException | 3 | JetBrains_intellij-community, checkstyle_checkstyle, dragonwell-project_dragonwell8 |
| CK Runtime Warning/Error | 1 | openjdk_jdk |
| CK ArrayIndexOutOfBoundsException | 1 | google_j2objc |
| Metrics Extraction Empty | 9 | Snailclimb_JavaGuide, hollischuang_toBeTopJavaer, frank-lam_fullstack-tutorial, react-native-camera_react-native-camera, CoderLeixiaoshuai_java-eight-part, Archmage83_tvapk, RedSpider1_concurrent, jlegewie_zotfile, NotFound9_interviewGuide |

### C. Dados Brutos

[Ver arquivo: `data/processed/consolidated_metrics.csv` com 974 repositórios e 21 colunas de métricas]

---

## 14. Referências

1. **CK - Code Metrics:** Aniche, M. CK: A tool to compute class-level code metrics. Retrieved from [https://github.com/mauricioaniche/ck](https://github.com/mauricioaniche/ck)

---

**Versão:** 2.0.0 | **Data:** 10/04/2026 | **Status:** Revisado
