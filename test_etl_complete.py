#!/usr/bin/env python3
"""
Teste completo do ETL com dados reais (sem filtro de cidades)
"""

import os
import sys
from pathlib import Path

# Adicionar diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data.etl import SAEVDataProcessor

def main():
    print("🧪 TESTE ETL COMPLETO - DADOS REAIS")
    print("="*50)
    
    # Configuração
    db_path = "db/avaliacao_teste.db"
    duckdb_path = db_path.replace('.db', '.duckdb')
    
    print(f"📊 Banco SQLite: {os.path.abspath(db_path)}")
    print(f"🦆 Banco DuckDB: {os.path.abspath(duckdb_path)}")
    
    # Listar arquivos CSV
    csv_files = list(Path("data/raw").glob("*.csv"))
    print(f"\n📁 Encontrados {len(csv_files)} arquivos CSV")
    
    # Processar com uma amostra pequena para teste rápido
    processor = SAEVDataProcessor(db_path)
    
    print("\n🚀 ETL com amostra pequena (1º arquivo apenas)...")
    try:
        # Processar apenas o primeiro arquivo para teste rápido
        first_csv = csv_files[0]
        results = processor.full_etl_process(
            csv_path=str(first_csv),  # Apenas um arquivo
            test_mode=False,  # Sem filtro de cidades
            apply_star_schema=True,
            overwrite_db=True,
            include_duckdb=True,  # Incluir migração DuckDB
            force_duckdb=True     # Forçar recriação DuckDB
        )
        
        print("\n✅ ETL CONCLUÍDO!")
        print("="*30)
        print("📊 RESULTADOS:")
        for key, value in results.items():
            print(f"   • {key}: {value:,}")
        
        # Verificar tamanhos dos arquivos
        sqlite_size = Path(db_path).stat().st_size / (1024*1024) if Path(db_path).exists() else 0
        duckdb_size = Path(duckdb_path).stat().st_size / (1024*1024) if Path(duckdb_path).exists() else 0
        
        print(f"\n📁 ARQUIVOS GERADOS:")
        print(f"   📊 SQLite: {sqlite_size:.1f}MB")
        print(f"   🦆 DuckDB: {duckdb_size:.1f}MB")
        
        if Path(duckdb_path).exists() and sqlite_size > 0:
            ratio = duckdb_size / sqlite_size
            print(f"   📈 Razão DuckDB/SQLite: {ratio:.2f}x")
        
        print(f"\n🎯 TESTE CONCLUÍDO COM SUCESSO!")
        
        # Mostrar próximos passos
        print("\n" + "="*50)
        print("📋 PRÓXIMOS PASSOS:")
        print("="*50)
        print("1️⃣  Para processar TODOS os dados:")
        print("   python carga_teste.py")
        print("")
        print("2️⃣  Para usar a galeria com DuckDB:")
        print("   ./galeria.sh")
        print("   → Escolher opção 1 (DuckDB)")
        print("")
        print("3️⃣  Para comparar performance:")
        print("   python demo_duckdb_vs_sqlite.py")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
        
    return True

if __name__ == "__main__":
    main()
