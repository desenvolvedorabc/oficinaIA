#!/bin/bash

# Script de ajuda para inicializar o SAEV Dashboard
# Uso: ./iniciar.sh

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Banner principal
echo -e "${PURPLE}"
echo "  ███████╗ █████╗ ███████╗██╗   ██╗"
echo "  ██╔════╝██╔══██╗██╔════╝██║   ██║"
echo "  ███████╗███████║█████╗  ██║   ██║"
echo "  ╚════██║██╔══██║██╔══╝  ╚██╗ ██╔╝"
echo "  ███████║██║  ██║███████╗ ╚████╔╝ "
echo "  ╚══════╝╚═╝  ╚═╝╚══════╝  ╚═══╝  "
echo -e "${NC}"
echo -e "${BLUE}Sistema de Análise de Avaliações Educacionais${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Verificar status dos ambientes
echo -e "${YELLOW}📊 Verificando ambientes disponíveis...${NC}"
echo ""

if [ -f "db/avaliacao_teste.db" ]; then
    TESTE_STATUS="${GREEN}✅ Disponível${NC}"
else
    TESTE_STATUS="${RED}❌ Não encontrado${NC}"
fi

if [ -f "db/avaliacao_prod.db" ]; then
    PROD_STATUS="${GREEN}✅ Disponível${NC}"
else
    PROD_STATUS="${RED}❌ Não encontrado${NC}"
fi

echo -e "🧪 ${CYAN}Ambiente de TESTE${NC}:     $TESTE_STATUS"
echo -e "🔴 ${RED}Ambiente de PRODUÇÃO${NC}: $PROD_STATUS"
echo ""

# Menu de opções
echo -e "${YELLOW}🚀 Escolha uma opção:${NC}"
echo ""
echo -e "${CYAN}1)${NC} Iniciar ambiente de ${CYAN}TESTE${NC} (dados ofuscados - seguro)"
echo -e "${RED}2)${NC} Iniciar ambiente de ${RED}PRODUÇÃO${NC} (dados reais - cuidado!)"
echo -e "${BLUE}3)${NC} Verificar status detalhado dos ambientes"
echo -e "${BLUE}4)${NC} Configurar ambiente de teste"
echo -e "${BLUE}5)${NC} Mostrar ajuda dos scripts"
echo -e "${YELLOW}6)${NC} Sair"
echo ""

# Ler opção do usuário
read -p "Digite sua escolha (1-6): " opcao

case $opcao in
    1)
        echo ""
        echo -e "${CYAN}🧪 Iniciando ambiente de TESTE...${NC}"
        echo ""
        if [ -f "iniciar_teste.sh" ]; then
            ./iniciar_teste.sh
        else
            echo -e "${RED}❌ Script iniciar_teste.sh não encontrado!${NC}"
        fi
        ;;
    2)
        echo ""
        echo -e "${RED}🔴 Iniciando ambiente de PRODUÇÃO...${NC}"
        echo ""
        if [ -f "iniciar_prod.sh" ]; then
            ./iniciar_prod.sh
        else
            echo -e "${RED}❌ Script iniciar_prod.sh não encontrado!${NC}"
        fi
        ;;
    3)
        echo ""
        echo -e "${BLUE}📊 Status detalhado dos ambientes:${NC}"
        echo ""
        if command -v python3 &> /dev/null || command -v python &> /dev/null; then
            PYTHON_CMD="python3"
            if ! command -v python3 &> /dev/null; then
                PYTHON_CMD="python"
            fi
            $PYTHON_CMD manage_env.py status
        else
            echo -e "${RED}❌ Python não encontrado!${NC}"
        fi
        ;;
    4)
        echo ""
        echo -e "${BLUE}⚙️  Configurando ambiente de teste...${NC}"
        echo ""
        if command -v python3 &> /dev/null || command -v python &> /dev/null; then
            PYTHON_CMD="python3"
            if ! command -v python3 &> /dev/null; then
                PYTHON_CMD="python"
            fi
            mkdir -p db
            $PYTHON_CMD manage_env.py setup teste
            echo ""
            echo -e "${GREEN}✅ Ambiente de teste configurado!${NC}"
            echo -e "${YELLOW}💡 Para adicionar dados, execute:${NC}"
            echo -e "   python carga_teste.py dados.csv cidade_teste.txt db/avaliacao_teste.db"
        else
            echo -e "${RED}❌ Python não encontrado!${NC}"
        fi
        ;;
    5)
        echo ""
        echo -e "${BLUE}📖 Ajuda dos Scripts:${NC}"
        echo ""
        echo -e "${CYAN}• ./iniciar_teste.sh [porta]${NC}"
        echo -e "  Inicia o dashboard no ambiente de teste"
        echo -e "  Exemplo: ./iniciar_teste.sh 8502"
        echo ""
        echo -e "${RED}• ./iniciar_prod.sh [porta]${NC}"
        echo -e "  Inicia o dashboard no ambiente de produção"
        echo -e "  Exemplo: ./iniciar_prod.sh 8503"
        echo ""
        echo -e "${BLUE}• python run_dashboard.py --list${NC}"
        echo -e "  Lista todos os ambientes disponíveis"
        echo ""
        echo -e "${BLUE}• python manage_env.py status${NC}"
        echo -e "  Mostra status detalhado dos ambientes"
        echo ""
        ;;
    6)
        echo ""
        echo -e "${GREEN}👋 Até logo!${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}❌ Opção inválida: $opcao${NC}"
        echo -e "${YELLOW}💡 Execute novamente e escolha uma opção entre 1-6${NC}"
        exit 1
        ;;
esac
