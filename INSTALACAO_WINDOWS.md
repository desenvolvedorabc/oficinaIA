# 🪟 Guia de Instalação - Windows

## 📋 Pré-requisitos para Oficina de IA

Este guia irá orientá-lo na instalação do ambiente necessário para executar o projeto SAEV em sistemas Windows.

---

## 🐍 1. Instalação do Python

### Opção A: Python.org (Recomendado)
1. Acesse: https://www.python.org/downloads/
2. Baixe a versão mais recente do Python 3.11 ou 3.12
3. **IMPORTANTE**: Durante a instalação, marque:
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users" (opcional)
4. Execute a instalação como Administrador

### Opção B: Microsoft Store
1. Abra a Microsoft Store
2. Procure por "Python 3.11" ou "Python 3.12"
3. Clique em "Instalar"

### Verificação da Instalação
Abra o **Prompt de Comando** (`cmd`) ou **PowerShell** e execute:
```cmd
python --version
pip --version
```

---

## 🗄️ 2. Instalação do SQLite

### SQLite já vem com Python! ✅
O SQLite já está incluído na instalação padrão do Python, então **não é necessário instalar separadamente**.

### Verificação do SQLite
Execute no terminal:
```cmd
python -c "import sqlite3; print('SQLite versão:', sqlite3.sqlite_version)"
```

### (Opcional) SQLite Command Line Tools
Se quiser usar o SQLite diretamente pelo terminal:
1. Acesse: https://www.sqlite.org/download.html
2. Baixe "sqlite-tools-win32-x86-XXXXXXX.zip"
3. Extraia para uma pasta (ex: `C:\sqlite`)
4. Adicione a pasta ao PATH do Windows

---

## 🦆 3. Instalação do DuckDB

### Via pip (Recomendado)
Execute no **Prompt de Comando** ou **PowerShell**:
```cmd
pip install duckdb
```

### Verificação do DuckDB
```cmd
python -c "import duckdb; print('DuckDB versão:', duckdb.__version__)"
```

### (Opcional) DuckDB CLI
Para usar o DuckDB diretamente pelo terminal:
1. Acesse: https://github.com/duckdb/duckdb/releases
2. Baixe "duckdb_cli-windows-amd64.zip"
3. Extraia para uma pasta (ex: `C:\duckdb`)
4. Adicione a pasta ao PATH do Windows

---

## 🔧 4. Configuração do Ambiente do Projeto

### 4.1 Baixar o Projeto
```cmd
git clone https://github.com/desenvolvedorabc/oficinaIA.git
cd oficinaIA
```

### 4.2 Criar Ambiente Virtual (Recomendado)
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4.3 Instalar Dependências
```cmd
pip install -r requirements.txt
```

### 4.4 Verificar Instalação
```cmd
python -c "import sqlite3, duckdb, pandas, streamlit; print('✅ Todos os módulos instalados!')"
```

---

## 🚀 5. Executando o Projeto

### 5.1 Processar Dados de Teste
```cmd
python carga_teste.py
```

### 5.2 Migrar para DuckDB
```cmd
python duckdb_migration.py migrate teste
```

### 5.3 Iniciar Galeria
```cmd
python run_gallery_duckdb.py --env teste --port 8504
```

Ou use o script auxiliar:
```cmd
# No Windows, pode ser necessário usar bash se disponível
bash galeria.sh

# Ou execute diretamente:
python run_gallery_duckdb.py --env teste --port 8504
```

---

## 🔍 6. Solução de Problemas Comuns

### Problema: "python não é reconhecido"
**Solução**: Python não foi adicionado ao PATH
1. Reinstale o Python marcando "Add to PATH"
2. Ou adicione manualmente: `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\`

### Problema: "pip não é reconhecido"
**Solução**: 
```cmd
python -m pip install --upgrade pip
```

### Problema: Erro de permissão
**Solução**: Execute o Prompt de Comando como Administrador

### Problema: Erro ao instalar duckdb
**Solução**: Atualize o pip e tente novamente
```cmd
python -m pip install --upgrade pip
pip install duckdb --upgrade
```

### Problema: Módulo não encontrado
**Solução**: Certifique-se de estar no ambiente virtual correto
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 7. Testando a Performance

### Comparar SQLite vs DuckDB
```cmd
python demo_duckdb_vs_sqlite.py
```

### Verificar Status dos Bancos
```cmd
python manage_env.py status
```

---

## 🛠️ 8. Ferramentas Adicionais (Opcional)

### Git para Windows
1. Baixe em: https://git-scm.com/download/win
2. Durante instalação, escolha "Git from the command line and also from 3rd-party software"

### Visual Studio Code
1. Baixe em: https://code.visualstudio.com/
2. Instale extensões recomendadas:
   - Python
   - SQLite Viewer
   - Git Graph

### Windows Terminal (Moderno)
1. Instale pela Microsoft Store
2. Oferece melhor experiência que o CMD tradicional

---

## 📝 9. Comandos de Verificação Final

Execute estes comandos para confirmar que tudo está funcionando:

```cmd
# Verificar Python e módulos
python --version
python -c "import sqlite3, duckdb, pandas, streamlit; print('✅ Ambiente OK!')"

# Verificar bancos de dados
dir db\*.db
dir db\*.duckdb

# Testar galeria (se os dados já foram processados)
python run_gallery_duckdb.py --env teste --port 8504
```

---

## 🆘 10. Suporte Durante a Oficina

Se encontrar problemas durante a oficina:

1. **Verifique o ambiente virtual**: `venv\Scripts\activate`
2. **Reinstale dependências**: `pip install -r requirements.txt`
3. **Execute diagnóstico**: `python manage_env.py status`
4. **Peça ajuda**: Levante a mão! 🙋‍♀️🙋‍♂️

---

## 🎯 Resultado Esperado

Ao final da instalação, você deve conseguir:
- ✅ Executar `python --version` e ver Python 3.11+
- ✅ Importar sqlite3 e duckdb sem erros
- ✅ Processar dados com `carga_teste.py`
- ✅ Migrar dados com `duckdb_migration.py`
- ✅ Visualizar dashboards em `http://localhost:8504`

---

**🚀 Boa oficina e bons estudos!**
