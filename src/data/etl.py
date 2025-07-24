"""
Módulo para processos de ETL dos dados do SAEV
"""
import sqlite3
import pandas as pd
import logging
from pathlib import Path
from typing import List, Optional
import hashlib
import subprocess
import os

class SAEVDataProcessor:
    """Classe para processamento de dados do SAEV"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger"""
        logger = logging.getLogger(__name__)
        
        # Evitar duplicação de handlers
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def create_database_structure(self, overwrite: bool = False):
        """Cria a estrutura do banco de dados"""
        # Verificar se deve sobrescrever o banco existente
        if overwrite and Path(self.db_path).exists():
            self.logger.info(f"🗑️  Removendo banco existente: {self.db_path}")
            Path(self.db_path).unlink()
        
        # Criar diretório se não existir
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"🏗️  Criando estrutura do banco: {self.db_path}")
        
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
        self.logger.info("📊 Criando índices para otimização...")
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_municipio ON avaliacao(MUN_NOME)',
            'CREATE INDEX IF NOT EXISTS idx_escola ON avaliacao(ESC_INEP)',
            'CREATE INDEX IF NOT EXISTS idx_avaliacao_ano ON avaliacao(AVA_ANO)',
            'CREATE INDEX IF NOT EXISTS idx_disciplina ON avaliacao(DIS_NOME)',
            'CREATE INDEX IF NOT EXISTS idx_serie ON avaliacao(SER_NUMBER)',
            'CREATE INDEX IF NOT EXISTS idx_serie_nome ON avaliacao(SER_NOME)',
            'CREATE INDEX IF NOT EXISTS idx_teste_nome ON avaliacao(TES_NOME)'
        ]
        
        for index in indexes:
            cursor.execute(index)
        
        conn.commit()
        conn.close()
        self.logger.info("✅ Estrutura do banco criada com sucesso")
    
    def load_csv_data(self, csv_path: str = None, csv_folder: str = None, 
                     test_mode: bool = False, allowed_cities: Optional[List[str]] = None):
        """Carrega dados do CSV ou de múltiplos CSVs de uma pasta para o banco"""
        try:
            dataframes = []
            
            if csv_folder:
                # Processar todos os arquivos CSV da pasta
                csv_folder_path = Path(csv_folder)
                if not csv_folder_path.exists():
                    raise FileNotFoundError(f"Pasta não encontrada: {csv_folder}")
                
                csv_files = list(csv_folder_path.glob("*.csv"))
                if not csv_files:
                    raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {csv_folder}")
                
                self.logger.info(f"📁 Processando pasta: {csv_folder}")
                self.logger.info(f"� Arquivos encontrados: {len(csv_files)}")
                
                for csv_file in sorted(csv_files):
                    self.logger.info(f"�📥 Carregando: {csv_file.name}")
                    df = pd.read_csv(csv_file, encoding='utf-8')
                    self.logger.info(f"   📊 {len(df):,} registros em {csv_file.name}")
                    dataframes.append(df)
                
                # Combinar todos os DataFrames
                df_combined = pd.concat(dataframes, ignore_index=True)
                self.logger.info(f"📄 Total combinado: {len(df_combined):,} registros")
                
            else:
                # Processar arquivo único (modo legado)
                if not csv_path:
                    raise ValueError("É necessário especificar csv_path ou csv_folder")
                
                self.logger.info(f"📥 Carregando dados do CSV: {csv_path}")
                df_combined = pd.read_csv(csv_path, encoding='utf-8')
                self.logger.info(f"📄 Total de registros no CSV: {len(df_combined)}")
            
            if test_mode and allowed_cities:
                original_count = len(df_combined)
                df_combined = df_combined[df_combined['MUN_NOME'].isin(allowed_cities)]
                self.logger.info(f"🏷️  Filtrando municípios: {len(df_combined):,}/{original_count:,} registros mantidos")
                df_combined = self._anonymize_data(df_combined)
                self.logger.info("🔒 Dados anonimizados para ambiente de teste")
            
            # Conectar ao banco e inserir dados
            conn = sqlite3.connect(self.db_path)
            
            # Limpar dados existentes se necessário
            cursor = conn.cursor()
            cursor.execute("DELETE FROM avaliacao")
            conn.commit()
            
            df_combined.to_sql('avaliacao', conn, if_exists='append', index=False)
            conn.close()
            
            self.logger.info(f"✅ Dados carregados com sucesso: {len(df_combined):,} registros")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {e}")
            raise
    
    def _anonymize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Anonimiza dados sensíveis para ambiente de teste"""
        sensitive_fields = ['ALU_NOME', 'ALU_CPF', 'MUN_NOME', 'ESC_NOME']
        
        for field in sensitive_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: hashlib.md5(str(x).encode()).hexdigest()[:10]
                )
        
        return df
    
    def apply_star_schema(self):
        """Aplica transformação Star Schema ao banco de dados"""
        try:
            self.logger.info("⭐ Iniciando transformação Star Schema...")
            
            # Caminhos absolutos
            db_path_abs = Path(self.db_path).resolve()
            project_root = Path(__file__).parent.parent
            star_schema_script = project_root / "star_schema.sql"
            
            if not star_schema_script.exists():
                raise FileNotFoundError(f"Script Star Schema não encontrado: {star_schema_script}")
            
            if not db_path_abs.exists():
                raise FileNotFoundError(f"Banco de dados não encontrado: {db_path_abs}")
            
            # Executar o script SQL usando sqlite3 command line com caminhos absolutos
            cmd = f"sqlite3 '{db_path_abs}' < '{star_schema_script}'"
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Erro na execução do Star Schema: {result.stderr}")
            
            self.logger.info("✅ Transformação Star Schema aplicada com sucesso")
            
            # Validar a transformação
            validation_results = self._validate_star_schema()
            
            self.logger.info("📊 Resultado da transformação Star Schema:")
            for table, count in validation_results.items():
                self.logger.info(f"   • {table}: {count:,} registros")
                
        except Exception as e:
            self.logger.error(f"❌ Erro na transformação Star Schema: {e}")
            raise
    
    def _validate_star_schema(self) -> dict:
        """Valida a estrutura do Star Schema criada"""
        conn = sqlite3.connect(self.db_path)
        
        validation_queries = {
            'dim_aluno': 'SELECT COUNT(*) FROM dim_aluno',
            'dim_escola': 'SELECT COUNT(*) FROM dim_escola', 
            'dim_descritor': 'SELECT COUNT(*) FROM dim_descritor',
            'fato_resposta_aluno': 'SELECT COUNT(*) FROM fato_resposta_aluno',
            'teste': 'SELECT COUNT(*) FROM teste'
        }
        
        results = {}
        for table, query in validation_queries.items():
            try:
                cursor = conn.execute(query)
                results[table] = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                results[table] = 0  # Tabela não existe
        
        conn.close()
        return results
    
    def validate_data(self) -> dict:
        """Valida a qualidade dos dados carregados"""
        self.logger.info("🔍 Validando qualidade dos dados...")
        
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
        
        # Log dos resultados
        self.logger.info("📈 Estatísticas dos dados:")
        self.logger.info(f"   • Total de registros: {results['total_records']:,}")
        self.logger.info(f"   • Alunos únicos: {results['unique_students']:,}")
        self.logger.info(f"   • Escolas: {results['schools_count']:,}")
        self.logger.info(f"   • Municípios: {results['cities_count']:,}")
        
        if results['null_students'] > 0:
            self.logger.warning(f"⚠️  Encontrados {results['null_students']} registros com ALU_ID nulo")
        
        if results['invalid_answers'] > 0:
            self.logger.warning(f"⚠️  Encontrados {results['invalid_answers']} registros com respostas inválidas")
        
        return results
    
    def full_etl_process(self, csv_path: str = None, csv_folder: str = None,
                        test_mode: bool = False, allowed_cities: Optional[List[str]] = None, 
                        apply_star_schema: bool = True, overwrite_db: bool = True):
        """Executa o processo completo de ETL"""
        self.logger.info("🚀 Iniciando processo completo de ETL...")
        
        try:
            # 1. Criar estrutura do banco
            self.create_database_structure(overwrite=overwrite_db)
            
            # 2. Carregar dados do CSV ou pasta
            self.load_csv_data(csv_path=csv_path, csv_folder=csv_folder, 
                             test_mode=test_mode, allowed_cities=allowed_cities)
            
            # 3. Validar dados carregados
            validation_results = self.validate_data()
            
            # 4. Aplicar Star Schema (se solicitado)
            if apply_star_schema:
                self.apply_star_schema()
            
            self.logger.info("🎉 Processo de ETL concluído com sucesso!")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"💥 Falha no processo de ETL: {e}")
            raise
