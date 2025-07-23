"""
Sistema de Análise Estatística Avançada para SAEV
"""
import pandas as pd
import numpy as np
import sqlite3
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Adicionar o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import config

class SAEVAnalytics:
    """Classe para análises estatísticas avançadas"""
    
    def __init__(self, db_path: str = None):
        # Se não especificar db_path, usa detecção automática
        if db_path is None:
            self.db_path = config.get_database_path()
        else:
            self.db_path = db_path
            
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
    
    def equity_analysis(self, year: int, discipline: str):
        """Análise de equidade educacional"""
        
        query = f"""
        SELECT 
            MUN_NOME,
            ESC_INEP,
            AVG(CAST(ATR_CERTO AS FLOAT)) * 100 as taxa_acerto
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY MUN_NOME, ESC_INEP
        HAVING COUNT(DISTINCT ALU_ID) >= 10
        """
        
        df = self.get_data(query)
        
        # Calcular índice de equidade (coeficiente de variação)
        equity_stats = df.groupby('MUN_NOME').agg({
            'taxa_acerto': ['mean', 'std', 'min', 'max', 'count']
        }).round(2)
        
        equity_stats.columns = ['media', 'desvio_padrao', 'minimo', 'maximo', 'num_escolas']
        equity_stats['coef_variacao'] = (equity_stats['desvio_padrao'] / equity_stats['media']) * 100
        equity_stats['amplitude'] = equity_stats['maximo'] - equity_stats['minimo']
        
        # Classificar equidade
        equity_stats['nivel_equidade'] = equity_stats['coef_variacao'].apply(
            lambda x: 'Alta Equidade' if x < 10 else 
                     'Média Equidade' if x < 20 else 'Baixa Equidade'
        )
        
        return equity_stats.reset_index()
    
    def trend_analysis(self, municipality: str, discipline: str, min_year: int = None):
        """Análise de tendências temporais"""
        
        where_clause = f"WHERE MUN_NOME = '{municipality}' AND DIS_NOME = '{discipline}'"
        if min_year:
            where_clause += f" AND AVA_ANO >= {min_year}"
        
        query = f"""
        SELECT 
            AVA_ANO,
            AVG(CAST(ATR_CERTO AS FLOAT)) * 100 as taxa_acerto,
            COUNT(DISTINCT ALU_ID) as total_alunos
        FROM avaliacao {where_clause}
        GROUP BY AVA_ANO
        ORDER BY AVA_ANO
        """
        
        df = self.get_data(query)
        
        if len(df) < 3:
            return {"error": "Dados insuficientes para análise de tendência"}
        
        # Calcular tendência linear
        x = df['AVA_ANO'].values
        y = df['taxa_acerto'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Interpretação da tendência
        if p_value < 0.05:  # Significância estatística
            if slope > 0.5:
                trend = "Tendência de melhoria significativa"
            elif slope < -0.5:
                trend = "Tendência de declínio significativa"
            else:
                trend = "Tendência estável"
        else:
            trend = "Sem tendência estatisticamente significativa"
        
        return {
            'data': df,
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'trend_interpretation': trend,
            'annual_change': slope,  # Mudança anual em pontos percentuais
        }
    
    def school_clustering(self, year: int, discipline: str):
        """Clustering de escolas por características de desempenho"""
        
        query = f"""
        SELECT 
            ESC_INEP,
            ESC_NOME,
            MUN_NOME,
            COUNT(DISTINCT ALU_ID) as total_alunos,
            AVG(CAST(ATR_CERTO AS FLOAT)) * 100 as taxa_acerto,
            COUNT(DISTINCT MTI_CODIGO) as competencias_avaliadas,
            MIN(CAST(ATR_CERTO AS FLOAT)) * 100 as pior_competencia,
            MAX(CAST(ATR_CERTO AS FLOAT)) * 100 as melhor_competencia
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY ESC_INEP, ESC_NOME, MUN_NOME
        HAVING total_alunos >= 15
        """
        
        df = self.get_data(query)
        
        if len(df) < 10:
            return {"error": "Dados insuficientes para clustering"}
        
        # Preparar dados para clustering
        features = ['total_alunos', 'taxa_acerto', 'competencias_avaliadas']
        X = df[features].values
        
        # Normalizar dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar K-means
        n_clusters = min(5, len(df) // 3)  # Máximo 5 clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Caracterizar clusters
        cluster_summary = df.groupby('cluster').agg({
            'total_alunos': ['mean', 'std'],
            'taxa_acerto': ['mean', 'std'],
            'competencias_avaliadas': 'mean'
        }).round(2)
        
        # Nomear clusters baseado em características
        cluster_names = {}
        for cluster_id in range(n_clusters):
            cluster_data = df[df['cluster'] == cluster_id]
            avg_performance = cluster_data['taxa_acerto'].mean()
            avg_size = cluster_data['total_alunos'].mean()
            
            if avg_performance >= 75:
                performance_level = "Alto Desempenho"
            elif avg_performance >= 60:
                performance_level = "Médio Desempenho"
            else:
                performance_level = "Baixo Desempenho"
            
            size_level = "Grande" if avg_size >= 100 else "Médio" if avg_size >= 50 else "Pequeno"
            
            cluster_names[cluster_id] = f"{performance_level} - Porte {size_level}"
        
        df['cluster_nome'] = df['cluster'].map(cluster_names)
        
        return {
            'data': df,
            'cluster_summary': cluster_summary,
            'cluster_names': cluster_names,
            'n_clusters': n_clusters
        }
    
    def competency_correlation_analysis(self, year: int, discipline: str):
        """Análise de correlação entre competências"""
        
        # Buscar dados por competência e aluno
        query = f"""
        SELECT 
            ALU_ID,
            MTI_CODIGO,
            AVG(CAST(ATR_CERTO AS FLOAT)) as desempenho
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY ALU_ID, MTI_CODIGO
        """
        
        df = self.get_data(query)
        
        # Criar matriz de competências x alunos
        pivot_df = df.pivot(index='ALU_ID', columns='MTI_CODIGO', values='desempenho')
        
        # Calcular matriz de correlação
        correlation_matrix = pivot_df.corr()
        
        # Encontrar competências mais correlacionadas
        correlation_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                comp1 = correlation_matrix.columns[i]
                comp2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if not np.isnan(corr_value):
                    correlation_pairs.append({
                        'competencia_1': comp1,
                        'competencia_2': comp2,
                        'correlacao': corr_value
                    })
        
        correlation_df = pd.DataFrame(correlation_pairs)
        correlation_df = correlation_df.sort_values('correlacao', ascending=False)
        
        return {
            'correlation_matrix': correlation_matrix,
            'top_correlations': correlation_df.head(10),
            'weak_correlations': correlation_df.tail(10)
        }
    
    def performance_gap_analysis(self, year: int, discipline: str):
        """Análise de gaps de desempenho"""
        
        query = f"""
        SELECT 
            MUN_NOME,
            SER_NOME,
            AVG(CAST(ATR_CERTO AS FLOAT)) * 100 as taxa_acerto,
            COUNT(DISTINCT ALU_ID) as total_alunos
        FROM avaliacao 
        WHERE AVA_ANO = {year} AND DIS_NOME = '{discipline}'
        GROUP BY MUN_NOME, SER_NOME
        HAVING total_alunos >= 10
        """
        
        df = self.get_data(query)
        
        # Calcular gaps entre séries dentro do mesmo município
        gaps = []
        for municipio in df['MUN_NOME'].unique():
            mun_data = df[df['MUN_NOME'] == municipio].sort_values('SER_NOME')
            
            for i in range(len(mun_data) - 1):
                serie_atual = mun_data.iloc[i]
                serie_seguinte = mun_data.iloc[i + 1]
                
                gap = serie_seguinte['taxa_acerto'] - serie_atual['taxa_acerto']
                
                gaps.append({
                    'municipio': municipio,
                    'serie_origem': serie_atual['SER_NOME'],
                    'serie_destino': serie_seguinte['SER_NOME'],
                    'taxa_origem': serie_atual['taxa_acerto'],
                    'taxa_destino': serie_seguinte['taxa_acerto'],
                    'gap': gap,
                    'gap_tipo': 'Progressão' if gap > 0 else 'Regressão'
                })
        
        gaps_df = pd.DataFrame(gaps)
        
        # Identificar maiores gaps
        maiores_gaps = gaps_df.nlargest(10, 'gap')
        menores_gaps = gaps_df.nsmallest(10, 'gap')
        
        return {
            'all_gaps': gaps_df,
            'biggest_improvements': maiores_gaps,
            'biggest_regressions': menores_gaps,
            'average_gap': gaps_df['gap'].mean()
        }
