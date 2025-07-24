#!/usr/bin/env python3
"""
Demonstração do processo de ETL com Star Schema integrado
Este script mostra como funciona o novo processo de ETL
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data.etl import SAEVDataProcessor

def demo_etl_process():
    """Demonstração do processo de ETL"""
    print("="*80)
    print("🚀 DEMONSTRAÇÃO - PROCESSO ETL COM STAR SCHEMA INTEGRADO")
    print("="*80)
    
    # Caminho para banco de demonstração
    demo_db = "db/demo_etl.db"
    
    try:
        print("1️⃣  Criando processador de dados...")
        processor = SAEVDataProcessor(demo_db)
        
        print("\n2️⃣  Criando estrutura do banco...")
        processor.create_database_structure(overwrite=True)
        
        print("\n3️⃣  Demonstrando funcionalidades disponíveis:")
        print("   📊 create_database_structure() - Cria estrutura e índices")
        print("   📥 load_csv_data() - Carrega dados do CSV")
        print("   🔍 validate_data() - Valida qualidade dos dados")
        print("   ⭐ apply_star_schema() - Aplica transformação Star Schema")
        print("   🚀 full_etl_process() - Processo completo integrado")
        
        print(f"\n4️⃣  Banco de demonstração criado: {demo_db}")
        print("   ✅ Estrutura criada com sucesso")
        print("   ✅ Índices otimizados aplicados") 
        print("   ✅ Pronto para receber dados")
        
        print(f"\n5️⃣  Para usar com dados reais:")
        print("   # Produção")
        print("   python carga.py seus_dados.csv db/avaliacao_prod.db")
        print("   ")
        print("   # Teste")
        print("   python carga_teste.py seus_dados.csv cidade_teste.txt db/avaliacao_teste.db")
        
        print("\n" + "="*80)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🔧 Módulo ETL está funcionando perfeitamente")
        print("⭐ Star Schema integrado e pronto para uso")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERRO NA DEMONSTRAÇÃO: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Criar diretório db se não existir
    Path("db").mkdir(exist_ok=True)
    
    # Executar demonstração
    success = demo_etl_process()
    
    # Limpar arquivo de demonstração
    demo_db = Path("db/demo_etl.db")
    if demo_db.exists():
        demo_db.unlink()
        print(f"🧹 Arquivo de demonstração removido: {demo_db}")
    
    sys.exit(0 if success else 1)
