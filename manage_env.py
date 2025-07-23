#!/usr/bin/env python3
"""
Utilitário para gerenciar ambientes do SAEV
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from src.config import config

def show_status():
    """Mostra o status de todos os ambientes"""
    print("📊 Status dos Ambientes SAEV")
    print("=" * 60)
    
    environments = config.list_available_environments()
    
    for env_name, info in environments.items():
        print(f"\n🗃️  {env_name.upper()}")
        print(f"   Status: {'✅ Disponível' if info.get('database_exists') else '❌ Indisponível'}")
        print(f"   Caminho: {info.get('database_path', 'N/A')}")
        
        if info.get('database_exists'):
            if 'file_size_mb' in info:
                print(f"   Tamanho: {info['file_size_mb']} MB")
            if 'last_modified' in info:
                last_mod = datetime.fromtimestamp(info['last_modified'])
                print(f"   Modificado: {last_mod.strftime('%d/%m/%Y %H:%M:%S')}")
        
        print(f"   Descrição: {info.get('description', 'N/A')}")
        print(f"   Repositório: {'✅ Permitido' if info.get('can_be_in_repo') else '❌ Não permitido'}")

def validate_environment(env_name):
    """Valida um ambiente específico"""
    print(f"🔍 Validando ambiente: {env_name}")
    print("=" * 40)
    
    try:
        is_valid, message = config.validate_environment(env_name)
        
        if is_valid:
            print(f"✅ {message}")
            
            # Mostrar detalhes
            info = config.get_environment_info(env_name)
            print(f"\n📁 Caminho: {info['database_path']}")
            print(f"📝 Descrição: {info['description']}")
            
            if info.get('file_size_mb'):
                print(f"📦 Tamanho: {info['file_size_mb']} MB")
        else:
            print(f"❌ {message}")
            
    except Exception as e:
        print(f"❌ Erro durante validação: {e}")

def detect_current():
    """Detecta e mostra o ambiente atual"""
    print("🔍 Detectando ambiente atual...")
    print("=" * 40)
    
    try:
        current_env = config.detect_environment()
        print(f"🎯 Ambiente detectado: {current_env.upper()}")
        
        info = config.get_environment_info(current_env)
        print(f"📁 Caminho: {info['database_path']}")
        print(f"📊 Existe: {'✅ Sim' if info['database_exists'] else '❌ Não'}")
        
        if not info['database_exists']:
            print("\n💡 Sugestões:")
            print("   - Execute o script de carga apropriado")
            print("   - Verifique se o arquivo está no local correto")
            
    except Exception as e:
        print(f"❌ Erro durante detecção: {e}")

def setup_environment(env_name):
    """Configura um ambiente (cria estrutura se necessário)"""
    print(f"⚙️  Configurando ambiente: {env_name}")
    print("=" * 40)
    
    try:
        from src.data.etl import SAEVDataProcessor
        
        db_path = config.get_database_path(env_name)
        
        if Path(db_path).exists():
            print(f"ℹ️  Banco de dados já existe: {db_path}")
        else:
            print(f"🔨 Criando estrutura do banco: {db_path}")
            
            # Criar diretório se necessário
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Criar estrutura do banco
            processor = SAEVDataProcessor(db_path)
            processor.create_database_structure()
            
            print("✅ Estrutura criada com sucesso!")
        
        # Validar
        is_valid, message = config.validate_environment(env_name)
        if is_valid:
            print(f"✅ Ambiente {env_name} está pronto para uso!")
        else:
            print(f"⚠️  Aviso: {message}")
            
    except Exception as e:
        print(f"❌ Erro durante configuração: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Gerenciador de ambientes SAEV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python manage_env.py status              # Mostra status de todos os ambientes
    python manage_env.py detect              # Detecta ambiente atual
    python manage_env.py validate teste      # Valida ambiente de teste
    python manage_env.py setup producao      # Configura ambiente de produção
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando status
    subparsers.add_parser('status', help='Mostra status de todos os ambientes')
    
    # Comando detect
    subparsers.add_parser('detect', help='Detecta ambiente atual')
    
    # Comando validate
    validate_parser = subparsers.add_parser('validate', help='Valida um ambiente específico')
    validate_parser.add_argument('environment', choices=['teste', 'producao'], help='Ambiente a validar')
    
    # Comando setup
    setup_parser = subparsers.add_parser('setup', help='Configura um ambiente')
    setup_parser.add_argument('environment', choices=['teste', 'producao'], help='Ambiente a configurar')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'status':
        show_status()
    elif args.command == 'detect':
        detect_current()
    elif args.command == 'validate':
        validate_environment(args.environment)
    elif args.command == 'setup':
        setup_environment(args.environment)

if __name__ == "__main__":
    main()
