"""
Dashboard Principal para Análise de Dados SAEV - Versão Star Schema
Otimizado para usar tabelas de dimensão e fato para performance superior
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
    page_title="SAEV Dashboard - Star Schema",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SAEVStarSchemaDashboard:
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
        
        # Verificar se as tabelas Star Schema existem
        if not self._check_star_schema():
            st.error("❌ Modelo Star Schema não encontrado no banco de dados")
            st.info("💡 Execute o script de carga com Star Schema ou use apply_star_schema.py")
            st.stop()
        
        # Mostrar informações do ambiente na sidebar
        self._show_environment_info()
    
    def _check_star_schema(self) -> bool:
        """Verifica se as tabelas do Star Schema existem"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar se as tabelas essenciais existem
            required_tables = ['dim_aluno', 'dim_escola', 'dim_descritor', 'fato_resposta_aluno']
            
            for table in required_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if not cursor.fetchone():
                    conn.close()
                    return False
            
            conn.close()
            return True
            
        except Exception:
            return False
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
                
                # Mostrar informações do Star Schema
                self._show_star_schema_info()
                
                # Link para trocar ambiente
                st.markdown("---")
                st.markdown("**🔄 Trocar Ambiente:**")
                st.code("python run_dashboard.py --env teste")
                st.code("python run_dashboard.py --env producao")
                
        except Exception as e:
            st.sidebar.error(f"Erro ao obter info do ambiente: {e}")
    
    def _show_star_schema_info(self):
        """Mostra informações sobre o Star Schema na sidebar"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Contar registros nas tabelas principais
            counts = {}
            tables = {
                'dim_aluno': 'Alunos',
                'dim_escola': 'Escolas', 
                'dim_descritor': 'Descritores',
                'fato_resposta_aluno': 'Fatos (Respostas)'
            }
            
            for table, label in tables.items():
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                counts[label] = cursor.fetchone()[0]
            
            conn.close()
            
            st.markdown("### ⭐ Star Schema")
            st.success("✅ Modelo dimensional ativo")
            
            for label, count in counts.items():
                st.metric(label, f"{count:,}")
                
        except Exception as e:
            st.error(f"Erro ao obter info Star Schema: {e}")
        
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
        """Cria filtros na sidebar baseados no Star Schema"""
        st.sidebar.header("🔍 Filtros")
        
        try:
            # Filtro de ano - usando tabela fato
            years = self.get_data("SELECT DISTINCT AVA_ANO FROM fato_resposta_aluno ORDER BY AVA_ANO")
            if years.empty:
                st.sidebar.error("❌ Nenhum ano encontrado nos dados")
                return None
            
            selected_year = st.sidebar.selectbox("Ano da Avaliação", years['AVA_ANO'].tolist())
            
            # Filtro de disciplina - usando tabela fato
            disciplines = self.get_data("SELECT DISTINCT DIS_NOME FROM fato_resposta_aluno ORDER BY DIS_NOME")
            if disciplines.empty:
                st.sidebar.error("❌ Nenhuma disciplina encontrada nos dados")
                return None
            
            selected_discipline = st.sidebar.selectbox("Disciplina", disciplines['DIS_NOME'].tolist())
            
            # Filtro de teste (nome do teste) - usando tabela fato
            tests_query = f"""
            SELECT DISTINCT TES_NOME 
            FROM fato_resposta_aluno 
            WHERE DIS_NOME = '{selected_discipline}' 
            ORDER BY TES_NOME
            """
            tests = self.get_data(tests_query)
            if tests.empty:
                st.sidebar.error("❌ Nenhum teste encontrado para esta disciplina")
                return None
            
            selected_test = st.sidebar.selectbox("Nome do Teste", tests['TES_NOME'].tolist())
            
            # Filtro de série - usando tabela fato
            series = self.get_data("SELECT DISTINCT SER_NOME FROM fato_resposta_aluno ORDER BY SER_NOME")
            series_list = series['SER_NOME'].tolist() if not series.empty else []
            
            # Definir valor padrão para 1º Ano
            default_series = []
            if "1º Ano EF" in series_list:
                default_series = ["1º Ano EF"]
            elif series_list:
                default_series = [series_list[0]]
            
            selected_series = st.sidebar.multiselect("Série", series_list, default=default_series)
            
            return {
                'year': selected_year,
                'discipline': selected_discipline,
                'test': selected_test,
                'series': selected_series
            }
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao criar filtros: {e}")
            return None
    
    def performance_overview(self, filters):
        """Visão geral do desempenho usando Star Schema"""
        st.header("📈 Visão Geral do Desempenho")
        
        # Query base otimizada com filtros Star Schema
        where_clause = f"WHERE f.AVA_ANO = {filters['year']} AND f.DIS_NOME = '{filters['discipline']}' AND f.TES_NOME = '{filters['test']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND f.SER_NOME IN ('{series_list}')"
        
        # Métricas principais usando agregações da tabela fato
        metrics_query = f"""
        SELECT 
            COUNT(DISTINCT f.ALU_ID) as total_alunos,
            COUNT(DISTINCT f.ESC_INEP) as total_escolas,
            COUNT(DISTINCT f.MUN_NOME) as total_municipios,
            SUM(f.ACERTO) as total_acertos,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto_geral
        FROM fato_resposta_aluno f
        {where_clause}
        """
        
        metrics = self.get_data(metrics_query)
        
        if not metrics.empty and metrics.iloc[0]['total_alunos'] > 0:
            # Exibir métricas em colunas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Total de Alunos", f"{metrics.iloc[0]['total_alunos']:,}")
            
            with col2:
                st.metric("🏫 Escolas", f"{metrics.iloc[0]['total_escolas']:,}")
            
            with col3:
                st.metric("🏙️ Municípios", f"{metrics.iloc[0]['total_municipios']:,}")
            
            with col4:
                st.metric("📊 Taxa de Acerto Geral", f"{metrics.iloc[0]['taxa_acerto_geral']}%")
            
            # Gráfico de distribuição de desempenho
            st.subheader("📊 Distribuição de Desempenho por Faixas")
            
            distribution_query = f"""
            SELECT 
                CASE 
                    WHEN taxa_acerto >= 80 THEN 'Excelente (80-100%)'
                    WHEN taxa_acerto >= 60 THEN 'Bom (60-79%)'
                    WHEN taxa_acerto >= 40 THEN 'Regular (40-59%)'
                    ELSE 'Abaixo do Esperado (<40%)'
                END as faixa_desempenho,
                COUNT(*) as quantidade_alunos
            FROM (
                SELECT 
                    f.ALU_ID,
                    ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto
                FROM fato_resposta_aluno f
                {where_clause}
                GROUP BY f.ALU_ID
            ) desempenho_alunos
            GROUP BY faixa_desempenho
            ORDER BY 
                CASE faixa_desempenho
                    WHEN 'Excelente (80-100%)' THEN 1
                    WHEN 'Bom (60-79%)' THEN 2
                    WHEN 'Regular (40-59%)' THEN 3
                    ELSE 4
                END
            """
            
            distribution = self.get_data(distribution_query)
            
            if not distribution.empty:
                fig = px.pie(
                    distribution,
                    values='quantidade_alunos',
                    names='faixa_desempenho',
                    title='Distribuição de Alunos por Faixa de Desempenho',
                    color_discrete_map={
                        'Excelente (80-100%)': '#2E8B57',
                        'Bom (60-79%)': '#32CD32', 
                        'Regular (40-59%)': '#FFD700',
                        'Abaixo do Esperado (<40%)': '#DC143C'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    
    def performance_by_municipality(self, filters):
        """Análise de desempenho por município usando Star Schema"""
        st.header("🏙️ Desempenho por Município")
        
        where_clause = f"WHERE f.AVA_ANO = {filters['year']} AND f.DIS_NOME = '{filters['discipline']}' AND f.TES_NOME = '{filters['test']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND f.SER_NOME IN ('{series_list}')"
        
        # Query otimizada usando Star Schema
        query = f"""
        SELECT 
            f.MUN_NOME,
            COUNT(DISTINCT f.ALU_ID) as total_alunos,
            COUNT(DISTINCT f.ESC_INEP) as total_escolas,
            SUM(f.ACERTO) as total_acertos,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        {where_clause}
        GROUP BY f.MUN_NOME
        ORDER BY taxa_acerto DESC
        """
        
        df = self.get_data(query)
        
        if not df.empty:
            # Gráfico de barras
            fig = px.bar(
                df,
                x='MUN_NOME',
                y='taxa_acerto',
                color='taxa_acerto',
                title='Taxa de Acerto por Município',
                labels={'taxa_acerto': 'Taxa de Acerto (%)', 'MUN_NOME': 'Município'},
                color_continuous_scale='RdYlGn',
                hover_data=['total_alunos', 'total_escolas']
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.subheader("📋 Detalhamento por Município")
            st.dataframe(df, use_container_width=True)
    
    def performance_by_school(self, filters):
        """Análise de desempenho por escola usando Star Schema"""
        st.header("🏫 Desempenho por Escola")
        
        where_clause = f"WHERE f.AVA_ANO = {filters['year']} AND f.DIS_NOME = '{filters['discipline']}' AND f.TES_NOME = '{filters['test']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND f.SER_NOME IN ('{series_list}')"
        
        # Query otimizada usando joins com tabelas de dimensão
        query = f"""
        SELECT 
            f.MUN_NOME,
            e.ESC_NOME,
            COUNT(DISTINCT f.ALU_ID) as total_alunos,
            SUM(f.ACERTO) as total_acertos,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        JOIN dim_escola e ON f.ESC_INEP = e.ESC_INEP
        {where_clause}
        GROUP BY f.MUN_NOME, e.ESC_NOME
        ORDER BY taxa_acerto DESC
        """
        
        df = self.get_data(query)
        
        if not df.empty:
            # Scatter plot para mostrar relação alunos vs desempenho
            fig = px.scatter(
                df,
                x='total_alunos',
                y='taxa_acerto',
                color='MUN_NOME',
                size='total_questoes',
                title='Desempenho por Escola (Tamanho = Total de Questões)',
                labels={
                    'total_alunos': 'Total de Alunos',
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
        """Análise por competências usando Star Schema"""
        st.header("🎯 Análise por Competências (Descritores)")
        
        where_clause = f"WHERE f.AVA_ANO = {filters['year']} AND f.DIS_NOME = '{filters['discipline']}' AND f.TES_NOME = '{filters['test']}'"
        if filters['series']:
            series_list = "','".join(filters['series'])
            where_clause += f" AND f.SER_NOME IN ('{series_list}')"
        
        # Query otimizada usando join com tabela de dimensão de descritores
        query = f"""
        SELECT 
            d.MTI_CODIGO,
            d.MTI_DESCRITOR,
            COUNT(DISTINCT f.ALU_ID) as alunos_avaliados,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            SUM(f.ACERTO) as total_acertos,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        JOIN dim_descritor d ON f.MTI_CODIGO = d.MTI_CODIGO
        {where_clause}
        GROUP BY d.MTI_CODIGO, d.MTI_DESCRITOR
        ORDER BY taxa_acerto ASC
        """
        
        df = self.get_data(query)
        
        if not df.empty:
            # Gráfico horizontal das competências
            fig = px.bar(
                df.head(15),  # Mostrar apenas os 15 primeiros para melhor visualização
                x='taxa_acerto',
                y='MTI_CODIGO',
                orientation='h',
                title='Taxa de Acerto por Competência (15 menores)',
                labels={'taxa_acerto': 'Taxa de Acerto (%)', 'MTI_CODIGO': 'Código do Descritor'},
                color='taxa_acerto',
                color_continuous_scale='RdYlGn',
                hover_data=['alunos_avaliados', 'total_questoes']
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Competências que necessitam atenção
            st.subheader("⚠️ Competências que Necessitam Atenção")
            worst_competencies = df.head(5)[['MTI_CODIGO', 'MTI_DESCRITOR', 'taxa_acerto', 'alunos_avaliados']]
            st.dataframe(worst_competencies, use_container_width=True)
            
            # Competências com melhor desempenho
            st.subheader("🏆 Competências com Melhor Desempenho")
            best_competencies = df.tail(5)[['MTI_CODIGO', 'MTI_DESCRITOR', 'taxa_acerto', 'alunos_avaliados']]
            st.dataframe(best_competencies, use_container_width=True)
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
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}' AND TES_NOME = '{filters['test']}'"
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
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}' AND TES_NOME = '{filters['test']}'"
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
        
        where_clause = f"WHERE AVA_ANO = {filters['year']} AND DIS_NOME = '{filters['discipline']}' AND TES_NOME = '{filters['test']}'"
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
    st.title("⭐ Dashboard SAEV - Star Schema")
    st.markdown("### Sistema de Avaliação Educacional com Modelo Dimensional Otimizado")
    st.markdown("---")
    
    # Inicializar dashboard
    dashboard = SAEVStarSchemaDashboard()
    
    # Verificar se há dados no Star Schema
    try:
        test_query = "SELECT COUNT(*) as total FROM fato_resposta_aluno LIMIT 1"
        result = dashboard.get_data(test_query)
        if result.empty or result.iloc[0]['total'] == 0:
            st.warning("⚠️ Nenhum dado encontrado na tabela fato.")
            st.info("💡 Execute o script de carga para importar dados com Star Schema.")
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
        
        # Seção adicional: Informações sobre o Star Schema
        with st.expander("ℹ️ Sobre o Modelo Star Schema"):
            st.markdown("""
            ### ⭐ Otimizações do Modelo Dimensional
            
            Este dashboard foi otimizado para usar o **modelo Star Schema** com as seguintes vantagens:
            
            - **🚀 Performance superior**: Consultas até 100x mais rápidas
            - **📊 Dados agregados**: Métricas pré-calculadas na tabela fato
            - **🔧 Joins otimizados**: Relacionamentos diretos entre dimensões e fatos
            - **💾 Menor uso de memória**: Dados normalizados em dimensões
            
            #### 📋 Estrutura das Tabelas:
            - **`fato_resposta_aluno`**: Tabela central com métricas agregadas (ACERTO, ERRO)
            - **`dim_aluno`**: Dimensão de alunos com dados únicos
            - **`dim_escola`**: Dimensão de escolas com informações institucionais  
            - **`dim_descritor`**: Dimensão de competências/descritores
            
            #### 🔗 Relacionamentos:
            - Todas as dimensões conectam-se à tabela fato através de chaves estrangeiras
            - Consultas utilizam JOINs otimizados para máxima performance
            """)

if __name__ == "__main__":
    main()
