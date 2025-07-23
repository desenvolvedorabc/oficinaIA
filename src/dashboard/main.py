"""
Dashboard Principal para Análise de Dados SAEV
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from pathlib import Path

# Adicionar o diretório raiz ao path para importações
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import config

# Configuração da página
st.set_page_config(
    page_title="SAEV Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SAEVDashboard:
    def __init__(self):
        # Obter caminho do banco de dados das variáveis de ambiente ou configuração
        self.db_path = os.getenv('SAEV_DATABASE_PATH')
        self.environment = os.getenv('SAEV_ENVIRONMENT', 'auto')
        
        if not self.db_path:
            # Fallback para detecção automática
            try:
                self.environment = config.detect_environment()
                self.db_path = config.get_database_path(self.environment)
            except Exception as e:
                st.error(f"❌ Erro ao configurar banco de dados: {e}")
                st.stop()
        
        # Verificar se o banco existe
        if not Path(self.db_path).exists():
            st.error(f"❌ Banco de dados não encontrado: {self.db_path}")
            st.info("💡 Execute o script de carga primeiro ou verifique o ambiente.")
            st.stop()
        
        # Mostrar informações do ambiente na sidebar
        self._show_environment_info()
    
    def _show_environment_info(self):
        """Mostra informações do ambiente atual na sidebar"""
        try:
            env_info = config.get_environment_info(self.environment)
            
            with st.sidebar:
                st.markdown("### ℹ️ Ambiente Atual")
                
                # Badge do ambiente
                if self.environment == 'teste':
                    st.markdown("🧪 **TESTE** (Dados Ofuscados)")
                    st.warning("⚠️ Dados com MD5 para proteção")
                else:
                    st.markdown("🔴 **PRODUÇÃO** (Dados Reais)")
                    st.error("🔒 Dados sensíveis - Use com cuidado")
                
                # Informações do banco
                if env_info.get('file_size_mb'):
                    st.metric("💾 Tamanho do Banco", f"{env_info['file_size_mb']} MB")
                
                # Link para trocar ambiente
                st.markdown("---")
                st.markdown("**🔄 Trocar Ambiente:**")
                st.code("python run_dashboard.py --env teste")
                st.code("python run_dashboard.py --env producao")
                
        except Exception as e:
            st.sidebar.error(f"Erro ao obter info do ambiente: {e}")
        
    def get_data(self, query: str) -> pd.DataFrame:
        """Executa query e retorna DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ Erro ao executar consulta: {e}")
            return pd.DataFrame()
    
    def create_filters(self):
        """Cria filtros na sidebar"""
        st.sidebar.header("🔍 Filtros")
        
        try:
            # Filtro de ano
            years = self.get_data("SELECT DISTINCT AVA_ANO FROM avaliacao ORDER BY AVA_ANO")
            if years.empty:
                st.sidebar.error("❌ Nenhum ano encontrado nos dados")
                return None
            
            selected_year = st.sidebar.selectbox("Ano da Avaliação", years['AVA_ANO'].tolist())
            
            # Filtro de disciplina
            disciplines = self.get_data("SELECT DISTINCT DIS_NOME FROM avaliacao ORDER BY DIS_NOME")
            if disciplines.empty:
                st.sidebar.error("❌ Nenhuma disciplina encontrada nos dados")
                return None
            
            selected_discipline = st.sidebar.selectbox("Disciplina", disciplines['DIS_NOME'].tolist())
            
            # Filtro de série
            series = self.get_data("SELECT DISTINCT SER_NOME FROM avaliacao ORDER BY SER_NUMBER")
            selected_series = st.sidebar.multiselect("Série", series['SER_NOME'].tolist() if not series.empty else [])
            
            return {
                'year': selected_year,
                'discipline': selected_discipline,
                'series': selected_series
            }
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao criar filtros: {e}")
            return None
    
    def performance_overview(self, filters):
        """Visão geral do desempenho"""
        st.header("📈 Visão Geral do Desempenho")
        
        # Query base com filtros
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND SER_NOME IN ('{series_list}')"
        
        # Métricas gerais
        metrics_query = f"""
        SELECT 
            COUNT(DISTINCT ALU_ID) as total_alunos,
            COUNT(DISTINCT ESC_INEP) as total_escolas,
            COUNT(DISTINCT MUN_NOME) as total_municipios,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as taxa_acerto
        FROM avaliacao {where_clause}
        """
        metrics = self.get_data(metrics_query).iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total de Alunos", f"{metrics['total_alunos']:,}")
        with col2:
            st.metric("🏫 Total de Escolas", f"{metrics['total_escolas']:,}")
        with col3:
            st.metric("🏘️ Total de Municípios", f"{metrics['total_municipios']:,}")
        with col4:
            st.metric("✅ Taxa de Acerto Geral", f"{metrics['taxa_acerto']}%")
    
    def performance_by_municipality(self, filters):
        """Desempenho por município"""
        st.header("🏘️ Desempenho por Município")
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND SER_NOME IN ('{series_list}')"
        
        query = f"""
        SELECT 
            MUN_NOME,
            COUNT(DISTINCT ALU_ID) as total_alunos,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as taxa_acerto
        FROM avaliacao {where_clause}
        GROUP BY MUN_NOME
        ORDER BY taxa_acerto DESC
        """
        
        df = self.get_data(query)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras
            fig = px.bar(
                df, 
                x='MUN_NOME', 
                y='taxa_acerto',
                title='Taxa de Acerto por Município',
                labels={'taxa_acerto': 'Taxa de Acerto (%)', 'MUN_NOME': 'Município'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tabela com dados
            st.subheader("📊 Dados Detalhados")
            st.dataframe(df, use_container_width=True)
    
    def performance_by_school(self, filters):
        """Desempenho por escola"""
        st.header("🏫 Desempenho por Escola")
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND SER_NOME IN ('{series_list}')"
        
        query = f"""
        SELECT 
            MUN_NOME,
            ESC_NOME,
            COUNT(DISTINCT ALU_ID) as total_alunos,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as taxa_acerto
        FROM avaliacao {where_clause}
        GROUP BY MUN_NOME, ESC_NOME
        HAVING total_alunos >= 10
        ORDER BY taxa_acerto DESC
        """
        
        df = self.get_data(query)
        
        # Scatter plot
        fig = px.scatter(
            df, 
            x='total_alunos', 
            y='taxa_acerto',
            color='MUN_NOME',
            title='Taxa de Acerto vs Número de Alunos por Escola',
            labels={
                'total_alunos': 'Número de Alunos',
                'taxa_acerto': 'Taxa de Acerto (%)',
                'MUN_NOME': 'Município'
            },
            hover_data=['ESC_NOME']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 10 escolas
        st.subheader("🏆 Top 10 Escolas por Taxa de Acerto")
        top_schools = df.head(10)[['MUN_NOME', 'ESC_NOME', 'total_alunos', 'taxa_acerto']]
        st.dataframe(top_schools, use_container_width=True)
    
    def competency_analysis(self, filters):
        """Análise por competências (descritores)"""
        st.header("🎯 Análise por Competências")
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND SER_NOME IN ('{series_list}')"
        
        query = f"""
        SELECT 
            MTI_CODIGO,
            MTI_DESCRITOR,
            COUNT(*) as total_questoes,
            ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as taxa_acerto
        FROM avaliacao {where_clause}
        GROUP BY MTI_CODIGO, MTI_DESCRITOR
        ORDER BY taxa_acerto ASC
        """
        
        df = self.get_data(query)
        
        # Gráfico horizontal das competências
        fig = px.bar(
            df, 
            x='taxa_acerto', 
            y='MTI_CODIGO',
            orientation='h',
            title='Taxa de Acerto por Competência (Descritor)',
            labels={'taxa_acerto': 'Taxa de Acerto (%)', 'MTI_CODIGO': 'Código do Descritor'},
            color='taxa_acerto',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Competências com menor desempenho
        st.subheader("⚠️ Competências que Necessitam Atenção")
        worst_competencies = df.head(5)[['MTI_CODIGO', 'MTI_DESCRITOR', 'taxa_acerto']]
        st.dataframe(worst_competencies, use_container_width=True)

def main():
    st.title("📊 Dashboard SAEV - Sistema de Avaliação Educacional")
    st.markdown("---")
    
    # Inicializar dashboard
    dashboard = SAEVDashboard()
    
    # Verificar se há dados no banco
    try:
        test_query = "SELECT COUNT(*) as total FROM avaliacao LIMIT 1"
        result = dashboard.get_data(test_query)
        if result.empty or result.iloc[0]['total'] == 0:
            st.warning("⚠️ Nenhum dado encontrado no banco de dados.")
            st.info("💡 Execute o script de carga para importar dados.")
            return
    except Exception as e:
        st.error(f"❌ Erro ao verificar dados: {e}")
        return
    
    # Criar filtros
    filters = dashboard.create_filters()
    
    # Exibir seções apenas se os filtros foram criados com sucesso
    if filters:
        dashboard.performance_overview(filters)
        st.markdown("---")
        
        dashboard.performance_by_municipality(filters)
        st.markdown("---")
        
        dashboard.performance_by_school(filters)
        st.markdown("---")
        
        dashboard.competency_analysis(filters)

if __name__ == "__main__":
    main()
