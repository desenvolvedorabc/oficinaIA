"""
MIGRAÇÃO PARA DUCKDB - PERFORMANCE SUPERIOR PARA ANÁLISES SAEV
============================================================

DuckDB é um banco de dados OLAP (Online Analytical Processing) otimizado
para consultas analíticas, oferecendo performance 10-100x superior ao SQLite
para operações de agregação e relatórios.

VANTAGENS DO DUCKDB:
- Arquitetura colunar otimizada para análises
- Processamento vetorizado 
- Compressão inteligente
- Zero configuração (arquivo único)
- Compatibilidade SQL completa
- Suporte nativo a Pandas
"""

import duckdb
import pandas as pd
import os
import sqlite3
from pathlib import Path
import time
from typing import Optional

class DuckDBMigrator:
    """Classe para migrar dados SQLite para DuckDB otimizado"""
    
    def __init__(self, sqlite_path: str, duckdb_path: str):
        self.sqlite_path = sqlite_path
        self.duckdb_path = duckdb_path
        
    def migrate_to_duckdb(self) -> bool:
        """Migra dados do SQLite para DuckDB com otimizações"""
        try:
            print("🦆 Iniciando migração SQLite → DuckDB...")
            start_time = time.time()
            
            # Conectar aos bancos
            sqlite_conn = sqlite3.connect(self.sqlite_path)
            duck_conn = duckdb.connect(self.duckdb_path)
            
            # Migrar tabelas dimensão
            self._migrate_dimension_tables(sqlite_conn, duck_conn)
            
            # Migrar tabela fato com particionamento
            self._migrate_fact_table(sqlite_conn, duck_conn)
            
            # Criar índices otimizados
            self._create_optimized_indexes(duck_conn)
            
            # Otimizar banco
            duck_conn.execute("ANALYZE")
            
            sqlite_conn.close()
            duck_conn.close()
            
            elapsed = time.time() - start_time
            print(f"✅ Migração concluída em {elapsed:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            return False
    
    def _migrate_dimension_tables(self, sqlite_conn, duck_conn):
        """Migra tabelas de dimensão"""
        dimensions = ['dim_aluno', 'dim_escola', 'dim_descritor']
        
        for dim in dimensions:
            print(f"📊 Migrando {dim}...")
            
            # Ler dados do SQLite
            df = pd.read_sql_query(f"SELECT * FROM {dim}", sqlite_conn)
            
            # Criar tabela no DuckDB com tipos otimizados
            duck_conn.register(f"{dim}_temp", df)
            duck_conn.execute(f"CREATE TABLE {dim} AS SELECT * FROM {dim}_temp")
            duck_conn.execute(f"DROP VIEW {dim}_temp")
    
    def _migrate_fact_table(self, sqlite_conn, duck_conn):
        """Migra tabela fato com otimizações"""
        print("⭐ Migrando fato_resposta_aluno (pode demorar)...")
        
        # Migrar em chunks para eficiência
        chunk_size = 100000
        offset = 0
        
        # Criar tabela vazia primeiro
        duck_conn.execute("""
        CREATE TABLE fato_resposta_aluno (
            MUN_UF VARCHAR,
            MUN_NOME VARCHAR,
            ESC_INEP VARCHAR,
            SER_NUMBER INTEGER,
            SER_NOME VARCHAR,
            TUR_PERIODO VARCHAR,
            TUR_NOME VARCHAR,
            ALU_ID INTEGER,
            AVA_NOME VARCHAR,
            AVA_ANO INTEGER,
            DIS_NOME VARCHAR,
            TES_NOME VARCHAR,
            MTI_CODIGO VARCHAR,
            ACERTO INTEGER,
            ERRO INTEGER
        )
        """)
        
        while True:
            # Ler chunk do SQLite
            query = f"""
            SELECT * FROM fato_resposta_aluno 
            LIMIT {chunk_size} OFFSET {offset}
            """
            df = pd.read_sql_query(query, sqlite_conn)
            
            if df.empty:
                break
                
            # Inserir no DuckDB
            duck_conn.register("chunk_temp", df)
            duck_conn.execute("INSERT INTO fato_resposta_aluno SELECT * FROM chunk_temp")
            duck_conn.execute("DROP VIEW chunk_temp")
            
            offset += chunk_size
            print(f"   📦 Processados {offset:,} registros...")
    
    def _create_optimized_indexes(self, duck_conn):
        """Cria índices otimizados para consultas analíticas"""
        print("🔧 Criando índices otimizados...")
        
        # Índices para filtros comuns
        indexes = [
            "CREATE INDEX idx_fact_ano ON fato_resposta_aluno(AVA_ANO)",
            "CREATE INDEX idx_fact_disciplina ON fato_resposta_aluno(DIS_NOME)", 
            "CREATE INDEX idx_fact_municipio ON fato_resposta_aluno(MUN_NOME)",
            "CREATE INDEX idx_fact_escola ON fato_resposta_aluno(ESC_INEP)",
            "CREATE INDEX idx_fact_serie ON fato_resposta_aluno(SER_NOME)",
            
            # Índices compostos para joins
            "CREATE INDEX idx_fact_aluno ON fato_resposta_aluno(ALU_ID)",
            "CREATE INDEX idx_fact_descritor ON fato_resposta_aluno(MTI_CODIGO)",
        ]
        
        for idx in indexes:
            try:
                duck_conn.execute(idx)
            except Exception as e:
                print(f"⚠️ Aviso ao criar índice: {e}")


class SAEVDuckDBConnector:
    """Connector otimizado para DuckDB no sistema SAEV"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Conecta ao DuckDB com configurações otimizadas"""
        self.conn = duckdb.connect(self.db_path)
        
        # Configurações de performance
        self.conn.execute("SET threads=4")  # Usar múltiplos threads
        self.conn.execute("SET memory_limit='2GB'")  # Limite de memória
        self.conn.execute("SET enable_progress_bar=true")  # Barra de progresso
        
        return self.conn
    
    def query_to_df(self, query: str) -> pd.DataFrame:
        """Executa query e retorna DataFrame"""
        if not self.conn:
            self.connect()
        
        return self.conn.execute(query).fetchdf()
    
    def benchmark_query(self, query: str, name: str = "Query"):
        """Executa query com benchmark de performance"""
        start_time = time.time()
        result = self.query_to_df(query)
        elapsed = time.time() - start_time
        
        print(f"⚡ {name}: {elapsed:.3f}s | {len(result):,} registros")
        return result
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
            self.conn = None


def migrate_saev_to_duckdb(env: str = 'teste') -> bool:
    """Migra banco SAEV SQLite para DuckDB"""
    from src.config import config
    
    try:
        # Paths dos bancos
        sqlite_path = config.get_database_path(env)
        duckdb_path = sqlite_path.replace('.db', '_duckdb.db')
        
        if not Path(sqlite_path).exists():
            print(f"❌ Banco SQLite não encontrado: {sqlite_path}")
            return False
        
        # Executar migração
        migrator = DuckDBMigrator(sqlite_path, duckdb_path)
        success = migrator.migrate_to_duckdb()
        
        if success:
            print(f"✅ Banco DuckDB criado: {duckdb_path}")
            print(f"📊 Para usar, configure: SAEV_DATABASE_PATH={duckdb_path}")
        
        return success
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False


def benchmark_comparison(env: str = 'teste'):
    """Compara performance SQLite vs DuckDB"""
    from src.config import config
    
    sqlite_path = config.get_database_path(env)
    duckdb_path = sqlite_path.replace('.db', '_duckdb.db')
    
    if not Path(duckdb_path).exists():
        print("❌ Execute a migração primeiro: migrate_saev_to_duckdb()")
        return
    
    # Queries de benchmark
    test_queries = [
        ("Contagem total", "SELECT COUNT(*) FROM fato_resposta_aluno"),
        ("Agregação por ano", "SELECT AVA_ANO, SUM(ACERTO), SUM(ERRO) FROM fato_resposta_aluno GROUP BY AVA_ANO"),
        ("Top municípios", """
         SELECT MUN_NOME, 
                SUM(ACERTO) as acertos,
                SUM(ACERTO + ERRO) as total,
                ROUND(SUM(ACERTO) * 100.0 / SUM(ACERTO + ERRO), 2) as taxa
         FROM fato_resposta_aluno 
         GROUP BY MUN_NOME 
         ORDER BY taxa DESC 
         LIMIT 10
         """),
        ("Join com dimensões", """
         SELECT e.ESC_NOME,
                COUNT(DISTINCT f.ALU_ID) as alunos,
                AVG(f.ACERTO * 100.0 / (f.ACERTO + f.ERRO)) as taxa_media
         FROM fato_resposta_aluno f
         JOIN dim_escola e ON f.ESC_INEP = e.ESC_INEP
         GROUP BY e.ESC_NOME
         ORDER BY taxa_media DESC
         LIMIT 20
         """)
    ]
    
    print("🏁 BENCHMARK: SQLite vs DuckDB")
    print("="*50)
    
    # SQLite
    print("\n📊 SQLite:")
    sqlite_conn = sqlite3.connect(sqlite_path)
    for name, query in test_queries:
        start = time.time()
        result = pd.read_sql_query(query, sqlite_conn)
        elapsed = time.time() - start
        print(f"   {name}: {elapsed:.3f}s | {len(result):,} registros")
    sqlite_conn.close()
    
    # DuckDB
    print("\n🦆 DuckDB:")
    duck = SAEVDuckDBConnector(duckdb_path)
    duck.connect()
    for name, query in test_queries:
        duck.benchmark_query(query, name)
    duck.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        env = sys.argv[2] if len(sys.argv) > 2 else 'teste'
        migrate_saev_to_duckdb(env)
    elif len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        env = sys.argv[2] if len(sys.argv) > 2 else 'teste'
        benchmark_comparison(env)
    else:
        print("""
🦆 SAEV DuckDB Migration Tool

Uso:
    python duckdb_migration.py migrate [teste|producao]    # Migrar dados
    python duckdb_migration.py benchmark [teste|producao]  # Comparar performance
        
Exemplos:
    python duckdb_migration.py migrate teste
    python duckdb_migration.py benchmark teste
        """)
