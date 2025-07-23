#!/bin/bash

# Script para iniciar o Dashboard SAEV no ambiente de TESTE
# Uso: ./iniciar_teste.sh [porta]

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}🧪 SAEV Dashboard - AMBIENTE DE TESTE${NC}"
echo -e "${CYAN}======================================${NC}"
echo -e "${GREEN}✅ Ambiente seguro com dados ofuscados (MD5)${NC}"
echo -e "${GREEN}🔓 Ideal para desenvolvimento e demonstrações${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "run_dashboard.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script no diretório raiz do projeto SAEV${NC}"
    echo -e "   Diretório atual: $(pwd)"
    echo -e "   Procurando por: run_dashboard.py"
    exit 1
fi

# Verificar dependências
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Erro: Python não encontrado!${NC}"
    echo -e "   Instale o Python 3.8+ para continuar."
    exit 1
fi

# Definir comando Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Verificar se o Streamlit está instalado
if ! $PYTHON_CMD -c "import streamlit" 2>/dev/null; then
    echo -e "${RED}❌ Erro: Streamlit não está instalado!${NC}"
    echo -e "${BLUE}💡 Instale as dependências:${NC}"
    echo -e "   pip install -r requirements.txt"
    exit 1
fi

# Verificar/criar banco de teste
if [ ! -f "db/avaliacao_teste.db" ]; then
    echo -e "${YELLOW}⚠️  Banco de teste não encontrado!${NC}"
    echo -e "${BLUE}🔨 Criando estrutura do banco de teste...${NC}"
    
    # Criar diretório db se não existir
    mkdir -p db
    
    # Configurar ambiente de teste
    $PYTHON_CMD manage_env.py setup teste
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro ao criar estrutura do banco de teste!${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ Estrutura do banco de teste criada!${NC}"
    echo -e "${YELLOW}💡 Para adicionar dados de exemplo, execute:${NC}"
    echo -e "   python carga_teste.py dados.csv cidade_teste.txt db/avaliacao_teste.db"
    echo ""
fi

# Definir porta (padrão ou argumento)
PORT=${1:-8501}

# Validar porta
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
    echo -e "${RED}❌ Erro: Porta inválida: $PORT${NC}"
    echo -e "   Use uma porta entre 1024 e 65535"
    exit 1
fi

# Mostrar informações do ambiente
echo -e "${BLUE}📊 Verificando ambiente de teste...${NC}"
$PYTHON_CMD manage_env.py validate teste

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ambiente de teste inválido!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Ambiente de teste validado com sucesso!${NC}"
echo ""

# Definir variáveis de ambiente
export SAEV_ENVIRONMENT=teste

echo -e "${GREEN}🚀 Iniciando Dashboard SAEV - TESTE${NC}"
echo -e "${GREEN}==============================${NC}"
echo -e "🔗 URL: ${BLUE}http://localhost:$PORT${NC}"
echo -e "🗃️  Ambiente: ${CYAN}TESTE${NC}"
echo -e "📁 Banco: db/avaliacao_teste.db"
echo -e "🔓 Dados: ${GREEN}OFUSCADOS (MD5)${NC}"
echo ""
echo -e "${YELLOW}💡 Para parar o servidor, pressione Ctrl+C${NC}"
echo -e "${GREEN}==============================${NC}"
echo ""

# Executar o dashboard
$PYTHON_CMD run_dashboard.py --env teste --port $PORT

# Mensagem de encerramento
echo ""
echo -e "${GREEN}👋 Dashboard SAEV encerrado.${NC}"
