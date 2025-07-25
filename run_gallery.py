#!/usr/bin/env python3
"""
LAUNCHER DA GALERIA DE PAINÉIS SAEV
==================================

Script para iniciar a galeria de painéis do sistema SAEV com múltiplos
dashboards especializados.

Uso:
    python run_gallery.py [--env teste|producao] [--port 8502]

Argumentos:
    --env: Ambiente (teste ou producao). Padrão: auto-detecção
    --port: Porta para o servidor. Padrão: 8502
    --help: Mostra esta ajuda

Exemplos:
    python run_gallery.py                    # Auto-detecção de ambiente
    python run_gallery.py --env teste        # Força ambiente de teste
    python run_gallery.py --env producao     # Força ambiente de produção
    python run_gallery.py --port 8503        # Muda a porta
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from src.config import config

def show_banner():
    """Exibe banner de inicialização"""
    print("🎨" + "="*50)
    print("🎨 GALERIA DE PAINÉIS SAEV")
    print("🎨 Sistema Avançado de Análise Educacional")
    print("🎨" + "="*50)

def setup_environment(env_name: str = None, port: int = 8502):
    """Configura o ambiente e variáveis"""
    
    # Detectar ambiente se não especificado
    if not env_name or env_name == 'auto':
        try:
            env_name = config.detect_environment()
            print(f"🔍 Ambiente detectado automaticamente: {env_name.upper()}")
        except Exception as e:
            print(f"❌ Erro na detecção automática: {e}")
            print("📝 Usando ambiente padrão: TESTE")
            env_name = 'teste'
    
    # Obter informações do ambiente
    try:
        db_path = config.get_database_path(env_name)
        env_info = config.get_environment_info(env_name)
        
        # Verificar se banco existe
        if not Path(db_path).exists():
            print(f"❌ Banco de dados não encontrado: {db_path}")
            print("💡 Execute primeiro um dos scripts de carga:")
            print("   - python carga_teste.py")
            print("   - python carga.py")
            sys.exit(1)
        
        # Configurar variáveis de ambiente
        os.environ['SAEV_DATABASE_PATH'] = db_path
        os.environ['SAEV_ENVIRONMENT'] = env_name
        
        # Exibir informações
        print(f"🗃️  Ambiente: {env_name.upper()}")
        print(f"📁 Banco de dados: {db_path}")
        print(f"📝 Descrição: {env_info['description']}")
        
        if env_info.get('file_size_mb'):
            print(f"📦 Tamanho: {env_info['file_size_mb']} MB")
        
        print(f"🔗 URL: http://localhost:{port}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar ambiente: {e}")
        return False

def run_gallery(port: int = 8502):
    """Executa a galeria de painéis"""
    
    # Caminho para o arquivo da galeria
    gallery_path = Path(__file__).parent / "src" / "dashboard" / "gallery.py"
    
    if not gallery_path.exists():
        print(f"❌ Arquivo da galeria não encontrado: {gallery_path}")
        sys.exit(1)
    
    # Comando do Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(gallery_path),
        "--server.port", str(port),
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    try:
        # Executar o comando
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar galeria: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Galeria interrompida pelo usuário")
        sys.exit(0)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Launcher da Galeria de Painéis SAEV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_gallery.py                    # Auto-detecção de ambiente
  python run_gallery.py --env teste        # Força ambiente de teste  
  python run_gallery.py --env producao     # Força ambiente de produção
  python run_gallery.py --port 8503        # Muda a porta

Painéis disponíveis:
  🎯 Análise Detalhada por Filtros         # Análise granular multi-filtros
  📊 Dashboard Geral                       # Visão panorâmica (em desenvolvimento)
  🏫 Análise por Escola                    # Análises institucionais (em desenvolvimento)
  🏙️ Análise por Município                 # Comparações regionais (em desenvolvimento)
  📈 Análise Temporal                      # Evolução histórica (em desenvolvimento)
        """
    )
    
    parser.add_argument(
        '--env',
        choices=['teste', 'producao', 'auto'],
        default='auto',
        help='Ambiente a ser usado (teste, producao ou auto para detecção automática)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8502,
        help='Porta para o servidor Streamlit (padrão: 8502)'
    )
    
    args = parser.parse_args()
    
    # Mostrar banner
    show_banner()
    
    # Configurar ambiente
    if not setup_environment(args.env, args.port):
        sys.exit(1)
    
    # Executar galeria
    print("🚀 Iniciando Galeria de Painéis SAEV...")
    run_gallery(args.port)

if __name__ == "__main__":
    main()
