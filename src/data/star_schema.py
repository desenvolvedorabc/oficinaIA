"""
Sistema de Otimização com Star Schema para SAEV
Migra dados da estrutura atual para arquitetura Star Schema otimizada
"""
import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Adicionar o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import config

class SAEVStarSchema:
    """Classe para migração e otimização com Star Schema"""
    
    def __init__(self, source_db_path: str = None, optimized_db_path: str = None):
        """
        Inicializa o sistema de otimização
        
        Args:
            source_db_path: Caminho do banco original (atual)
            optimized_db_path: Caminho do banco otimizado (Star Schema)
        """
        if source_db_path is None:
            self.source_db_path = config.get_database_path()
        else:
            self.source_db_path = source_db_path
            
        if optimized_db_path is None:
            base_path = Path(self.source_db_path).parent
            if 'teste' in self.source_db_path:
                self.optimized_db_path = str(base_path / 'avaliacao_teste_optimized.db')
            else:
                self.optimized_db_path = str(base_path / 'avaliacao_prod_optimized.db')
        else:
            self.optimized_db_path = optimized_db_path
    
    def create_star_schema(self):
        """Cria a estrutura Star Schema otimizada"""
        conn = sqlite3.connect(self.optimized_db_path)
        cursor = conn.cursor()
        
        print("🏗️ Criando estrutura Star Schema...")
        
        # DIMENSÃO: MUNICÍPIOS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_municipio (
                municipio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mun_uf CHAR(2),
                mun_nome VARCHAR(60),
                UNIQUE(mun_uf, mun_nome)
            )
        ''')
        
        # DIMENSÃO: ESCOLAS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_escola (
                escola_id INTEGER PRIMARY KEY AUTOINCREMENT,
                esc_inep CHAR(8) UNIQUE,
                esc_nome VARCHAR(80),
                municipio_id INTEGER,
                FOREIGN KEY (municipio_id) REFERENCES dim_municipio(municipio_id)
            )
        ''')
        
        # DIMENSÃO: SÉRIES
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_serie (
                serie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ser_number INTEGER,
                ser_nome VARCHAR(30),
                UNIQUE(ser_number, ser_nome)
            )
        ''')
        
        # DIMENSÃO: DISCIPLINAS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_disciplina (
                disciplina_id INTEGER PRIMARY KEY AUTOINCREMENT,
                dis_nome VARCHAR(30) UNIQUE
            )
        ''')
        
        # DIMENSÃO: COMPETÊNCIAS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_competencia (
                competencia_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mti_codigo VARCHAR(15) UNIQUE,
                mti_descritor VARCHAR(512)
            )
        ''')
        
        # DIMENSÃO: TEMPO
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_tempo (
                tempo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ava_ano INTEGER UNIQUE,
                ava_nome VARCHAR(50)
            )
        ''')
        
        # FATO: DESEMPENHO AGREGADO POR ESCOLA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fato_desempenho_escola (
                escola_id INTEGER,
                serie_id INTEGER,
                disciplina_id INTEGER,
                tempo_id INTEGER,
                total_alunos INTEGER,
                total_questoes INTEGER,
                total_acertos INTEGER,
                taxa_acerto REAL,
                media_competencias REAL,
                desvio_padrao REAL,
                PRIMARY KEY (escola_id, serie_id, disciplina_id, tempo_id),
                FOREIGN KEY (escola_id) REFERENCES dim_escola(escola_id),
                FOREIGN KEY (serie_id) REFERENCES dim_serie(serie_id),
                FOREIGN KEY (disciplina_id) REFERENCES dim_disciplina(disciplina_id),
                FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id)
            )
        ''')
        
        # FATO: DESEMPENHO POR COMPETÊNCIA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fato_competencia (
                escola_id INTEGER,
                serie_id INTEGER,
                disciplina_id INTEGER,
                competencia_id INTEGER,
                tempo_id INTEGER,
                total_alunos INTEGER,
                total_questoes INTEGER,
                total_acertos INTEGER,
                taxa_acerto REAL,
                PRIMARY KEY (escola_id, serie_id, disciplina_id, competencia_id, tempo_id),
                FOREIGN KEY (escola_id) REFERENCES dim_escola(escola_id),
                FOREIGN KEY (serie_id) REFERENCES dim_serie(serie_id),
                FOREIGN KEY (disciplina_id) REFERENCES dim_disciplina(disciplina_id),
                FOREIGN KEY (competencia_id) REFERENCES dim_competencia(competencia_id),
                FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id)
            )
        ''')
        
        # FATO: AGREGAÇÃO MUNICIPAL (PRÉ-CALCULADA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fato_municipio (
                municipio_id INTEGER,
                serie_id INTEGER,
                disciplina_id INTEGER,
                tempo_id INTEGER,
                total_escolas INTEGER,
                total_alunos INTEGER,
                total_questoes INTEGER,
                total_acertos INTEGER,
                taxa_acerto REAL,
                media_portugues REAL,
                media_matematica REAL,
                ranking_posicao INTEGER,
                PRIMARY KEY (municipio_id, serie_id, disciplina_id, tempo_id),
                FOREIGN KEY (municipio_id) REFERENCES dim_municipio(municipio_id),
                FOREIGN KEY (serie_id) REFERENCES dim_serie(serie_id),
                FOREIGN KEY (disciplina_id) REFERENCES dim_disciplina(disciplina_id),
                FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id)
            )
        ''')
        
        print("✅ Estrutura Star Schema criada com sucesso!")
        
        # Criar índices otimizados
        self._create_optimized_indexes(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_optimized_indexes(self, cursor):
        """Cria índices otimizados para consultas rápidas"""
        print("📊 Criando índices otimizados...")
        
        indexes = [
            # Índices nas tabelas dimensão
            'CREATE INDEX IF NOT EXISTS idx_municipio_nome ON dim_municipio(mun_nome)',
            'CREATE INDEX IF NOT EXISTS idx_escola_inep ON dim_escola(esc_inep)',
            'CREATE INDEX IF NOT EXISTS idx_escola_municipio ON dim_escola(municipio_id)',
            'CREATE INDEX IF NOT EXISTS idx_serie_number ON dim_serie(ser_number)',
            'CREATE INDEX IF NOT EXISTS idx_disciplina_nome ON dim_disciplina(dis_nome)',
            'CREATE INDEX IF NOT EXISTS idx_competencia_codigo ON dim_competencia(mti_codigo)',
            'CREATE INDEX IF NOT EXISTS idx_tempo_ano ON dim_tempo(ava_ano)',
            
            # Índices nas tabelas fato (consultas mais comuns)
            'CREATE INDEX IF NOT EXISTS idx_fato_escola_serie_disc ON fato_desempenho_escola(serie_id, disciplina_id)',
            'CREATE INDEX IF NOT EXISTS idx_fato_escola_tempo ON fato_desempenho_escola(tempo_id)',
            'CREATE INDEX IF NOT EXISTS idx_fato_municipio_serie_disc ON fato_municipio(serie_id, disciplina_id)',
            'CREATE INDEX IF NOT EXISTS idx_fato_municipio_tempo ON fato_municipio(tempo_id)',
            'CREATE INDEX IF NOT EXISTS idx_fato_municipio_ranking ON fato_municipio(ranking_posicao)',
            'CREATE INDEX IF NOT EXISTS idx_fato_competencia_escola ON fato_competencia(escola_id)',
            'CREATE INDEX IF NOT EXISTS idx_fato_competencia_comp ON fato_competencia(competencia_id)',
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        print("✅ Índices criados com sucesso!")
    
    def migrate_data(self):
        """Migra dados da estrutura atual para Star Schema"""
        print("🚀 Iniciando migração de dados...")
        
        source_conn = sqlite3.connect(self.source_db_path)
        target_conn = sqlite3.connect(self.optimized_db_path)
        
        try:
            # 1. Migrar dimensões
            self._migrate_dimensions(source_conn, target_conn)
            
            # 2. Migrar e agregar fatos
            self._migrate_facts(source_conn, target_conn)
            
            print("✅ Migração concluída com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            target_conn.rollback()
            raise
        
        finally:
            source_conn.close()
            target_conn.close()
    
    def _migrate_dimensions(self, source_conn, target_conn):
        """Migra dados para as tabelas dimensão"""
        print("📦 Migrando dimensões...")
        
        # DIMENSÃO MUNICÍPIOS
        municipios_df = pd.read_sql_query('''
            SELECT DISTINCT MUN_UF, MUN_NOME 
            FROM avaliacao 
            ORDER BY MUN_NOME
        ''', source_conn)
        municipios_df.to_sql('dim_municipio', target_conn, if_exists='append', index=False)
        
        # DIMENSÃO ESCOLAS
        escolas_df = pd.read_sql_query('''
            SELECT DISTINCT 
                a.ESC_INEP, 
                a.ESC_NOME,
                m.municipio_id
            FROM avaliacao a
            JOIN dim_municipio m ON a.MUN_NOME = m.mun_nome AND a.MUN_UF = m.mun_uf
            ORDER BY a.ESC_NOME
        ''', target_conn)
        escolas_df.to_sql('dim_escola', target_conn, if_exists='append', index=False)
        
        # DIMENSÃO SÉRIES
        series_df = pd.read_sql_query('''
            SELECT DISTINCT SER_NUMBER, SER_NOME 
            FROM avaliacao 
            ORDER BY SER_NUMBER
        ''', source_conn)
        series_df.to_sql('dim_serie', target_conn, if_exists='append', index=False)
        
        # DIMENSÃO DISCIPLINAS
        disciplinas_df = pd.read_sql_query('''
            SELECT DISTINCT DIS_NOME 
            FROM avaliacao 
            ORDER BY DIS_NOME
        ''', source_conn)
        disciplinas_df.to_sql('dim_disciplina', target_conn, if_exists='append', index=False)
        
        # DIMENSÃO COMPETÊNCIAS
        competencias_df = pd.read_sql_query('''
            SELECT DISTINCT MTI_CODIGO, MTI_DESCRITOR 
            FROM avaliacao 
            WHERE MTI_CODIGO IS NOT NULL
            ORDER BY MTI_CODIGO
        ''', source_conn)
        competencias_df.to_sql('dim_competencia', target_conn, if_exists='append', index=False)
        
        # DIMENSÃO TEMPO
        tempo_df = pd.read_sql_query('''
            SELECT DISTINCT AVA_ANO, AVA_NOME 
            FROM avaliacao 
            ORDER BY AVA_ANO
        ''', source_conn)
        tempo_df.to_sql('dim_tempo', target_conn, if_exists='append', index=False)
        
        target_conn.commit()
        print("✅ Dimensões migradas!")
    
    def _migrate_facts(self, source_conn, target_conn):
        """Migra e agrega dados para as tabelas fato"""
        print("🎯 Migrando e agregando fatos...")
        
        # FATO: DESEMPENHO POR ESCOLA (PRÉ-AGREGADO)
        fato_escola_query = '''
            INSERT INTO fato_desempenho_escola (
                escola_id, serie_id, disciplina_id, tempo_id,
                total_alunos, total_questoes, total_acertos, 
                taxa_acerto, media_competencias, desvio_padrao
            )
            SELECT 
                e.escola_id,
                s.serie_id,
                d.disciplina_id,
                t.tempo_id,
                COUNT(DISTINCT a.ALU_ID) as total_alunos,
                COUNT(*) as total_questoes,
                SUM(CAST(a.ATR_CERTO AS INTEGER)) as total_acertos,
                AVG(CAST(a.ATR_CERTO AS FLOAT)) * 100 as taxa_acerto,
                COUNT(DISTINCT a.MTI_CODIGO) as media_competencias,
                CASE 
                    WHEN COUNT(*) > 1 THEN 
                        SQRT(SUM((CAST(a.ATR_CERTO AS FLOAT) - AVG(CAST(a.ATR_CERTO AS FLOAT))) * 
                                 (CAST(a.ATR_CERTO AS FLOAT) - AVG(CAST(a.ATR_CERTO AS FLOAT)))) / (COUNT(*) - 1)) * 100
                    ELSE 0 
                END as desvio_padrao
            FROM avaliacao a
            JOIN dim_escola e ON a.ESC_INEP = e.esc_inep
            JOIN dim_serie s ON a.SER_NUMBER = s.ser_number
            JOIN dim_disciplina d ON a.DIS_NOME = d.dis_nome
            JOIN dim_tempo t ON a.AVA_ANO = t.ava_ano
            GROUP BY e.escola_id, s.serie_id, d.disciplina_id, t.tempo_id
            HAVING total_alunos >= 10
        '''
        
        target_conn.execute(fato_escola_query)
        
        # FATO: DESEMPENHO POR COMPETÊNCIA
        fato_competencia_query = '''
            INSERT INTO fato_competencia (
                escola_id, serie_id, disciplina_id, competencia_id, tempo_id,
                total_alunos, total_questoes, total_acertos, taxa_acerto
            )
            SELECT 
                e.escola_id,
                s.serie_id,
                d.disciplina_id,
                c.competencia_id,
                t.tempo_id,
                COUNT(DISTINCT a.ALU_ID) as total_alunos,
                COUNT(*) as total_questoes,
                SUM(CAST(a.ATR_CERTO AS INTEGER)) as total_acertos,
                AVG(CAST(a.ATR_CERTO AS FLOAT)) * 100 as taxa_acerto
            FROM avaliacao a
            JOIN dim_escola e ON a.ESC_INEP = e.esc_inep
            JOIN dim_serie s ON a.SER_NUMBER = s.ser_number
            JOIN dim_disciplina d ON a.DIS_NOME = d.dis_nome
            JOIN dim_competencia c ON a.MTI_CODIGO = c.mti_codigo
            JOIN dim_tempo t ON a.AVA_ANO = t.ava_ano
            WHERE a.MTI_CODIGO IS NOT NULL
            GROUP BY e.escola_id, s.serie_id, d.disciplina_id, c.competencia_id, t.tempo_id
            HAVING total_alunos >= 5
        '''
        
        target_conn.execute(fato_competencia_query)
        
        # FATO: AGREGAÇÃO MUNICIPAL (SUPER OTIMIZADA)
        fato_municipio_query = '''
            INSERT INTO fato_municipio (
                municipio_id, serie_id, disciplina_id, tempo_id,
                total_escolas, total_alunos, total_questoes, total_acertos, taxa_acerto,
                media_portugues, media_matematica, ranking_posicao
            )
            SELECT 
                m.municipio_id,
                s.serie_id,
                d.disciplina_id,
                t.tempo_id,
                COUNT(DISTINCT e.escola_id) as total_escolas,
                SUM(fe.total_alunos) as total_alunos,
                SUM(fe.total_questoes) as total_questoes,
                SUM(fe.total_acertos) as total_acertos,
                AVG(fe.taxa_acerto) as taxa_acerto,
                CASE WHEN d.dis_nome = 'Português' THEN AVG(fe.taxa_acerto) ELSE NULL END as media_portugues,
                CASE WHEN d.dis_nome = 'Matemática' THEN AVG(fe.taxa_acerto) ELSE NULL END as media_matematica,
                RANK() OVER (PARTITION BY s.serie_id, d.disciplina_id, t.tempo_id ORDER BY AVG(fe.taxa_acerto) DESC) as ranking_posicao
            FROM fato_desempenho_escola fe
            JOIN dim_escola e ON fe.escola_id = e.escola_id
            JOIN dim_municipio m ON e.municipio_id = m.municipio_id
            JOIN dim_serie s ON fe.serie_id = s.serie_id
            JOIN dim_disciplina d ON fe.disciplina_id = d.disciplina_id
            JOIN dim_tempo t ON fe.tempo_id = t.tempo_id
            GROUP BY m.municipio_id, s.serie_id, d.disciplina_id, t.tempo_id
        '''
        
        target_conn.execute(fato_municipio_query)
        
        target_conn.commit()
        print("✅ Fatos migrados e agregados!")
    
    def analyze_performance_improvement(self):
        """Analisa melhoria de performance entre as duas estruturas"""
        print("📊 Analisando melhoria de performance...")
        
        import time
        
        # Teste na estrutura original
        original_conn = sqlite3.connect(self.source_db_path)
        start_time = time.time()
        
        original_query = '''
            SELECT 
                MUN_NOME,
                SER_NOME,
                DIS_NOME,
                COUNT(DISTINCT ALU_ID) as total_alunos,
                AVG(CAST(ATR_CERTO AS FLOAT)) * 100 as taxa_acerto
            FROM avaliacao 
            GROUP BY MUN_NOME, SER_NOME, DIS_NOME
            ORDER BY taxa_acerto DESC
            LIMIT 20
        '''
        
        df_original = pd.read_sql_query(original_query, original_conn)
        original_time = time.time() - start_time
        original_conn.close()
        
        # Teste na estrutura otimizada
        optimized_conn = sqlite3.connect(self.optimized_db_path)
        start_time = time.time()
        
        optimized_query = '''
            SELECT 
                m.mun_nome,
                s.ser_nome,
                d.dis_nome,
                fm.total_alunos,
                fm.taxa_acerto
            FROM fato_municipio fm
            JOIN dim_municipio m ON fm.municipio_id = m.municipio_id
            JOIN dim_serie s ON fm.serie_id = s.serie_id
            JOIN dim_disciplina d ON fm.disciplina_id = d.disciplina_id
            ORDER BY fm.taxa_acerto DESC
            LIMIT 20
        '''
        
        df_optimized = pd.read_sql_query(optimized_query, optimized_conn)
        optimized_time = time.time() - start_time
        optimized_conn.close()
        
        # Resultados
        improvement = ((original_time - optimized_time) / original_time) * 100
        
        print(f"\n📈 RESULTADOS DA OTIMIZAÇÃO:")
        print(f"⏱️  Tempo estrutura original: {original_time:.3f}s")
        print(f"🚀 Tempo estrutura otimizada: {optimized_time:.3f}s")
        print(f"📊 Melhoria de performance: {improvement:.1f}%")
        print(f"⚡ Speedup: {original_time/optimized_time:.1f}x mais rápido")
        
        return {
            'original_time': original_time,
            'optimized_time': optimized_time,
            'improvement_percent': improvement,
            'speedup_factor': original_time/optimized_time
        }

def main():
    """Função principal para executar migração"""
    print("🌟 SAEV Star Schema Migration Tool")
    print("=" * 50)
    
    migrator = SAEVStarSchema()
    
    try:
        # 1. Criar estrutura
        migrator.create_star_schema()
        
        # 2. Migrar dados
        migrator.migrate_data()
        
        # 3. Analisar performance
        results = migrator.analyze_performance_improvement()
        
        print(f"\n✅ MIGRAÇÃO CONCLUÍDA!")
        print(f"🔗 Banco otimizado criado: {migrator.optimized_db_path}")
        print(f"🚀 Speedup alcançado: {results['speedup_factor']:.1f}x")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
