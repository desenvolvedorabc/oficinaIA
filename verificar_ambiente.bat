@echo off
REM Script de verificação rápida do ambiente SAEV para Windows
REM Uso: verificar_ambiente.bat

echo.
echo ========================================
echo    VERIFICAÇÃO DO AMBIENTE SAEV
echo ========================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✅ Python OK
) else (
    echo ❌ Python não encontrado! Instale o Python primeiro.
    echo 💡 Baixe em: https://www.python.org/downloads/
    goto erro
)
echo.

REM Verificar pip
echo [2/6] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip OK
) else (
    echo ❌ pip não encontrado!
    goto erro
)
echo.

REM Verificar módulos Python essenciais
echo [3/6] Verificando módulos Python...
python -c "import sqlite3; print('✅ SQLite3:', sqlite3.sqlite_version)" 2>nul || echo ❌ SQLite3 não disponível
python -c "import duckdb; print('✅ DuckDB:', duckdb.__version__)" 2>nul || echo ❌ DuckDB não instalado - Execute: pip install duckdb
python -c "import pandas; print('✅ Pandas:', pandas.__version__)" 2>nul || echo ❌ Pandas não instalado - Execute: pip install pandas
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)" 2>nul || echo ❌ Streamlit não instalado - Execute: pip install streamlit
echo.

REM Verificar estrutura de diretórios
echo [4/6] Verificando estrutura de diretórios...
if exist "db\" (
    echo ✅ Diretório db\ existe
) else (
    echo ⚠️  Diretório db\ não existe - será criado automaticamente
    mkdir db
)

if exist "data\" (
    echo ✅ Diretório data\ existe
) else (
    echo ❌ Diretório data\ não encontrado
)

if exist "src\" (
    echo ✅ Diretório src\ existe
) else (
    echo ❌ Diretório src\ não encontrado
)
echo.

REM Verificar scripts principais
echo [5/6] Verificando scripts principais...
if exist "carga_teste.py" (
    echo ✅ carga_teste.py
) else (
    echo ❌ carga_teste.py não encontrado
)

if exist "duckdb_migration.py" (
    echo ✅ duckdb_migration.py
) else (
    echo ❌ duckdb_migration.py não encontrado
)

if exist "run_gallery_duckdb.py" (
    echo ✅ run_gallery_duckdb.py
) else (
    echo ❌ run_gallery_duckdb.py não encontrado
)

if exist "requirements.txt" (
    echo ✅ requirements.txt
) else (
    echo ❌ requirements.txt não encontrado
)
echo.

REM Verificar bancos de dados
echo [6/6] Verificando bancos de dados...
if exist "db\avaliacao_teste.db" (
    for %%A in ("db\avaliacao_teste.db") do echo ✅ SQLite Teste (%%~zA bytes)
) else (
    echo ⚠️  SQLite Teste não encontrado - Execute: python carga_teste.py
)

if exist "db\avaliacao_teste.duckdb" (
    for %%A in ("db\avaliacao_teste.duckdb") do echo ✅ DuckDB Teste (%%~zA bytes)
) else (
    echo ⚠️  DuckDB Teste não encontrado - Execute: python duckdb_migration.py migrate teste
)

if exist "db\avaliacao_prod.db" (
    for %%A in ("db\avaliacao_prod.db") do echo ✅ SQLite Produção (%%~zA bytes)
) else (
    echo ⚠️  SQLite Produção não encontrado - Execute: python carga.py
)

if exist "db\avaliacao_prod.duckdb" (
    for %%A in ("db\avaliacao_prod.duckdb") do echo ✅ DuckDB Produção (%%~zA bytes)
) else (
    echo ⚠️  DuckDB Produção não encontrado - Execute: python duckdb_migration.py migrate prod
)
echo.

echo ========================================
echo         VERIFICAÇÃO CONCLUÍDA
echo ========================================
echo.
echo 🚀 Para iniciar a galeria, execute:
echo    galeria.bat
echo.
echo 📚 Para ver o guia completo:
echo    type INSTALACAO_WINDOWS.md
echo.
goto fim

:erro
echo.
echo ========================================
echo           ERRO ENCONTRADO
echo ========================================
echo.
echo ❌ Corrija os problemas acima antes de continuar.
echo 📖 Consulte o arquivo INSTALACAO_WINDOWS.md para instruções detalhadas.
echo.

:fim
pause
