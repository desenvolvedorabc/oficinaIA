@echo off
setlocal EnableDelayedExpansion

REM Script de ajuda para inicializar a Galeria de Painéis SAEV no Windows
REM Uso: galeria.bat

REM Cores para output (limitadas no CMD)
set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "CYAN=[36m"
set "PURPLE=[35m"
set "MAGENTA=[95m"
set "NC=[0m"

echo.
echo   ████████╗ █████╗ ██╗     ███████╗██████╗ ██╗ █████╗ 
echo   ╚══██╔══╝██╔══██╗██║     ██╔════╝██╔══██╗██║██╔══██╗
echo      ██║   ███████║██║     █████╗  ██████╔╝██║███████║
echo      ██║   ██╔══██║██║     ██╔══╝  ██╔══██╗██║██╔══██║
echo      ██║   ██║  ██║███████╗███████╗██║  ██║██║██║  ██║
echo      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
echo.
echo 🖼️  Galeria de Painéis de Análise Educacional
echo =============================================
echo.

REM Verificar status dos ambientes
echo 📊 Verificando ambientes disponíveis...
echo.

REM Verificar bancos SQLite
set "TESTE_SQLITE_STATUS=❌ SQLite"
if exist "db\avaliacao_teste.db" set "TESTE_SQLITE_STATUS=✅ SQLite"

set "PROD_SQLITE_STATUS=❌ SQLite"
if exist "db\avaliacao_prod.db" set "PROD_SQLITE_STATUS=✅ SQLite"

REM Verificar bancos DuckDB
set "TESTE_DUCKDB_STATUS=❌ DuckDB"
if exist "db\avaliacao_teste.duckdb" set "TESTE_DUCKDB_STATUS=✅ DuckDB"

set "PROD_DUCKDB_STATUS=❌ DuckDB"
if exist "db\avaliacao_prod.duckdb" set "PROD_DUCKDB_STATUS=✅ DuckDB"

echo 🧪 Ambiente de TESTE:     !TESTE_SQLITE_STATUS! ^| !TESTE_DUCKDB_STATUS!
echo 🔴 Ambiente de PRODUÇÃO: !PROD_SQLITE_STATUS! ^| !PROD_DUCKDB_STATUS!
echo.

REM Verificar se existe run_gallery_duckdb.py
set "GALLERY_STATUS=❌ Não encontrado"
if exist "run_gallery_duckdb.py" set "GALLERY_STATUS=✅ Disponível"

echo 🖼️  Galeria de Painéis:   !GALLERY_STATUS!
echo.

REM Menu de opções
echo 🚀 Escolha uma opção:
echo.
echo 1^) Galeria TESTE com DuckDB (recomendado - máxima performance^)
echo 2^) Galeria TESTE com SQLite (compatibilidade^)
echo 3^) Galeria PRODUÇÃO com DuckDB (dados reais - máxima performance^)
echo 4^) Galeria PRODUÇÃO com SQLite (dados reais - compatibilidade^)
echo 5^) Benchmark de Performance (comparar SQLite vs DuckDB^)
echo 6^) Verificar status detalhado dos ambientes
echo 7^) Migrar SQLite para DuckDB
echo 8^) Mostrar ajuda da galeria
echo 9^) Sair
echo.

set /p "opcao=Digite sua escolha (1-9): "

if "%opcao%"=="1" goto teste_duckdb
if "%opcao%"=="2" goto teste_sqlite
if "%opcao%"=="3" goto prod_duckdb
if "%opcao%"=="4" goto prod_sqlite
if "%opcao%"=="5" goto benchmark
if "%opcao%"=="6" goto status
if "%opcao%"=="7" goto migrar
if "%opcao%"=="8" goto ajuda
if "%opcao%"=="9" goto sair
goto opcao_invalida

:teste_duckdb
echo.
echo 🖼️  Iniciando Galeria TESTE com DuckDB...
echo ✨ Performance otimizada para análises complexas
echo.
if not exist "run_gallery_duckdb.py" (
    echo ❌ Script run_gallery_duckdb.py não encontrado!
    goto fim
)
if not exist "db\avaliacao_teste.duckdb" (
    echo ⚠️  Banco DuckDB de teste não encontrado!
    echo 💡 Execute: python duckdb_migration.py migrate teste
    goto fim
)
echo 🔗 URL: http://localhost:8504
echo 💡 Abrindo navegador automaticamente...
start "" "http://localhost:8504"
python run_gallery_duckdb.py --env teste --port 8504
goto fim

:teste_sqlite
echo.
echo 🖼️  Iniciando Galeria TESTE com SQLite...
echo ⚠️  Performance limitada para análises complexas
echo.
if not exist "run_gallery.py" (
    echo ❌ Script run_gallery.py não encontrado!
    goto fim
)
if not exist "db\avaliacao_teste.db" (
    echo ⚠️  Banco SQLite de teste não encontrado!
    echo 💡 Execute: python carga_teste.py
    goto fim
)
echo 🔗 URL: http://localhost:8504
echo 💡 Abrindo navegador automaticamente...
start "" "http://localhost:8504"
python run_gallery.py --env teste --port 8504
goto fim

