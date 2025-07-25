#!/usr/bin/env python3
"""
DEMONSTRAÇÃO: ETL COMPLETO COM MIGRAÇÃO DUCKDB AUTOMÁTICA
========================================================

Este script demonstra o novo processo de ETL que:
1. Processa dados CSV → SQLite (processo original mantido)
2. Aplica Star Schema no SQLite
3. Migra automaticamente para DuckDB 
4. Valida a consistência dos dados
5. Disponibiliza ambos os bancos para uso

BENEFÍCIOS:
- Compatibilidade total com processo existente
- Performance superior com DuckDB
- Validação automática de integridade
- Flexibilidade para usar SQLite ou DuckDB conforme necessário
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from data.etl import SAEVDataProcessor
from config import config

def demo_etl_completo():
    """Demonstra o processo ETL completo com DuckDB"""
    
    print("🚀 DEMO: ETL COMPLETO COM DUCKDB")
    print("="*50)
    
    # Configurar processador para ambiente de teste
    db_path = config.get_database_path('teste')
    processor = SAEVDataProcessor(db_path)
    
    print(f"📊 Banco SQLite: {db_path}")
    print(f"🦆 Banco DuckDB: {db_path.replace('.db', '_duckdb.db')}")
    print()
    
    try:
        # Executar ETL completo
        results = processor.full_etl_process(
            csv_folder='data/raw',          # Processar toda a pasta data/raw
            test_mode=True,                 # Modo de teste (anonimização)
            allowed_cities=['CAMPOS DOS GOYTACAZES', 'NITERÓI'],  # Filtrar cidades
            apply_star_schema=True,         # Aplicar modelo estrela
            overwrite_db=True,             # Recriar banco
            include_duckdb=True,           # NOVA FUNCIONALIDADE: Migrar para DuckDB
            force_duckdb=True              # Forçar recriação do DuckDB
        )
        
        print("\n🎉 ETL COMPLETO FINALIZADO!")
        print("="*50)
        
        # Mostrar resultados
        print("📈 RESULTADOS:")
        print(f"   • Total de registros: {results['total_records']:,}")
        print(f"   • Alunos únicos: {results['unique_students']:,}")
        print(f"   • Escolas: {results['schools_count']:,}")
        print(f"   • Municípios: {results['cities_count']:,}")
        
        # Status DuckDB
        if results.get('duckdb_migrated', False):
            if results.get('duckdb_validated', False):
                print(f"   🦆 DuckDB: ✅ Migrado e validado")
            else:
                print(f"   🦆 DuckDB: ⚠️  Migrado mas validação falhou")
        else:
            print(f"   🦆 DuckDB: ❌ Falha na migração")
        
        print("\n🔧 PRÓXIMOS PASSOS:")
        print("   1. Use './iniciar.sh' para dashboard SQLite")
        print("   2. Use './galeria.sh' para interface unificada")
        print("   3. Escolha DuckDB para máxima performance")
        
        # Mostrar tamanhos dos arquivos
        sqlite_path = Path(db_path)
        duckdb_path = Path(db_path.replace('.db', '_duckdb.db'))
        
        if sqlite_path.exists() and duckdb_path.exists():
            sqlite_size = sqlite_path.stat().st_size / (1024**2)
            duckdb_size = duckdb_path.stat().st_size / (1024**2)
            
            print(f"\n📁 TAMANHOS DOS ARQUIVOS:")
            print(f"   • SQLite: {sqlite_size:.1f}MB")
            print(f"   • DuckDB: {duckdb_size:.1f}MB")
            
            if duckdb_size < sqlite_size:
                reduction = ((sqlite_size - duckdb_size) / sqlite_size) * 100
                print(f"   🗜️  Compressão DuckDB: {reduction:.1f}% menor")
        
    except Exception as e:
        print(f"💥 ERRO NO ETL: {e}")
        sys.exit(1)

def demo_opcoes_flexiveis():
    """Demonstra diferentes opções do ETL"""
    
    print("\n" + "="*50)
    print("🎛️  OPÇÕES FLEXÍVEIS DO ETL")
    print("="*50)
    
    print("1️⃣  ETL SOMENTE SQLITE (processo original):")
    print("   processor.full_etl_process(")
    print("       csv_folder='data/raw',")
    print("       include_duckdb=False")
    print("   )")
    
    print("\n2️⃣  ETL COM DUCKDB (novo - recomendado):")
    print("   processor.full_etl_process(")
    print("       csv_folder='data/raw',")
    print("       include_duckdb=True")
    print("   )")
    
    print("\n3️⃣  ETL FORÇANDO RECRIAÇÃO:")
    print("   processor.full_etl_process(")
    print("       csv_folder='data/raw',")
    print("       overwrite_db=True,")
    print("       force_duckdb=True")
    print("   )")
    
    print("\n4️⃣  SOMENTE MIGRAÇÃO DUCKDB:")
    print("   processor.migrate_to_duckdb(force=True)")
    print("   processor.validate_duckdb_migration()")

if __name__ == "__main__":
    demo_etl_completo()
    demo_opcoes_flexiveis()
