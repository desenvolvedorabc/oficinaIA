#!/bin/bash

# Script de ajuda para inicializar a Galeria de Painéis SAEV
# Uso: ./galeria.sh

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
MAGENTA='\033[0;95m'
NC='\033[0m' # No Color

# Função para capturar Ctrl+C e encerrar processos em background
cleanup() {
    if [ ! -z "$GALLERY_PID" ]; then
        echo ""
        echo -e "${YELLOW}🛑 Encerrando galeria...${NC}"
        kill $GALLERY_PID 2>/dev/null || true
        wait $GALLERY_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}👋 Galeria encerrada.${NC}"
    exit 0
}

# Configurar handler para Ctrl+C
trap cleanup SIGINT SIGTERM

# Banner principal
echo -e "${PURPLE}"
echo "  ████████╗ █████╗ ██╗     ███████╗██████╗ ██╗ █████╗ "
echo "  ╚══██╔══╝██╔══██╗██║     ██╔════╝██╔══██╗██║██╔══██╗"
echo "     ██║   ███████║██║     █████╗  ██████╔╝██║███████║"
echo "     ██║   ██╔══██║██║     ██╔══╝  ██╔══██╗██║██╔══██║"
echo "     ██║   ██║  ██║███████╗███████╗██║  ██║██║██║  ██║"
echo "     ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${MAGENTA}🖼️  Galeria de Painéis de Análise Educacional${NC}"
echo -e "${MAGENTA}=============================================${NC}"
echo ""

# Verificar status dos ambientes
echo -e "${YELLOW}📊 Verificando ambientes disponíveis...${NC}"
echo ""

# Verificar bancos SQLite
if [ -f "db/avaliacao_teste.db" ]; then
    TESTE_SQLITE_STATUS="${GREEN}✅ SQLite${NC}"
else
    TESTE_SQLITE_STATUS="${RED}❌ SQLite${NC}"
fi

if [ -f "db/avaliacao_prod.db" ]; then
    PROD_SQLITE_STATUS="${GREEN}✅ SQLite${NC}"
else
    PROD_SQLITE_STATUS="${RED}❌ SQLite${NC}"
fi

# Verificar bancos DuckDB
if [ -f "db/avaliacao_teste_duckdb.db" ]; then
    TESTE_DUCKDB_STATUS="${CYAN}✅ DuckDB${NC}"
else
    TESTE_DUCKDB_STATUS="${RED}❌ DuckDB${NC}"
fi

if [ -f "db/avaliacao_prod_duckdb.db" ]; then
    PROD_DUCKDB_STATUS="${CYAN}✅ DuckDB${NC}"
else
    PROD_DUCKDB_STATUS="${RED}❌ DuckDB${NC}"
fi

echo -e "🧪 ${CYAN}Ambiente de TESTE${NC}:     $TESTE_SQLITE_STATUS | $TESTE_DUCKDB_STATUS"
echo -e "🔴 ${RED}Ambiente de PRODUÇÃO${NC}: $PROD_SQLITE_STATUS | $PROD_DUCKDB_STATUS"
echo ""

# Verificar se existe run_gallery_duckdb.py
if [ -f "run_gallery_duckdb.py" ]; then
    GALLERY_STATUS="${GREEN}✅ Disponível${NC}"
else
    GALLERY_STATUS="${RED}❌ Não encontrado${NC}"
fi

echo -e "🖼️  ${MAGENTA}Galeria de Painéis${NC}:   $GALLERY_STATUS"
echo ""

# Menu de opções
echo -e "${YELLOW}🚀 Escolha uma opção:${NC}"
echo ""
echo -e "${CYAN}1)${NC} Galeria ${CYAN}TESTE${NC} com ${CYAN}DuckDB${NC} (recomendado - máxima performance)"
echo -e "${CYAN}2)${NC} Galeria ${CYAN}TESTE${NC} com ${BLUE}SQLite${NC} (compatibilidade)"
echo -e "${RED}3)${NC} Galeria ${RED}PRODUÇÃO${NC} com ${CYAN}DuckDB${NC} (dados reais - máxima performance)"
echo -e "${RED}4)${NC} Galeria ${RED}PRODUÇÃO${NC} com ${BLUE}SQLite${NC} (dados reais - compatibilidade)"
echo -e "${MAGENTA}5)${NC} Benchmark de Performance (comparar SQLite vs DuckDB)"
echo -e "${BLUE}6)${NC} Verificar status detalhado dos ambientes"
echo -e "${BLUE}7)${NC} Migrar SQLite para DuckDB"
echo -e "${BLUE}8)${NC} Mostrar ajuda da galeria"
echo -e "${YELLOW}9)${NC} Sair"
echo ""

