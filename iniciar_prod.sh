#!/bin/bash

# Script para iniciar o Dashboard SAEV no ambiente de PRODUÇÃO
# Uso: ./iniciar_prod.sh [porta]

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${RED}🔴 SAEV Dashboard - AMBIENTE DE PRODUÇÃO${NC}"
echo -e "${RED}=================================================${NC}"
echo -e "${YELLOW}⚠️  ATENÇÃO: Dados reais e sensíveis!${NC}"
echo -e "${YELLOW}🔒 Use com responsabilidade e cuidado.${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "run_dashboard.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script no diretório raiz do projeto SAEV${NC}"
    echo -e "   Diretório atual: $(pwd)"
    echo -e "   Procurando por: run_dashboard.py"
    exit 1
fi

# Verificar se o banco de produção existe
if [ ! -f "db/avaliacao_prod.db" ]; then
    echo -e "${RED}❌ Erro: Banco de produção não encontrado!${NC}"
    echo -e "   Esperado em: db/avaliacao_prod.db"
    echo ""
    echo -e "${BLUE}💡 Sugestões:${NC}"
    echo -e "   1. Execute o script de carga: python carga.py dados.csv db/avaliacao_prod.db"
    echo -e "   2. Ou configure o ambiente: python manage_env.py setup producao"
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

# Definir porta (padrão ou argumento)
PORT=${1:-8501}

# Validar porta
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
    echo -e "${RED}❌ Erro: Porta inválida: $PORT${NC}"
    echo -e "   Use uma porta entre 1024 e 65535"
    exit 1
fi

# Mostrar informações do ambiente
echo -e "${BLUE}📊 Verificando ambiente de produção...${NC}"
$PYTHON_CMD manage_env.py validate producao

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ambiente de produção inválido!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Ambiente de produção validado com sucesso!${NC}"
echo ""

# Confirmar execução em produção
echo -e "${YELLOW}⚠️  CONFIRMAÇÃO NECESSÁRIA${NC}"
echo -e "Você está prestes a iniciar o dashboard com ${RED}DADOS REAIS DE PRODUÇÃO${NC}."
echo ""
read -p "Deseja continuar? (digite 'SIM' para confirmar): " confirmacao

if [ "$confirmacao" != "SIM" ]; then
    echo -e "${YELLOW}🛑 Operação cancelada pelo usuário.${NC}"
    exit 0
fi

# Definir variáveis de ambiente
export SAEV_ENVIRONMENT=producao

echo ""
echo -e "${GREEN}🚀 Iniciando Dashboard SAEV - PRODUÇÃO${NC}"
echo -e "${GREEN}=================================${NC}"
echo -e "🔗 URL: ${BLUE}http://localhost:$PORT${NC}"
echo -e "🗃️  Ambiente: ${RED}PRODUÇÃO${NC}"
echo -e "📁 Banco: db/avaliacao_prod.db"
echo -e "🔒 Dados: ${RED}REAIS E SENSÍVEIS${NC}"
echo ""
echo -e "${YELLOW}💡 Para parar o servidor, pressione Ctrl+C${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""

# Executar o dashboard
$PYTHON_CMD run_dashboard.py --env producao --port $PORT

# Mensagem de encerramento
echo ""
echo -e "${GREEN}👋 Dashboard SAEV encerrado.${NC}"
