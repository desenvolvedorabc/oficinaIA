"""
Sistema de Relatórios Automatizados para SAEV
"""
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Adicionar o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import config

class SAEVReports:
    """Classe para geração de relatórios automatizados"""
    
    def __init__(self, db_path: str = None, output_dir: str = "reports"):
        # Se não especificar db_path, usa detecção automática
        if db_path is None:
            self.db_path = config.get_database_path()
        else:
            self.db_path = db_path
            
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Verificar se o banco existe
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
    
    def get_data(self, query: str) -> pd.DataFrame:
        """Executa query e retorna DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            raise Exception(f"Erro ao executar consulta: {e}")
    
    def generate_municipal_report(self, year: int, discipline: str) -> str:
        """Gera relatório por município"""
        
        query = f"""
        SELECT 
            MUN_NOME as Municipio,
            COUNT(DISTINCT ALU_ID) as Total_Alunos,
            COUNT(DISTINCT ESC_INEP) as Total_Escolas,
            COUNT(*) as Total_Questoes_Respondidas,
            SUM(ATR_CERTO) as Total_Acertos,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as Taxa_Acerto_Pct,
            ROUND(
                (SUM(ATR_CERTO) * 1.0 / COUNT(*)) * 100, 2
            ) as Performance_Geral
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY MUN_NOME
        ORDER BY Taxa_Acerto_Pct DESC
        """
        
        df = self.get_data(query)
        
        # Adicionar classificação
        df['Posicao'] = range(1, len(df) + 1)
        df['Classificacao'] = df['Taxa_Acerto_Pct'].apply(self._classify_performance)
        
        # Salvar em Excel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_municipal_{discipline}_{year}_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Desempenho_Municipal', index=False)
            
            # Adicionar sumário estatístico
            summary = self._create_summary_stats(df)
            summary.to_excel(writer, sheet_name='Resumo_Estatistico', index=False)
        
        return str(filepath)
    
    def generate_school_report(self, year: int, discipline: str, municipality: str = None) -> str:
        """Gera relatório por escola"""
        
        where_clause = f"WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'"
        if municipality:
            where_clause += f" AND MUN_NOME = '{municipality}'"
        
        query = f"""
        SELECT 
            MUN_NOME as Municipio,
            ESC_NOME as Escola,
            ESC_INEP as Codigo_INEP,
            COUNT(DISTINCT ALU_ID) as Total_Alunos,
            COUNT(DISTINCT SER_NOME) as Series_Atendidas,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as Taxa_Acerto_Pct,
            COUNT(*) as Total_Questoes
        FROM avaliacao {where_clause}
        GROUP BY MUN_NOME, ESC_NOME, ESC_INEP
        HAVING Total_Alunos >= 5
        ORDER BY Municipio, Taxa_Acerto_Pct DESC
        """
        
        df = self.get_data(query)
        df['Classificacao'] = df['Taxa_Acerto_Pct'].apply(self._classify_performance)
        
        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = f"_{municipality}" if municipality else "_geral"
        filename = f"relatorio_escolas_{discipline}_{year}{suffix}_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        
        df.to_excel(filepath, index=False)
        return str(filepath)
    
    def generate_competency_report(self, year: int, discipline: str) -> str:
        """Gera relatório por competências"""
        
        query = f"""
        SELECT 
            MTI_CODIGO as Codigo_Competencia,
            MTI_DESCRITOR as Descricao_Competencia,
            COUNT(*) as Total_Questoes,
            COUNT(DISTINCT ALU_ID) as Alunos_Avaliados,
            SUM(ATR_CERTO) as Total_Acertos,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as Taxa_Acerto_Pct
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY MTI_CODIGO, MTI_DESCRITOR
        ORDER BY Taxa_Acerto_Pct ASC
        """
        
        df = self.get_data(query)
        
        # Classificar dificuldade
        df['Nivel_Dificuldade'] = df['Taxa_Acerto_Pct'].apply(self._classify_difficulty)
        df['Prioridade_Intervencao'] = df['Taxa_Acerto_Pct'].apply(
            lambda x: 'Alta' if x < 40 else 'Média' if x < 60 else 'Baixa'
        )
        
        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_competencias_{discipline}_{year}_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        
        df.to_excel(filepath, index=False)
        return str(filepath)
    
    def generate_comparative_report(self, years: list, discipline: str) -> str:
        """Gera relatório comparativo entre anos"""
        
        all_data = []
        for year in years:
            query = f"""
            SELECT 
                {year} as Ano,
                MUN_NOME as Municipio,
                ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as Taxa_Acerto_Pct
            FROM avaliacao 
            WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
            GROUP BY MUN_NOME
            """
            df_year = self.get_data(query)
            all_data.append(df_year)
        
        # Combinar dados
        df_combined = pd.concat(all_data, ignore_index=True)
        
        # Criar tabela pivotada
        df_pivot = df_combined.pivot(index='Municipio', columns='Ano', values='Taxa_Acerto_Pct')
        
        # Calcular evolução
        if len(years) >= 2:
            df_pivot['Evolucao'] = df_pivot[years[-1]] - df_pivot[years[0]]
            df_pivot['Tendencia'] = df_pivot['Evolucao'].apply(
                lambda x: 'Melhoria' if x > 2 else 'Estável' if x >= -2 else 'Declínio'
            )
        
        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_comparativo_{discipline}_{'-'.join(map(str, years))}_{timestamp}.xlsx"
        filepath = self.output_dir / filename
        
        df_pivot.to_excel(filepath)
        return str(filepath)
    
    def _classify_performance(self, score: float) -> str:
        """Classifica performance baseada na taxa de acerto"""
        if score >= 80:
            return "Excelente"
        elif score >= 70:
            return "Bom"
        elif score >= 60:
            return "Satisfatório"
        elif score >= 50:
            return "Regular"
        else:
            return "Insuficiente"
    
    def _classify_difficulty(self, score: float) -> str:
        """Classifica dificuldade da competência"""
        if score >= 80:
            return "Fácil"
        elif score >= 60:
            return "Médio"
        elif score >= 40:
            return "Difícil"
        else:
            return "Muito Difícil"
    
    def _create_summary_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria estatísticas resumidas"""
        stats = {
            'Métrica': [
                'Número de Municípios',
                'Taxa Média de Acerto',
                'Taxa Máxima de Acerto',
                'Taxa Mínima de Acerto',
                'Desvio Padrão',
                'Municípios com Performance Excelente (≥80%)',
                'Municípios com Performance Insuficiente (<50%)'
            ],
            'Valor': [
                len(df),
                f"{df['Taxa_Acerto_Pct'].mean():.2f}%",
                f"{df['Taxa_Acerto_Pct'].max():.2f}%",
                f"{df['Taxa_Acerto_Pct'].min():.2f}%",
                f"{df['Taxa_Acerto_Pct'].std():.2f}",
                len(df[df['Taxa_Acerto_Pct'] >= 80]),
                len(df[df['Taxa_Acerto_Pct'] < 50])
            ]
        }
        
        return pd.DataFrame(stats)
