#!/usr/bin/env python3
"""
DIAGNÓSTICO DO STAR SCHEMA - SAEV
================================

Script para diagnosticar problemas de detecção do Star Schema
em bancos SQLite e DuckDB.
"""

import sqlite3
import os
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

try:
    import duckdb
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False
    print("⚠️ DuckDB não disponível")

from src.config import config

def diagnose_database(db_path: str, db_type: str = 'auto'):
    """Diagnostica banco de dados e Star Schema"""
    
    print(f"🔍 DIAGNÓSTICO: {db_path}")
    print("="*60)
    
    # Verificar se arquivo existe
    if not Path(db_path).exists():
        print(f"❌ Arquivo não encontrado: {db_path}")
        return False
    
    # Tamanho do arquivo
    size_mb = Path(db_path).stat().st_size / (1024 * 1024)
    print(f"📦 Tamanho: {size_mb:.2f} MB")
    
    # Detectar tipo do banco
    is_duckdb = 'duckdb' in db_path or db_type == 'duckdb'
    
    try:
        if is_duckdb and DUCKDB_AVAILABLE:
            print("🦆 Conectando via DuckDB...")
            conn = duckdb.connect(db_path)
            
            # Listar todas as tabelas
            tables = conn.execute("SHOW TABLES").fetchall()
            print(f"📋 Tabelas encontradas: {[t[0] for t in tables]}")
            
            # Verificar Star Schema
            required_tables = ['dim_aluno', 'dim_escola', 'dim_descritor', 'fato_resposta_aluno']
            star_schema_ok = True
            
            for table in required_tables:
                try:
                    result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchall()
                    if result:
                        print(f"✅ {table}: OK")
                    else:
                        print(f"❌ {table}: NÃO ENCONTRADA")
                        star_schema_ok = False
                except Exception as e:
                    print(f"❌ {table}: ERRO - {e}")
                    star_schema_ok = False
            
            # Contar registros se tudo OK
            if star_schema_ok:
                count = conn.execute("SELECT COUNT(*) FROM fato_resposta_aluno").fetchall()[0][0]
                print(f"📊 Registros na tabela fato: {count:,}")
                
                # Teste de query simples
                try:
                    sample = conn.execute("SELECT AVA_ANO, COUNT(*) FROM fato_resposta_aluno GROUP BY AVA_ANO LIMIT 3").fetchall()
                    print(f"📈 Anos disponíveis: {sample}")
                except Exception as e:
                    print(f"⚠️ Erro em query teste: {e}")
            
            conn.close()
            
        else:
            print("📊 Conectando via SQLite...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Listar todas as tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tabelas encontradas: {tables}")
            
            # Verificar Star Schema
            required_tables = ['dim_aluno', 'dim_escola', 'dim_descritor', 'fato_resposta_aluno']
            star_schema_ok = True
            
            for table in required_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    print(f"✅ {table}: OK")
                else:
                    print(f"❌ {table}: NÃO ENCONTRADA")
                    star_schema_ok = False
            
            # Contar registros se tudo OK
            if star_schema_ok:
                cursor.execute("SELECT COUNT(*) FROM fato_resposta_aluno")
                count = cursor.fetchone()[0]
                print(f"📊 Registros na tabela fato: {count:,}")
                
                # Teste de query simples
                try:
                    cursor.execute("SELECT AVA_ANO, COUNT(*) FROM fato_resposta_aluno GROUP BY AVA_ANO LIMIT 3")
                    sample = cursor.fetchall()
                    print(f"📈 Anos disponíveis: {sample}")
                except Exception as e:
                    print(f"⚠️ Erro em query teste: {e}")
            
            conn.close()
        
        print(f"\n🎯 Star Schema: {'✅ OK' if star_schema_ok else '❌ PROBLEMAS'}")
        return star_schema_ok
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal"""
    
    print("🔍 DIAGNÓSTICO STAR SCHEMA - SAEV")
    print("="*60)
    
    # Diagnósticar ambos ambientes
    environments = ['teste', 'producao']
    
    for env in environments:
        print(f"\n🌍 AMBIENTE: {env.upper()}")
        print("-" * 40)
        
        try:
            # SQLite
            sqlite_path = config.get_database_path(env)
            if Path(sqlite_path).exists():
                diagnose_database(sqlite_path, 'sqlite')
            else:
                print(f"⚠️ SQLite não encontrado: {sqlite_path}")
            
            # DuckDB
            duckdb_path = sqlite_path.replace('.db', '.duckdb')
            if Path(duckdb_path).exists():
                print("\n" + "-" * 20)
                diagnose_database(duckdb_path, 'duckdb')
            else:
                print(f"⚠️ DuckDB não encontrado: {duckdb_path}")
                
        except Exception as e:
            print(f"❌ Erro no ambiente {env}: {e}")
    
    print("\n" + "="*60)
    print("🎯 RECOMENDAÇÕES:")
    print("- Se Star Schema OK: Dashboard deveria funcionar")
    print("- Se Star Schema com problemas: Execute apply_star_schema.py")
    print("- Se DuckDB com problemas: Re-execute migração")

if __name__ == "__main__":
    main()
