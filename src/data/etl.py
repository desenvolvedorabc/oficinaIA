"""
Módulo para processos de ETL dos dados do SAEV
"""
import sqlite3
import pandas as pd
import logging
from pathlib import Path
from typing import List, Optional
import hashlib

class SAEVDataProcessor:
    """Classe para processamento de dados do SAEV"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def create_database_structure(self):
        """Cria a estrutura do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # DDL da tabela avaliacao
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avaliacao (
                MUN_UF         CHAR(2),
                MUN_NOME       VARCHAR(60),
                ESC_INEP       CHAR(8),
                ESC_NOME       VARCHAR(80),
                SER_NUMBER     INTEGER,
                SER_NOME       VARCHAR(30),
                TUR_PERIODO    VARCHAR(15),
                TUR_NOME       VARCHAR(20),
                ALU_ID         INTEGER,
                ALU_NOME       VARCHAR(80),
                ALU_CPF        VARCHAR(15),
                AVA_NOME       VARCHAR(50),
                AVA_ANO        INTEGER,
                DIS_NOME       VARCHAR(30),
                TES_NOME       VARCHAR(30),
                TEG_ORDEM      INTEGER,
                ATR_RESPOSTA   CHAR(1),
                ATR_CERTO      INTEGER,
                MTI_CODIGO     VARCHAR(15),
                MTI_DESCRITOR  VARCHAR(512)
            )
        ''')
        
        # Criar índices para melhor performance
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_municipio ON avaliacao(MUN_NOME)',
            'CREATE INDEX IF NOT EXISTS idx_escola ON avaliacao(ESC_INEP)',
            'CREATE INDEX IF NOT EXISTS idx_avaliacao_ano ON avaliacao(AVA_ANO)',
            'CREATE INDEX IF NOT EXISTS idx_disciplina ON avaliacao(DIS_NOME)',
            'CREATE INDEX IF NOT EXISTS idx_serie ON avaliacao(SER_NUMBER)'
        ]
        
        for index in indexes:
            cursor.execute(index)
        
        conn.commit()
        conn.close()
        self.logger.info("Estrutura do banco criada com sucesso")
    
    def load_csv_data(self, csv_path: str, test_mode: bool = False, 
                     allowed_cities: Optional[List[str]] = None):
        """Carrega dados do CSV para o banco"""
        try:
            # Ler CSV com pandas para melhor tratamento de dados
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            if test_mode and allowed_cities:
                df = df[df['MUN_NOME'].isin(allowed_cities)]
                df = self._anonymize_data(df)
            
            # Conectar ao banco e inserir dados
            conn = sqlite3.connect(self.db_path)
            df.to_sql('avaliacao', conn, if_exists='append', index=False)
            conn.close()
            
            self.logger.info(f"Dados carregados: {len(df)} registros de {csv_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def _anonymize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Anonimiza dados sensíveis"""
        sensitive_fields = ['ALU_NOME', 'ALU_CPF', 'MUN_NOME', 'ESC_NOME']
        
        for field in sensitive_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: hashlib.md5(str(x).encode()).hexdigest()[:10]
                )
        
        return df
    
    def validate_data(self) -> dict:
        """Valida a qualidade dos dados carregados"""
        conn = sqlite3.connect(self.db_path)
        
        validation_queries = {
            'total_records': 'SELECT COUNT(*) FROM avaliacao',
            'null_students': 'SELECT COUNT(*) FROM avaliacao WHERE ALU_ID IS NULL',
            'invalid_answers': 'SELECT COUNT(*) FROM avaliacao WHERE ATR_CERTO NOT IN (0, 1)',
            'unique_students': 'SELECT COUNT(DISTINCT ALU_ID) FROM avaliacao',
            'schools_count': 'SELECT COUNT(DISTINCT ESC_INEP) FROM avaliacao',
            'cities_count': 'SELECT COUNT(DISTINCT MUN_NOME) FROM avaliacao'
        }
        
        results = {}
        for key, query in validation_queries.items():
            cursor = conn.execute(query)
            results[key] = cursor.fetchone()[0]
        
        conn.close()
        return results
