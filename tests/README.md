# Test Scripts

Teste scripts para validar o batch processor com poucos repositórios antes de processar 1000.

## 📋 Scripts Disponíveis

### 1. `test_batch_processor.py` - Processar Repositórios de Teste
Processa N repositórios mantendo os arquivos gerados para inspeção.

**Uso (da raiz do projeto):**
```powershell
# Testar com 1 repositório
python tests/test_batch_processor.py 1

# Testar com 3 repositórios
python tests/test_batch_processor.py 3

# Testar com 5 repositórios
python tests/test_batch_processor.py 5
```

**Uso (de dentro da pasta tests/):**
```powershell
cd tests
python test_batch_processor.py 1
```

**O que faz:**
- ✓ Clone com --depth 1 (shallow clone)
- ✓ Remove pasta se já existe (de teste anterior)
- ✓ Executa CK analysis
- ✓ Extrai e salva métricas
- ✓ **MANTÉM** repos e metrics para inspeção
- ✓ Mostra detalhes de erro (se houver)

### 2. `inspect_test_data.py` - Visualizar Arquivos Gerados
Inspeciona resultados dos testes sem modificar nada.

**Uso (da raiz do projeto):**
```powershell
python tests/inspect_test_data.py
```

**Uso (de dentro da pasta tests/):**
```powershell
cd tests
python inspect_test_data.py
```

**Mostra:**
- 📁 Repositórios clonados (tamanho em MB)
- 📊 Estrutura de métricas CK
  - `class.csv` - métricas de classe
  - `method.csv` - métricas de método
- 📈 Preview do CSV consolidado
- ✓ Repositórios já processados (progress)

### 3. `cleanup_test_data.py` - Limpar Dados de Teste
Remove todos os arquivos de teste gerados.

**Uso (da raiz do projeto):**
```powershell
# Só visualiza o que será deletado
python tests/cleanup_test_data.py

# REALMENTE deleta os arquivos
python tests/cleanup_test_data.py --confirm
```

**Uso (de dentro da pasta tests/):**
```powershell
cd tests
# Visualiza
python cleanup_test_data.py

# Deleta
python cleanup_test_data.py --confirm
```

## 🔄 Workflow Recomendado

### Passo 1: Teste Inicial
```powershell
python tests/test_batch_processor.py 1
```

Resultado esperado:
```
[1/1] Processing owner_repo
  Cloning... repo_name
  Running CK analysis...
  Extracting metrics...
  ✓ Metrics saved
  ✓ Completed

TEST RESULTS: 1/1 repositories processed successfully
```

### Passo 2: Inspecione os Arquivos
```powershell
python tests/inspect_test_data.py
```

Isso mostra:
- Pastas clonadas em `repos/`
- CSVs do CK em `data/raw/ck_metrics/`
- Dados consolidados em `data/processed/test_consolidated_metrics.csv`
- Progresso em `data/processed/test_progress.txt`

### Passo 3: Limpe (se tudo OK)
```powershell
python tests/cleanup_test_data.py --confirm
```

### Passo 4: Processe 1000 Repositórios
```powershell
python src/main.py
```

## 🐛 Se Houver Erro do CK

O teste mostra detalhes:
```
ERROR: CK analysis failed
  stdout: [detalhes do CK]
  stderr: [erros do CK]
```

**Causas comuns:**
1. Java não instalado → instale JDK
2. `ck.jar` não encontrado → baixe em https://github.com/mauricioaniche/ck
3. Repositório sem código Java → ignora e continua

## 📂 Estrutura de Arquivos Gerados

```
LAB-02/
├── repos/                    # Repositórios clonados (com --depth 1)
│   ├── owner_repo1/
│   └── owner_repo2/
├── data/
│   ├── raw/
│   │   └── ck_metrics/       # Saída do CK (class.csv, method.csv)
│   │       ├── owner_repo1/
│   │       └── owner_repo2/
│   └── processed/
│       ├── test_consolidated_metrics.csv  # Métricas agregadas
│       └── test_progress.txt              # Qual repos já foi processado
└── tests/
    ├── test_batch_processor.py
    ├── inspect_test_data.py
    └── cleanup_test_data.py
```

## 💡 Dicas

- **Não deletar manualmente**: Use `cleanup_test_data.py --confirm`
- **Retomar interrompido**: O `progress.txt` rastreia qual repos já foi processado
- **Ver erros detalhados**: Use `verbose=True` no test (já está habilitado)
- **Vários testes**: Limpe entre cada teste com cleanup_test_data.py

## ✅ Checklist para ir para produção

- [ ] Teste com 1 repo: `python test_batch_processor.py 1`
- [ ] Veja resultado: `python inspect_test_data.py`
- [ ] Limpe: `python cleanup_test_data.py --confirm`
- [ ] Teste com 3 repos: `python test_batch_processor.py 3`
- [ ] Veja resultado novamente
- [ ] Limpe novamente
- [ ] Inicie processamento 1000: `python src/main.py`
