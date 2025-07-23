#!/usr/bin/env python3
"""
Script para executar o Dashboard SAEV
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

def parse_arguments():
    """Parse argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Execute o Dashboard SAEV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python run_dashboard.py                    # Detecta automaticamente o ambiente
    python run_dashboard.py --env teste        # Força usar banco de teste
    python run_dashboard.py --env producao     # Força usar banco de produção
    python run_dashboard.py --list             # Lista ambientes disponíveis
    python run_dashboard.py --port 8502        # Executa na porta 8502
        """
    )
    
    parser.add_argument(
        '--env', '--environment',
        choices=['teste', 'producao'],
        help='Ambiente a ser usado (teste ou producao). Se não especificado, detecta automaticamente.'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Porta para executar o Streamlit (padrão: 8501)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='Lista os ambientes disponíveis e sai'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Mostra informações do ambiente e sai'
    )
    
    return parser.parse_args()

def show_environment_list():
    """Mostra lista de ambientes disponíveis"""
    from src.config import config
    
    print("🗃️  Ambientes Disponíveis:")
    print("=" * 60)
    
    environments = config.list_available_environments()
    
    for env_name, info in environments.items():
        status = "✅ Disponível" if info.get('database_exists', False) else "❌ Indisponível"
        
        print(f"\n📊 {env_name.upper()}")
        print(f"   Status: {status}")
        print(f"   Descrição: {info.get('description', 'N/A')}")
        
        if info.get('database_exists', False):
            print(f"   Caminho: {info.get('database_path', 'N/A')}")
            if 'file_size_mb' in info:
                print(f"   Tamanho: {info['file_size_mb']} MB")
            if 'last_modified' in info:
                last_mod = datetime.fromtimestamp(info['last_modified'])
                print(f"   Modificado: {last_mod.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            print(f"   Caminho esperado: {info.get('database_path', 'N/A')}")
            if 'error' in info:
                print(f"   Erro: {info['error']}")

def show_environment_info(environment=None):
    """Mostra informações detalhadas do ambiente"""
    from src.config import config
    
    try:
        info = config.get_environment_info(environment)
        
        print(f"ℹ️  Informações do Ambiente: {info['environment'].upper()}")
        print("=" * 50)
        print(f"📁 Caminho do banco: {info['database_path']}")
        print(f"📊 Banco existe: {'✅ Sim' if info['database_exists'] else '❌ Não'}")
        print(f"📝 Descrição: {info['description']}")
        print(f"🔒 Pode estar no repo: {'✅ Sim' if info['can_be_in_repo'] else '❌ Não'}")
        print(f"🧪 Dados de exemplo: {'✅ Sim' if info['sample_data'] else '❌ Não'}")
        
        if info['database_exists']:
            print(f"📦 Tamanho: {info.get('file_size_mb', 'N/A')} MB")
            if 'last_modified' in info:
                last_mod = datetime.fromtimestamp(info['last_modified'])
                print(f"📅 Última modificação: {last_mod.strftime('%d/%m/%Y %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erro ao obter informações: {e}")

def main():
    """Função principal para executar o dashboard"""
    args = parse_arguments()
    
    # Verificar se estamos no diretório correto
    current_dir = Path.cwd()
    dashboard_path = current_dir / "src" / "dashboard" / "main.py"
    
    if not dashboard_path.exists():
        print("❌ Erro: Arquivo do dashboard não encontrado!")
        print(f"   Procurando em: {dashboard_path}")
        print("   Certifique-se de estar no diretório raiz do projeto.")
        sys.exit(1)
    
    # Importar configuração
    from src.config import config
    
    # Processar argumentos especiais
    if args.list:
        show_environment_list()
        sys.exit(0)
    
    if args.info:
        show_environment_info(args.env)
        sys.exit(0)
    
    # Determinar ambiente
    try:
        environment = args.env if args.env else config.detect_environment()
        
        # Validar ambiente
        is_valid, message = config.validate_environment(environment)
        if not is_valid:
            print(f"❌ {message}")
            print("\n💡 Use --list para ver ambientes disponíveis")
            sys.exit(1)
        
        # Obter informações do ambiente
        env_info = config.get_environment_info(environment)
        
        print("🚀 Iniciando o Dashboard SAEV...")
        print("=" * 50)
        print(f"🗃️  Ambiente: {environment.upper()}")
        print(f"� Banco de dados: {env_info['database_path']}")
        print(f"📝 Descrição: {env_info['description']}")
        if env_info.get('file_size_mb'):
            print(f"📦 Tamanho: {env_info['file_size_mb']} MB")
        print(f"🔗 URL: http://localhost:{args.port}")
        print("=" * 50)
        
        # Definir variável de ambiente para o Streamlit
        os.environ['SAEV_DATABASE_PATH'] = env_info['database_path']
        os.environ['SAEV_ENVIRONMENT'] = environment
        
    except Exception as e:
        print(f"❌ Erro ao configurar ambiente: {e}")
        print("💡 Use --list para ver ambientes disponíveis")
        sys.exit(1)
    
    # Executar o Streamlit
    try:
        subprocess.run([
            "streamlit", "run", str(dashboard_path),
            "--server.port", str(args.port),
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o Streamlit: {e}")
        print("💡 Certifique-se de que o Streamlit está instalado:")
        print("   pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário.")

if __name__ == "__main__":
    main()
