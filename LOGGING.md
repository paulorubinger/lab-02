# Sistema de Logging

Este projeto inclui um sistema de logging completo para rastrear falhas de clone e análise.

## 📋 O que é registrado

O sistema registra automaticamente:

### Clone Failures
- Repositório que falhou ao clonar
- Mensagem de erro do Git
- Timestamp da falha

### Analysis Failures
- Repositório que falhou durante análise
- Estágio da falha:
  - `ck_analysis` - Falha ao executar CK
  - `metrics_extraction` - Falha ao extrair métricas
  - `data_save` - Falha ao salvar dados
  - `process_repo` - Erro geral no processamento
- Mensagem de erro
- Timestamp da falha

## 📁 Estrutura dos Logs

Todos os logs são salvos em: `logs/processing_YYYYMMDD_HHMMSS.json`

### Exemplo de Arquivo de Log

```json
{
  "execution_timestamp": "2026-04-04T10:30:00.123456",
  "summary": {
    "total_attempted": 10,
    "clone_successful": 8,
    "clone_failed": 2,
    "analysis_successful": 7,
    "analysis_failed": 1
  },
  "clone_failures": [
    {
      "repo": "owner_repository",
      "timestamp": "2026-04-04T10:30:15.456789",
      "error": "fatal: unable to access repository: Connection timed out"
    }
  ],
  "analysis_failures": [
    {
      "repo": "owner_repository",
      "stage": "ck_analysis",
      "timestamp": "2026-04-04T10:35:20.789123",
      "error": "Java memory error: OutOfMemoryException"
    }
  ]
}
```

## 📊 Visualizando Logs

### Opção 1: Resumo Automático
O resumo é exibido automaticamente ao final da execução do pipeline:

```bash
python src/main.py
```

Output exemplo:
```
================================================================================
PROCESSING SUMMARY
================================================================================

Total attempted: 10
  Clone successful: 8
  Clone failures:   2
  Analysis successful: 7
  Analysis failures:   1

Success rates:
  Clone success rate:    80.0%
  Analysis success rate: 87.5%

❌ Clone failures (2):
  • owner_repo1: fatal: Connection timed out
  • owner_repo2: fatal: Could not resolve host

❌ Analysis failures (1):
  • owner_repo3 (ck_analysis): Java memory error
  
Log file: logs/processing_20260404_103000.json
================================================================================
```

### Opção 2: Visualizador Interativo

```bash
cd src/utils
python view_logs.py
```

Ou para ver um log específico:

```bash
python view_logs.py ../../logs/processing_20260404_103000.json
```

### Opção 3: Análise Manual

Abra o arquivo JSON em seu editor favorito para análise detalhada.

## 🔍 Analisando Resultados

### Taxa de Sucesso
- **Clone success rate**: % de clones bem-sucedidos
- **Analysis success rate**: % de análises bem-sucedidas

Fórmulas:
- Clone success rate = `clone_successful / (clone_successful + clone_failed) * 100`
- Analysis success rate = `analysis_successful / (analysis_successful + analysis_failed) * 100`

### Identificando Padrões

Procure por:
1. **Falhas comuns**: Mesmo erro em múltiplos repositórios
2. **Falhas intermitentes**: Erro que ocorre ocasionalmente
3. **Etapas críticas**: Em qual estágio as falhas ocorrem mais

### Próximos Passos Depois das Falhas

1. **Clone failures**: Tipicamente relacionado a rede/timeout
   - Pode tentar novamente mais tarde
   - Verificar conectividade

2. **CK analysis failures**: Pode ser erro de configuração Java ou timeout
   - Ajustar heap memory do Java
   - Aumentar timeout

3. **Metrics extraction failures**: Problema com formato de dados
   - Verificar se CK gerou arquivos de saída
   - Validar estrutura dos dados

## 📝 Integração com seu Código

O sistema de logging é automaticamente integrado em:
- `src/processing/batch_processor.py` - Rastreia análises
- `src/clone/clone_repositories.py` - Rastreia clones
- `src/main.py` - Inicializa logger e exibe resumo

Para usar programaticamente:

```python
from utils.processing_logger import ProcessingLogger

# Criar logger
logger = ProcessingLogger()

# Registrar falha
logger.log_clone_failure("owner_repo", "Connection timeout")

# Registrar sucesso
logger.log_clone_success("owner_repo")

# Registrar falha de análise
logger.log_analysis_failure("owner_repo", "ck_analysis", "Java error")

# Exibir resumo
logger.print_summary()
```

## 🛠️ Manipulação de Logs

### Carregar dados de um log

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.processing_logger import ProcessingLogger

log_data = ProcessingLogger.load_log("logs/processing_20260404_103000.json")
failures = log_data["clone_failures"]
```

### Listar todos os logs

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.processing_logger import ProcessingLogger

logs = ProcessingLogger.list_logs("logs")
print(logs)  # ['processing_20260404_103000.json', 'processing_20260404_110000.json', ...]
```

## 💡 Dicas

1. **Backup**: Mantenha logs do seu histórico de execução
2. **Comparação**: Compare logs de diferentes datas para verificar progresso
3. **Automação**: Use os logs para criar alerts ou scripts de recuperação
4. **Análise**: Importe os JSONs em ferramentas como pandas para análise estatística

---

Para mais informações, veja [README.md](README.md)