:prod_duckdb
echo.
echo 🖼️  Iniciando Galeria PRODUÇÃO com DuckDB...
echo ✨ Performance otimizada para dados reais
echo ⚠️  ATENÇÃO: Dados reais sensíveis!
echo.
set /p "confirm=Confirma inicialização em PRODUÇÃO? (s/N): "
if /i not "%confirm%"=="s" (
    echo ✅ Operação cancelada
    goto fim
)
if not exist "run_gallery_duckdb.py" (
    echo ❌ Script run_gallery_duckdb.py não encontrado!
    goto fim
)
if not exist "db\avaliacao_prod.duckdb" (
    echo ⚠️  Banco DuckDB de produção não encontrado!
    echo 💡 Execute: python duckdb_migration.py migrate prod
    goto fim
)
echo 🔗 URL: http://localhost:8505
echo 💡 Abrindo navegador automaticamente...
start "" "http://localhost:8505"
python run_gallery_duckdb.py --env producao --port 8505
goto fim

:prod_sqlite
echo.
echo 🖼️  Iniciando Galeria PRODUÇÃO com SQLite...
echo ⚠️  Performance limitada + dados reais sensíveis!
echo.
set /p "confirm=Confirma inicialização em PRODUÇÃO com SQLite? (s/N): "
if /i not "%confirm%"=="s" (
    echo ✅ Operação cancelada
    goto fim
)
if not exist "run_gallery.py" (
    echo ❌ Script run_gallery.py não encontrado!
    goto fim
)
if not exist "db\avaliacao_prod.db" (
    echo ⚠️  Banco SQLite de produção não encontrado!
    echo 💡 Execute: python carga.py
    goto fim
)
echo 🔗 URL: http://localhost:8505
echo 💡 Abrindo navegador automaticamente...
start "" "http://localhost:8505"
python run_gallery.py --env producao --port 8505
goto fim

:benchmark
echo.
echo 🏁 Executando Benchmark de Performance...
echo.
if not exist "demo_duckdb_vs_sqlite.py" (
    echo ❌ Script demo_duckdb_vs_sqlite.py não encontrado!
    goto fim
)
python demo_duckdb_vs_sqlite.py
goto fim

:status
echo.
echo 📊 Status detalhado dos ambientes:
echo.
python -c "import sys; print('Python:', sys.version)" 2>nul || echo ❌ Python não encontrado!
python manage_env.py status 2>nul || echo ❌ Script manage_env.py não encontrado!
echo.
echo 🦆 Status DuckDB:
if exist "db\avaliacao_teste.duckdb" (
    for %%A in ("db\avaliacao_teste.duckdb") do echo    🧪 Teste: ✅ Disponível (%%~zA bytes)
) else (
    echo    🧪 Teste: ❌ Não encontrado
)
if exist "db\avaliacao_prod.duckdb" (
    for %%A in ("db\avaliacao_prod.duckdb") do echo    🔴 Prod:  ✅ Disponível (%%~zA bytes)
) else (
    echo    🔴 Prod:  ❌ Não encontrado
)
goto fim

:migrar
echo.
echo 🔄 Migrando SQLite para DuckDB...
echo.
echo Escolha o ambiente para migrar:
echo 1^) Migrar ambiente de TESTE
echo 2^) Migrar ambiente de PRODUÇÃO
echo 3^) Voltar ao menu principal
echo.
set /p "migrate_option=Digite sua escolha (1-3): "

if "%migrate_option%"=="1" (
    echo.
    echo 🔄 Migrando ambiente de TESTE...
    if exist "duckdb_migration.py" (
        python duckdb_migration.py migrate teste
    ) else (
        echo ❌ Script duckdb_migration.py não encontrado!
    )
    goto fim
)
if "%migrate_option%"=="2" (
    echo.
    echo 🔄 Migrando ambiente de PRODUÇÃO...
    echo ⚠️  ATENÇÃO: Operação em dados de produção!
    set /p "confirm_migrate=Confirma migração de PRODUÇÃO? (s/N): "
    if /i "!confirm_migrate!"=="s" (
        if exist "duckdb_migration.py" (
            python duckdb_migration.py migrate prod
        ) else (
            echo ❌ Script duckdb_migration.py não encontrado!
        )
    ) else (
        echo ✅ Migração cancelada
    )
    goto fim
)
if "%migrate_option%"=="3" (
    echo ↩️  Voltando ao menu principal...
    goto fim
)
echo ❌ Opção inválida: %migrate_option%
goto fim

:ajuda
echo.
echo 📖 Ajuda da Galeria de Painéis:
echo.
echo 🖼️  GALERIA DE PAINÉIS
echo A galeria oferece múltiplos painéis especializados:
echo.
echo 📊 Painéis Disponíveis:
echo    • Dashboard Principal (visão geral)
echo    • Análise Detalhada (filtros avançados)
echo    • Comparativo de Desempenho
echo    • Análise por Competências
echo    • Relatórios Executivos
echo.
echo 🚀 Performance:
echo    • DuckDB: 10-190x mais rápido que SQLite
echo    • SQLite: Compatibilidade total
echo.
echo 📱 Acesso:
echo    • Teste:    http://localhost:8504
echo    • Produção: http://localhost:8505
echo.
echo 🔧 Scripts Relacionados:
echo    • python run_gallery_duckdb.py - Galeria otimizada
echo    • python run_gallery.py - Galeria compatível
echo    • python duckdb_migration.py - Migração de dados
echo    • python demo_duckdb_vs_sqlite.py - Benchmark
echo.
goto fim

:sair
echo.
echo 👋 Até logo!
goto fim

:opcao_invalida
echo.
echo ❌ Opção inválida: %opcao%
echo 💡 Execute novamente e escolha uma opção entre 1-9

:fim
pause
