#!/usr/bin/env python3
"""
Teste ETL produção com arquivo pequeno
"""

import os
import sys
from pathlib import Path

# Adicionar diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data.etl import SAEVDataProcessor

def main():
    print("🧪 TESTE ETL PRODUÇÃO (AMOSTRA)")
    print("="*50)
    
    # Configuração para teste
    db_path = "db/teste_prod_pequeno.db"
    csv_file = "data/raw/teste_prod_pequeno.csv"
    
    print(f"📊 Banco: {db_path}")
    print(f"📁 CSV: {csv_file}")
    
    if not Path(csv_file).exists():
        print(f"❌ Arquivo não encontrado: {csv_file}")
        return False
    
    try:
        # Criar processador
        processor = SAEVDataProcessor(db_path)
        
        # ETL completo com DuckDB
        print("\n🚀 Executando ETL...")
        results = processor.full_etl_process(
            csv_path=csv_file,
            test_mode=False,  # Modo produção
            apply_star_schema=True,
            overwrite_db=True,
            include_duckdb=True,  # Incluir DuckDB
            force_duckdb=True     # Forçar recriação
        )
        
        print("\n✅ TESTE CONCLUÍDO!")
        print("="*30)
        print("📊 Resultados:")
        for key, value in results.items():
            print(f"   • {key}: {value:,}")
        
        # Verificar arquivos gerados
        sqlite_path = Path(db_path)
        duckdb_path = Path(db_path.replace('.db', '.duckdb'))
        
        print(f"\n📁 Arquivos gerados:")
        if sqlite_path.exists():
            size = sqlite_path.stat().st_size / 1024
            print(f"   📊 SQLite: {size:.1f}KB")
        
        if duckdb_path.exists():
            size = duckdb_path.stat().st_size / 1024
            print(f"   🦆 DuckDB: {size:.1f}KB")
            print("   ✅ Migração funcionou!")
        else:
            print("   ❌ DuckDB não foi criado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