# Ler opção do usuário
read -p "Digite sua escolha (1-9): " opcao

case $opcao in
    1)
        echo ""
        echo -e "${CYAN}🖼️  Iniciando Galeria TESTE com DuckDB...${NC}"
        echo -e "${GREEN}✨ Performance otimizada para análises complexas${NC}"
        echo ""
        if [ -f "run_gallery_duckdb.py" ]; then
            if [ -f "db/avaliacao_teste_duckdb.db" ]; then
                echo -e "${BLUE}🔗 URL: http://localhost:8504${NC}"
                echo -e "${YELLOW}💡 Abrindo navegador automaticamente...${NC}"
                echo ""
                
                # Iniciar galeria em background
                python3 run_gallery_duckdb.py --env teste --port 8504 &
                GALLERY_PID=$!
                
                # Aguardar servidor inicializar
                sleep 3
                
                # Abrir navegador automaticamente (macOS)
                if command -v open &> /dev/null; then
                    open "http://localhost:8504" 2>/dev/null || true
                fi
                
                # Aguardar processo da galeria
                echo -e "${GREEN}✅ Galeria executando! Pressione Ctrl+C para parar.${NC}"
                wait $GALLERY_PID
            else
                echo -e "${YELLOW}⚠️  Banco DuckDB de teste não encontrado!${NC}"
                echo -e "${BLUE}💡 Execute: python duckdb_migration.py migrate teste${NC}"
            fi
        else
            echo -e "${RED}❌ Script run_gallery_duckdb.py não encontrado!${NC}"
        fi
        ;;
    2)
        echo ""
        echo -e "${CYAN}🖼️  Iniciando Galeria TESTE com SQLite...${NC}"
        echo -e "${YELLOW}⚠️  Performance limitada para análises complexas${NC}"
        echo ""
        if [ -f "run_gallery.py" ]; then
            if [ -f "db/avaliacao_teste.db" ]; then
                echo -e "${BLUE}🔗 URL: http://localhost:8504${NC}"
                echo -e "${YELLOW}💡 Abrindo navegador automaticamente...${NC}"
                echo ""
                
                # Iniciar galeria em background
                python3 run_gallery.py --env teste --port 8504 &
                GALLERY_PID=$!
                
                # Aguardar servidor inicializar
                sleep 3
                
                # Abrir navegador automaticamente (macOS)
                if command -v open &> /dev/null; then
                    open "http://localhost:8504" 2>/dev/null || true
                fi
                
                # Aguardar processo da galeria
                echo -e "${GREEN}✅ Galeria executando! Pressione Ctrl+C para parar.${NC}"
                wait $GALLERY_PID
            else
                echo -e "${YELLOW}⚠️  Banco SQLite de teste não encontrado!${NC}"
                echo -e "${BLUE}💡 Execute: python carga_teste.py${NC}"
            fi
        else
            echo -e "${RED}❌ Script run_gallery.py não encontrado!${NC}"
        fi
        ;;
    3)
        echo ""
        echo -e "${RED}🖼️  Iniciando Galeria PRODUÇÃO com DuckDB...${NC}"
        echo -e "${GREEN}✨ Performance otimizada para dados reais${NC}"
        echo -e "${YELLOW}⚠️  ATENÇÃO: Dados reais sensíveis!${NC}"
        echo ""
        read -p "Confirma inicialização em PRODUÇÃO? (s/N): " confirm
        if [[ $confirm =~ ^[Ss]$ ]]; then
            if [ -f "run_gallery_duckdb.py" ]; then
                if [ -f "db/avaliacao_prod_duckdb.db" ]; then
                    echo -e "${BLUE}🔗 URL: http://localhost:8505${NC}"
                    echo -e "${YELLOW}💡 Abrindo navegador automaticamente...${NC}"
                    echo ""
                    
                    # Iniciar galeria em background
                    python3 run_gallery_duckdb.py --env producao --port 8505 &
                    GALLERY_PID=$!
                    
                    # Aguardar servidor inicializar
                    sleep 3
                    
                    # Abrir navegador automaticamente (macOS)
                    if command -v open &> /dev/null; then
                        open "http://localhost:8505" 2>/dev/null || true
                    fi
                    
                    # Aguardar processo da galeria
                    echo -e "${GREEN}✅ Galeria PRODUÇÃO executando! Pressione Ctrl+C para parar.${NC}"
                    wait $GALLERY_PID
                else
                    echo -e "${YELLOW}⚠️  Banco DuckDB de produção não encontrado!${NC}"
                    echo -e "${BLUE}💡 Execute: python duckdb_migration.py migrate prod${NC}"
                fi
            else
                echo -e "${RED}❌ Script run_gallery_duckdb.py não encontrado!${NC}"
            fi
        else
            echo -e "${GREEN}✅ Operação cancelada${NC}"
        fi
        ;;
    4)
        echo ""
        echo -e "${RED}🖼️  Iniciando Galeria PRODUÇÃO com SQLite...${NC}"
        echo -e "${YELLOW}⚠️  Performance limitada + dados reais sensíveis!${NC}"
        echo ""
        read -p "Confirma inicialização em PRODUÇÃO com SQLite? (s/N): " confirm
        if [[ $confirm =~ ^[Ss]$ ]]; then
            if [ -f "run_gallery.py" ]; then
                if [ -f "db/avaliacao_prod.db" ]; then
                    echo -e "${BLUE}🔗 URL: http://localhost:8505${NC}"
                    echo -e "${YELLOW}💡 Abrindo navegador automaticamente...${NC}"
                    echo ""
                    
                    # Iniciar galeria em background
                    python3 run_gallery.py --env producao --port 8505 &
                    GALLERY_PID=$!
                    
                    # Aguardar servidor inicializar
                    sleep 3
                    
                    # Abrir navegador automaticamente (macOS)
                    if command -v open &> /dev/null; then
                        open "http://localhost:8505" 2>/dev/null || true
                    fi
                    
                    # Aguardar processo da galeria
                    echo -e "${GREEN}✅ Galeria PRODUÇÃO executando! Pressione Ctrl+C para parar.${NC}"
                    wait $GALLERY_PID
                else
                    echo -e "${YELLOW}⚠️  Banco SQLite de produção não encontrado!${NC}"
                    echo -e "${BLUE}💡 Execute: python carga.py${NC}"
                fi
            else
                echo -e "${RED}❌ Script run_gallery.py não encontrado!${NC}"
            fi
        else
            echo -e "${GREEN}✅ Operação cancelada${NC}"
        fi
        ;;
    5)
        echo ""
        echo -e "${MAGENTA}🏁 Executando Benchmark de Performance...${NC}"
        echo ""
        if [ -f "demo_duckdb_vs_sqlite.py" ]; then
            python3 demo_duckdb_vs_sqlite.py
        else
            echo -e "${RED}❌ Script demo_duckdb_vs_sqlite.py não encontrado!${NC}"
        fi
        ;;
    6)
        echo ""
        echo -e "${BLUE}📊 Status detalhado dos ambientes:${NC}"
        echo ""
        if command -v python3 &> /dev/null || command -v python &> /dev/null; then
            PYTHON_CMD="python3"
            if ! command -v python3 &> /dev/null; then
                PYTHON_CMD="python"
            fi
            $PYTHON_CMD manage_env.py status
            echo ""
            echo -e "${CYAN}🦆 Status DuckDB:${NC}"
            if [ -f "db/avaliacao_teste_duckdb.db" ]; then
                echo -e "   🧪 Teste: ${GREEN}✅ Disponível${NC} ($(du -h db/avaliacao_teste_duckdb.db | cut -f1))"
            else
                echo -e "   🧪 Teste: ${RED}❌ Não encontrado${NC}"
            fi
            if [ -f "db/avaliacao_prod_duckdb.db" ]; then
                echo -e "   🔴 Prod:  ${GREEN}✅ Disponível${NC} ($(du -h db/avaliacao_prod_duckdb.db | cut -f1))"
            else
                echo -e "   🔴 Prod:  ${RED}❌ Não encontrado${NC}"
            fi
        else
            echo -e "${RED}❌ Python não encontrado!${NC}"
        fi
        ;;
    7)
        echo ""
        echo -e "${BLUE}🔄 Migrando SQLite para DuckDB...${NC}"
        echo ""
        echo -e "${YELLOW}Escolha o ambiente para migrar:${NC}"
        echo -e "${CYAN}1)${NC} Migrar ambiente de ${CYAN}TESTE${NC}"
        echo -e "${RED}2)${NC} Migrar ambiente de ${RED}PRODUÇÃO${NC}"
        echo -e "${YELLOW}3)${NC} Voltar ao menu principal"
        echo ""
        read -p "Digite sua escolha (1-3): " migrate_option
        
        case $migrate_option in
            1)
                echo ""
                echo -e "${CYAN}🔄 Migrando ambiente de TESTE...${NC}"
                if [ -f "duckdb_migration.py" ]; then
                    python3 duckdb_migration.py migrate teste
                else
                    echo -e "${RED}❌ Script duckdb_migration.py não encontrado!${NC}"
                fi
                ;;
            2)
                echo ""
                echo -e "${RED}🔄 Migrando ambiente de PRODUÇÃO...${NC}"
                echo -e "${YELLOW}⚠️  ATENÇÃO: Operação em dados de produção!${NC}"
                read -p "Confirma migração de PRODUÇÃO? (s/N): " confirm_migrate
                if [[ $confirm_migrate =~ ^[Ss]$ ]]; then
                    if [ -f "duckdb_migration.py" ]; then
                        python3 duckdb_migration.py migrate prod
                    else
                        echo -e "${RED}❌ Script duckdb_migration.py não encontrado!${NC}"
                    fi
                else
                    echo -e "${GREEN}✅ Migração cancelada${NC}"
                fi
                ;;
            3)
                echo -e "${GREEN}↩️  Voltando ao menu principal...${NC}"
                ;;
            *)
                echo -e "${RED}❌ Opção inválida: $migrate_option${NC}"
                ;;
        esac
        ;;
    8)
        echo ""
        echo -e "${BLUE}📖 Ajuda da Galeria de Painéis:${NC}"
        echo ""
        echo -e "${MAGENTA}🖼️  GALERIA DE PAINÉIS${NC}"
        echo -e "A galeria oferece múltiplos painéis especializados:"
        echo ""
        echo -e "${CYAN}📊 Painéis Disponíveis:${NC}"
        echo -e "   • Dashboard Principal (visão geral)"
        echo -e "   • Análise Detalhada (filtros avançados)"
        echo -e "   • Comparativo de Desempenho"
        echo -e "   • Análise por Competências"
        echo -e "   • Relatórios Executivos"
        echo ""
        echo -e "${CYAN}🚀 Performance:${NC}"
        echo -e "   • ${CYAN}DuckDB${NC}: 10-190x mais rápido que SQLite"
        echo -e "   • ${BLUE}SQLite${NC}: Compatibilidade total"
        echo ""
        echo -e "${CYAN}📱 Acesso:${NC}"
        echo -e "   • Teste:    http://localhost:8504"
        echo -e "   • Produção: http://localhost:8505"
        echo ""
        echo -e "${CYAN}🔧 Scripts Relacionados:${NC}"
        echo -e "   • ${GREEN}python3 run_gallery_duckdb.py${NC} - Galeria otimizada"
        echo -e "   • ${BLUE}python3 run_gallery.py${NC} - Galeria compatível"
        echo -e "   • ${YELLOW}python3 duckdb_migration.py${NC} - Migração de dados"
        echo -e "   • ${MAGENTA}python3 demo_duckdb_vs_sqlite.py${NC} - Benchmark"
        echo ""
        ;;
    9)
        echo ""
        echo -e "${GREEN}👋 Até logo!${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}❌ Opção inválida: $opcao${NC}"
        echo -e "${YELLOW}💡 Execute novamente e escolha uma opção entre 1-9${NC}"
        exit 1
        ;;
esac
