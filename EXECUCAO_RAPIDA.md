# 🚀 SAEV - SCRIPTS DE EXECUÇÃO RÁPIDA

## 📊 Dashboards Disponíveis

### 1. 🦆 **Galeria com DuckDB** (MÁXIMA PERFORMANCE) ⚡
```bash
# Ambiente de teste com performance superior
python run_gallery_duckdb.py --env teste

# Ambiente de produção com DuckDB
python run_gallery_duckdb.py --env producao

# Migrar dados e executar
python run_gallery_duckdb.py --migrate --env teste
```
**URL**: http://localhost:8503  
**⚡ Performance**: 10-100x mais rápido que SQLite

---

### 2. 🎨 **Galeria de Painéis** (RECOMENDADO)
```bash
# Ambiente de teste (dados ofuscados)
python run_gallery.py --env teste

# Ambiente de produção (dados reais)
python run_gallery.py --env producao

# Auto-detecção de ambiente
python run_gallery.py
```
**URL**: http://localhost:8502

**🎯 Painéis Inclusos:**
- ✅ **Análise Detalhada por Filtros**: Investigação granular multi-filtros
- 🚧 **Dashboard Geral**: Visão panorâmica (em desenvolvimento)
- 🚧 **Análise por Escola**: Foco institucional (em desenvolvimento)
- 🚧 **Análise por Município**: Comparações regionais (em desenvolvimento)
- 🚧 **Análise Temporal**: Evolução histórica (em desenvolvimento)

---

### 3. ⭐ **Dashboard Star Schema** (Principal)
```bash
# Ambiente de teste
python run_dashboard.py --env teste

# Ambiente de produção
python run_dashboard.py --env producao
```
**URL**: http://localhost:8501

**📈 Funcionalidades:**
- Visão geral de desempenho
- Análise por município
- Análise por escola
- Análise de competências

---

## 🚀 Comparação de Performance

### 🦆 **DuckDB vs SQLite** - Benchmarks Reais:

| Operação | SQLite | DuckDB | Speedup |
|----------|---------|---------|---------|
| Contagem total | 0.036s | 0.001s | **36x** |
| Agregação por ano | 0.295s | 0.003s | **98x** |
| Top municípios | 0.380s | 0.005s | **76x** |
| JOINs complexos | 0.579s | 0.021s | **28x** |

**🎯 Recomendação**: Use DuckDB para análises com grandes volumes de dados!

---

## 💾 Preparação de Dados

### 1. **Carga de Dados - Ambiente de Teste**
```bash
python carga_teste.py
```
- Carrega e processa todos os CSVs de `data/raw/`
- Cria modelo Star Schema otimizado
- Ofusca dados sensíveis com MD5
- Banco: `db/avaliacao_teste.db`

### 2. **Carga de Dados - Ambiente de Produção**
```bash
python carga.py
```
- Carrega dados reais (sem ofuscação)
- Cria modelo Star Schema otimizado
- Banco: `db/avaliacao_prod.db`

### 3. **Aplicar Apenas Star Schema** (se já tem dados)
```bash
python apply_star_schema.py
```

---

## 🧪 Scripts de Desenvolvimento

```bash
# Testar filtros específicos
python test_filter.py

# Demonstrar funcionalidades ETL
python demo_funcionalidades.py

# Demonstrar Star Schema
python demo_star_schema.py

# Processo ETL completo
python demo_etl_process.py
```

---

## 📊 Estrutura do Star Schema

```
📊 TABELAS CRIADAS:
├── 👥 dim_aluno          # Dimensão de alunos únicos
├── 🏫 dim_escola         # Dimensão de escolas únicas
├── 🎯 dim_descritor      # Dimensão de competências
└── ⭐ fato_resposta_aluno # Tabela fato com métricas agregadas
```

**🚀 Performance**: Consultas 10-100x mais rápidas que modelo tradicional

---

## 🔄 Fluxo Recomendado

### Para Máxima Performance:
1. **Carregar dados**: `python carga_teste.py`
2. **Migrar para DuckDB**: `python duckdb_migration.py migrate teste`
3. **Galeria DuckDB**: `python run_gallery_duckdb.py --env teste`

### Para Novos Usuários:
1. **Carregar dados**: `python carga_teste.py`
2. **Abrir galeria**: `python run_gallery.py --env teste`
3. **Explorar painéis**: Começar com "Análise Detalhada por Filtros"

### Para Usuários Avançados:
1. **Dados produção**: `python carga.py`
2. **DuckDB produção**: `python run_gallery_duckdb.py --env producao`
3. **Dashboard principal**: `python run_dashboard.py --env producao`

---

## 🆘 Resolução de Problemas

### ❌ "Banco de dados não encontrado"
**Solução**: Execute primeiro um script de carga:
```bash
python carga_teste.py  # ou python carga.py
```

### ❌ "Star Schema não encontrado"
**Solução**: Aplique o Star Schema:
```bash
python apply_star_schema.py
```

### ❌ "Nenhum dado encontrado"
**Solução**: Verifique se existem arquivos CSV em `data/raw/`

### 🐛 Erro de porta ocupada
**Solução**: Use porta diferente:
```bash
python run_gallery.py --port 8503
python run_dashboard.py --port 8504
```

---

## 📁 Estrutura de Arquivos

```
oficinaIA/
├── 🎨 run_gallery.py          # Galeria de painéis
├── ⭐ run_dashboard.py         # Dashboard principal
├── 📊 carga_teste.py          # Carga ambiente teste
├── 📊 carga.py                # Carga ambiente produção
├── 🔧 apply_star_schema.py    # Aplicar Star Schema
├── 📋 GALERIA_PAINEIS.md      # Documentação da galeria
├── 📋 EXECUCAO_RAPIDA.md      # Este arquivo
├── src/dashboard/
│   ├── 🎨 gallery.py          # Código da galeria
│   └── ⭐ main.py             # Dashboard Star Schema
├── src/data/
│   ├── 🔄 etl.py              # ETL otimizado
│   └── ⭐ star_schema.py      # Criação Star Schema
├── data/raw/                  # CSVs fonte
└── db/                        # Bancos SQLite
```

---

**🎯 Dica**: Comece sempre pela **Galeria de Painéis** para ter acesso a todas as funcionalidades disponíveis!
