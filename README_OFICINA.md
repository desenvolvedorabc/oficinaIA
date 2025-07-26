# 🎓 Oficina de IA - Sistema SAEV
## Dashboard de Análise Educacional com SQLite e DuckDB

---

## 📋 O que você vai aprender

Nesta oficina, você irá:
- ✅ Configurar um ambiente Python completo
- ✅ Trabalhar com **SQLite** (tradicional) e **DuckDB** (alta performance)
- ✅ Criar dashboards interativos com **Streamlit**
- ✅ Implementar **ETL** (Extract, Transform, Load)
- ✅ Comparar performance entre bancos de dados
- ✅ Aplicar **Star Schema** para análise de dados

---

## 🚀 Início Rápido (Windows)

### 1️⃣ Verificar Ambiente
```cmd
verificar_ambiente.bat
```

### 2️⃣ Instalar Dependências
```cmd
pip install -r requirements_oficina.txt
```

### 3️⃣ Processar Dados
```cmd
python carga_teste.py
python duckdb_migration.py migrate teste
```

### 4️⃣ Iniciar Dashboard
```cmd
galeria.bat
```

---

## 📁 Estrutura do Projeto

```
oficinaIA/
├── 📖 INSTALACAO_WINDOWS.md    # Guia detalhado de instalação
├── 🚀 galeria.bat             # Launcher para Windows
├── 🔍 verificar_ambiente.bat  # Verificação do ambiente
├── 📦 requirements_oficina.txt # Dependências da oficina
│
├── 📊 DASHBOARDS
│   ├── run_gallery_duckdb.py  # Dashboard com DuckDB (rápido)
│   └── run_gallery.py         # Dashboard com SQLite (compatível)
│
├── 🔄 ETL & MIGRAÇÃO
│   ├── carga_teste.py         # Carregar dados de teste
│   ├── carga.py               # Carregar dados de produção
│   └── duckdb_migration.py    # Migrar SQLite → DuckDB
│
├── 🗄️ BANCOS DE DADOS
│   ├── db/avaliacao_teste.db     # SQLite teste
│   ├── db/avaliacao_teste.duckdb # DuckDB teste
│   ├── db/avaliacao_prod.db      # SQLite produção
│   └── db/avaliacao_prod.duckdb  # DuckDB produção
│
└── 📈 ANÁLISES & DEMOS
    ├── demo_duckdb_vs_sqlite.py  # Benchmark de performance
    ├── demo_etl_completo.py      # Demo ETL completo
    └── Tutorial_SAEV_*.ipynb     # Jupyter Notebooks
```

---

## 🎯 Exercícios da Oficina

### 🔰 **Nível Iniciante**
1. **Configuração do Ambiente**
   - Instalar Python, SQLite e DuckDB
   - Verificar instalação com `verificar_ambiente.bat`

2. **Primeiro Dashboard**
   - Executar `python carga_teste.py`
   - Iniciar galeria com `galeria.bat`
   - Explorar diferentes painéis

### 🔥 **Nível Intermediário**
3. **Comparação de Performance**
   - Executar `python demo_duckdb_vs_sqlite.py`
   - Comparar tempos de execução
   - Analisar diferenças de performance

4. **Migração de Dados**
   - Migrar dados para DuckDB
   - Comparar dashboards SQLite vs DuckDB
   - Observar melhorias de velocidade

### 🚀 **Nível Avançado**
5. **Star Schema**
   - Entender a estrutura dimensional
   - Analisar queries otimizadas
   - Criar novos indicadores

6. **ETL Personalizado**
   - Modificar `carga_teste.py`
   - Adicionar novos campos
   - Testar pipeline completo

---

## 📊 Resultados Esperados

Ao final da oficina, você terá:

| Funcionalidade | SQLite | DuckDB |
|----------------|---------|---------|
| **Dashboard Básico** | ✅ 3-5s | ✅ <1s |
| **Filtros Complexos** | ⚠️ 8-15s | ✅ 1-2s |
| **Agregações** | ⚠️ 10-20s | ✅ 1-3s |
| **Exportações** | ⚠️ 15-30s | ✅ 2-5s |

### 🎯 **Performance Esperada**
- **SQLite**: Adequado para datasets pequenos (<100k registros)
- **DuckDB**: Excelente para datasets grandes (>1M registros)
- **Speedup**: 10x a 190x mais rápido com DuckDB

---

## 🛠️ Comandos Úteis

### Verificação Rápida
```cmd
# Verificar instalação completa
verificar_ambiente.bat

# Testar módulos Python
python -c "import sqlite3, duckdb, pandas, streamlit; print('✅ OK')"

# Ver versões
python --version
python -c "import duckdb; print(duckdb.__version__)"
```

### Processamento de Dados
```cmd
# Dados de teste (rápido)
python carga_teste.py

# Migrar para DuckDB
python duckdb_migration.py migrate teste

# Dados de produção (mais demorado)
python carga.py
python duckdb_migration.py migrate prod
```

### Dashboards
```cmd
# Via script auxiliar (recomendado)
galeria.bat

# Direto (alternativo)
python run_gallery_duckdb.py --env teste --port 8504
python run_gallery.py --env teste --port 8504
```

### Análises
```cmd
# Benchmark de performance
python demo_duckdb_vs_sqlite.py

# Status dos ambientes
python manage_env.py status

# Demo ETL completo
python demo_etl_completo.py
```

---

## 🆘 Resolução de Problemas

### ❌ **Python não encontrado**
```cmd
# Verificar se Python está no PATH
python --version

# Se não funcionar, reinstale marcando "Add to PATH"
```

### ❌ **DuckDB não instala**
```cmd
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Instalar DuckDB
pip install duckdb --upgrade
```

### ❌ **Dashboard não carrega**
```cmd
# Verificar se os dados foram processados
dir db\*.db
dir db\*.duckdb

# Reprocessar se necessário
python carga_teste.py
python duckdb_migration.py migrate teste
```

### ❌ **Porta ocupada**
```cmd
# Usar portas alternativas
python run_gallery_duckdb.py --env teste --port 8506
```

---

## 📚 Recursos Adicionais

### 📖 **Documentação**
- [INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md) - Guia completo de instalação
- [PADRONIZACAO_DUCKDB.md](PADRONIZACAO_DUCKDB.md) - Padrões DuckDB
- [README.md](README.md) - Documentação principal do projeto

### 🎓 **Tutoriais Interativos**
- `Tutorial_SAEV_Relatórios_e_Análises.ipynb` - Jupyter Notebook completo

### 🔧 **Scripts de Demo**
- `demo_funcionalidades.py` - Demonstração de funcionalidades
- `demo_sql_duckdb.py` - Exemplos de SQL com DuckDB
- `demo_star_schema.py` - Explicação do modelo dimensional

---

## 🎯 Metas da Oficina

**✅ Meta Mínima**: Conseguir executar o dashboard básico
**🔥 Meta Intermediária**: Comparar SQLite vs DuckDB
**🚀 Meta Avançada**: Entender e modificar o pipeline ETL

---

## 👥 Suporte Durante a Oficina

**🙋‍♀️ Dúvidas?** Levante a mão!

**🐛 Encontrou um bug?** Chame o instrutor!

**💡 Ideia interessante?** Compartilhe com a turma!

---

**🚀 Vamos começar! Boa oficina! 🎓**
