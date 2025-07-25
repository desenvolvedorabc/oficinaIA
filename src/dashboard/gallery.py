"""
GALERIA DE PAINÉIS SAEV - Sistema de Análise Educacional
=========================================================

Galeria principal que contém múltiplos painéis especializados para diferentes
tipos de análises educacionais usando o modelo Star Schema.

PAINÉIS DISPONÍVEIS:
1. 🎯 Análise Detalhada por Filtros - Análise granular com múltiplos filtros
2. 📊 Dashboard Geral (em desenvolvimento)
3. 🏫 Análise por Escola (em desenvolvimento)
4. 🏙️ Análise por Município (em desenvolvimento)
5. 📈 Análise Temporal (em desenvolvimento)

AUTOR: SAEV Dashboard Project
DATA: 2025
VERSÃO: 1.0
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Adicionar o diretório raiz ao path para importações
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import config

# Configuração da página
st.set_page_config(
    page_title="Galeria SAEV - Painéis de Análise",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SAEVGalleryBase:
    """Classe base para todos os painéis da galeria"""
    
    def __init__(self):
        # Configuração do banco de dados
        self.db_path = os.getenv('SAEV_DATABASE_PATH')
        self.environment = os.getenv('SAEV_ENVIRONMENT', 'auto')
        
        if not self.db_path:
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
    
    def _check_star_schema(self) -> bool:
        """Verifica se as tabelas do Star Schema existem (compatível com DuckDB e SQLite)"""
        try:
            required_tables = ['dim_aluno', 'dim_escola', 'dim_descritor', 'fato_resposta_aluno']
            
            # Detectar se é DuckDB ou SQLite
            db_type = os.getenv('SAEV_DB_TYPE', 'sqlite')
            
            if db_type == 'duckdb' and 'duckdb' in self.db_path:
                # Verificação para DuckDB
                try:
                    import duckdb
                    conn = duckdb.connect(self.db_path)
                    
                    for table in required_tables:
                        result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchall()
                        if not result:
                            conn.close()
                            return False
                    
                    conn.close()
                    return True
                    
                except ImportError:
                    # Fallback para SQLite se DuckDB não disponível
                    pass
            
            # Verificação para SQLite (padrão)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for table in required_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if not cursor.fetchone():
                    conn.close()
                    return False
            
            conn.close()
            return True
            
        except Exception:
            return False
    
    def get_data(self, query: str) -> pd.DataFrame:
        """Executa query e retorna DataFrame (otimizado para DuckDB)"""
        try:
            # Detectar se é DuckDB ou SQLite
            db_type = os.getenv('SAEV_DB_TYPE', 'sqlite')
            
            if db_type == 'duckdb' and 'duckdb' in self.db_path:
                # Usar DuckDB para performance superior
                try:
                    import duckdb
                    conn = duckdb.connect(self.db_path)
                    df = conn.execute(query).fetchdf()
                    conn.close()
                    return df
                except ImportError:
                    # Fallback para SQLite se DuckDB não disponível
                    pass
            
            # SQLite padrão
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
            
        except Exception as e:
            st.error(f"❌ Erro ao executar consulta: {e}")
            return pd.DataFrame()
    
    def show_environment_info(self):
        """Mostra informações do ambiente na sidebar"""
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
                
                # Informação do tipo de banco
                db_type = os.getenv('SAEV_DB_TYPE', 'sqlite')
                if 'duckdb' in self.db_path or db_type == 'duckdb':
                    st.success("🦆 **DuckDB** - Performance Superior")
                    st.info("⚡ Consultas 10-100x mais rápidas")
                else:
                    st.info("📊 **SQLite** - Banco Padrão")
                
                # Tamanho do banco
                if env_info.get('file_size_mb'):
                    st.metric("💾 Tamanho do Banco", f"{env_info['file_size_mb']} MB")
                elif Path(self.db_path).exists():
                    size_mb = Path(self.db_path).stat().st_size / (1024 * 1024)
                    st.metric("💾 Tamanho do Banco", f"{size_mb:.2f} MB")
                
        except Exception as e:
            st.sidebar.error(f"Erro ao obter info do ambiente: {e}")


class DetailedAnalysisPanel(SAEVGalleryBase):
    """
    🎯 PAINEL 1: ANÁLISE DETALHADA POR FILTROS
    
    Painel especializado para análise granular com múltiplos filtros:
    - Estado (UF)
    - Município 
    - Escola
    - Ano de Avaliação
    - Disciplina
    - Teste
    - Série
    
    Análises fornecidas:
    - Taxa de acerto geral e por aluno
    - Distribuição de desempenho
    - Ranking de alunos
    - Análise por competências (descritores)
    """
    
    def __init__(self):
        super().__init__()
        self.panel_title = "🎯 Análise Detalhada por Filtros"
        
    def create_advanced_filters(self) -> Optional[Dict[str, Any]]:
        """Cria filtros avançados com múltiplas seleções"""
        st.sidebar.header("🔍 Filtros Avançados")
        st.sidebar.markdown("*Utilize múltiplas seleções para análises granulares*")
        
        try:
            # 1. Filtro de Estado (UF)
            states = self.get_data("SELECT DISTINCT MUN_UF FROM fato_resposta_aluno ORDER BY MUN_UF")
            if states.empty:
                st.sidebar.error("❌ Nenhum estado encontrado")
                return None
            
            selected_states = st.sidebar.multiselect(
                "🗺️ Estado (UF)",
                states['MUN_UF'].tolist(),
                default=[states['MUN_UF'].iloc[0]] if not states.empty else []
            )
            
            if not selected_states:
                st.sidebar.warning("⚠️ Selecione pelo menos um estado")
                return None
            
            # 2. Filtro de Município (baseado nos estados selecionados)
            states_filter = "','".join(selected_states)
            municipalities_query = f"""
            SELECT DISTINCT MUN_NOME 
            FROM fato_resposta_aluno 
            WHERE MUN_UF IN ('{states_filter}')
            ORDER BY MUN_NOME
            """
            municipalities = self.get_data(municipalities_query)
            
            selected_municipalities = st.sidebar.multiselect(
                "🏙️ Município",
                municipalities['MUN_NOME'].tolist(),
                default=municipalities['MUN_NOME'].tolist()[:3] if len(municipalities) >= 3 else municipalities['MUN_NOME'].tolist()
            )
            
            if not selected_municipalities:
                st.sidebar.warning("⚠️ Selecione pelo menos um município")
                return None
            
            # 3. Filtro de Escola (baseado nos municípios selecionados) 
            municipalities_filter = "','".join(selected_municipalities)
            schools_query = f"""
            SELECT DISTINCT f.ESC_INEP, e.ESC_NOME
            FROM fato_resposta_aluno f
            JOIN dim_escola e ON f.ESC_INEP = e.ESC_INEP
            WHERE f.MUN_NOME IN ('{municipalities_filter}')
            ORDER BY e.ESC_NOME
            """
            schools = self.get_data(schools_query)
            
            # Criar lista de opções com nome da escola para melhor UX
            school_options = [f"{row['ESC_NOME']} ({row['ESC_INEP']})" for _, row in schools.iterrows()]
            selected_school_options = st.sidebar.multiselect(
                "🏫 Escola",
                school_options,
                default=school_options[:5] if len(school_options) >= 5 else school_options
            )
            
            # Extrair códigos INEP das seleções
            selected_schools = []
            for option in selected_school_options:
                inep_code = option.split('(')[-1].replace(')', '')
                selected_schools.append(inep_code)
            
            if not selected_schools:
                st.sidebar.warning("⚠️ Selecione pelo menos uma escola")
                return None
            
            # 4. Filtro de Ano
            years = self.get_data("SELECT DISTINCT AVA_ANO FROM fato_resposta_aluno ORDER BY AVA_ANO DESC")
            selected_years = st.sidebar.multiselect(
                "📅 Ano da Avaliação",
                years['AVA_ANO'].tolist(),
                default=[years['AVA_ANO'].iloc[0]] if not years.empty else []
            )
            
            # 5. Filtro de Disciplina
            disciplines = self.get_data("SELECT DISTINCT DIS_NOME FROM fato_resposta_aluno ORDER BY DIS_NOME")
            selected_disciplines = st.sidebar.multiselect(
                "📚 Disciplina",
                disciplines['DIS_NOME'].tolist(),
                default=[disciplines['DIS_NOME'].iloc[0]] if not disciplines.empty else []
            )
            
            # 6. Filtro de Teste (baseado nas disciplinas selecionadas)
            if selected_disciplines:
                disciplines_filter = "','".join(selected_disciplines)
                tests_query = f"""
                SELECT DISTINCT TES_NOME 
                FROM fato_resposta_aluno 
                WHERE DIS_NOME IN ('{disciplines_filter}')
                ORDER BY TES_NOME
                """
                tests = self.get_data(tests_query)
                
                selected_tests = st.sidebar.multiselect(
                    "📝 Teste",
                    tests['TES_NOME'].tolist(),
                    default=tests['TES_NOME'].tolist()[:2] if len(tests) >= 2 else tests['TES_NOME'].tolist()
                )
            else:
                selected_tests = []
            
            # 7. Filtro de Série
            series = self.get_data("SELECT DISTINCT SER_NOME FROM fato_resposta_aluno ORDER BY SER_NOME")
            selected_series = st.sidebar.multiselect(
                "🎓 Série",
                series['SER_NOME'].tolist(),
                default=series['SER_NOME'].tolist()[:2] if len(series) >= 2 else series['SER_NOME'].tolist()
            )
            
            # Validar se todos os filtros obrigatórios foram selecionados
            if not all([selected_states, selected_municipalities, selected_schools, 
                       selected_years, selected_disciplines, selected_tests, selected_series]):
                st.sidebar.error("❌ Preencha todos os filtros obrigatórios")
                return None
            
            return {
                'states': selected_states,
                'municipalities': selected_municipalities, 
                'schools': selected_schools,
                'years': selected_years,
                'disciplines': selected_disciplines,
                'tests': selected_tests,
                'series': selected_series
            }
            
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao criar filtros: {e}")
            return None
    
    def build_where_clause(self, filters: Dict[str, Any]) -> str:
        """Constrói cláusula WHERE baseada nos filtros selecionados"""
        conditions = []
        
        if filters['states']:
            states_list = "','".join(filters['states'])
            conditions.append(f"f.MUN_UF IN ('{states_list}')")
        
        if filters['municipalities']:
            municipalities_list = "','".join(filters['municipalities'])
            conditions.append(f"f.MUN_NOME IN ('{municipalities_list}')")
        
        if filters['schools']:
            schools_list = "','".join(filters['schools'])
            conditions.append(f"f.ESC_INEP IN ('{schools_list}')")
        
        if filters['years']:
            years_list = ','.join(map(str, filters['years']))
            conditions.append(f"f.AVA_ANO IN ({years_list})")
        
        if filters['disciplines']:
            disciplines_list = "','".join(filters['disciplines'])
            conditions.append(f"f.DIS_NOME IN ('{disciplines_list}')")
        
        if filters['tests']:
            tests_list = "','".join(filters['tests'])
            conditions.append(f"f.TES_NOME IN ('{tests_list}')")
        
        if filters['series']:
            series_list = "','".join(filters['series'])
            conditions.append(f"f.SER_NOME IN ('{series_list}')")
        
        return "WHERE " + " AND ".join(conditions) if conditions else ""
    
    def show_summary_metrics(self, filters: Dict[str, Any]):
        """Exibe métricas resumo dos filtros aplicados"""
        st.header("📊 Resumo da Seleção")
        
        where_clause = self.build_where_clause(filters)
        
        # Query para métricas gerais
        summary_query = f"""
        SELECT 
            COUNT(DISTINCT f.ALU_ID) as total_alunos,
            COUNT(DISTINCT f.ESC_INEP) as total_escolas,
            COUNT(DISTINCT f.MUN_NOME) as total_municipios,
            COUNT(DISTINCT f.MUN_UF) as total_estados,
            COUNT(DISTINCT f.AVA_ANO) as total_anos,
            COUNT(DISTINCT f.DIS_NOME) as total_disciplinas,
            COUNT(DISTINCT f.TES_NOME) as total_testes,
            SUM(f.ACERTO) as total_acertos,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto_geral
        FROM fato_resposta_aluno f
        {where_clause}
        """
        
        summary = self.get_data(summary_query)
        
        if not summary.empty and summary.iloc[0]['total_alunos'] > 0:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("👥 Alunos", f"{summary.iloc[0]['total_alunos']:,}")
                st.metric("🏫 Escolas", f"{summary.iloc[0]['total_escolas']:,}")
            
            with col2:
                st.metric("🏙️ Municípios", f"{summary.iloc[0]['total_municipios']:,}")
                st.metric("🗺️ Estados", f"{summary.iloc[0]['total_estados']:,}")
            
            with col3:
                st.metric("📅 Anos", f"{summary.iloc[0]['total_anos']:,}")
                st.metric("📚 Disciplinas", f"{summary.iloc[0]['total_disciplinas']:,}")
            
            with col4:
                st.metric("📝 Testes", f"{summary.iloc[0]['total_testes']:,}")
                st.metric("❓ Questões", f"{summary.iloc[0]['total_questoes']:,}")
            
            with col5:
                st.metric("✅ Acertos", f"{summary.iloc[0]['total_acertos']:,}")
                st.metric("📈 Taxa Geral", f"{summary.iloc[0]['taxa_acerto_geral']}%")
        else:
            st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados")
    
    def student_performance_analysis(self, filters: Dict[str, Any]):
        """Análise detalhada do desempenho dos alunos"""
        st.header("🎯 Análise de Desempenho dos Alunos")
        
        where_clause = self.build_where_clause(filters)
        
        # Query para desempenho individual dos alunos
        students_query = f"""
        SELECT 
            f.ALU_ID,
            a.ALU_NOME,
            f.MUN_NOME,
            e.ESC_NOME,
            f.SER_NOME,
            SUM(f.ACERTO) as total_acertos,
            SUM(f.ACERTO + f.ERRO) as total_questoes,
            ROUND((SUM(f.ACERTO) * 100.0) / SUM(f.ACERTO + f.ERRO), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        JOIN dim_aluno a ON f.ALU_ID = a.ALU_ID
        JOIN dim_escola e ON f.ESC_INEP = e.ESC_INEP
        {where_clause}
        GROUP BY f.ALU_ID, a.ALU_NOME, f.MUN_NOME, e.ESC_NOME, f.SER_NOME
        ORDER BY taxa_acerto DESC
        """
        
        students_df = self.get_data(students_query)
        
        if not students_df.empty:
            # Distribuição de desempenho
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Distribuição de Taxa de Acerto")
                fig_hist = px.histogram(
                    students_df,
                    x='taxa_acerto',
                    nbins=20,
                    title='Distribuição de Taxa de Acerto dos Alunos',
                    labels={'taxa_acerto': 'Taxa de Acerto (%)', 'count': 'Quantidade de Alunos'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Faixas de Desempenho")
                
                # Criar faixas de desempenho
                students_df['faixa_desempenho'] = students_df['taxa_acerto'].apply(
                    lambda x: 'Excelente (80-100%)' if x >= 80
                    else 'Bom (60-79%)' if x >= 60
                    else 'Regular (40-59%)' if x >= 40
                    else 'Abaixo do Esperado (<40%)'
                )
                
                faixas_count = students_df['faixa_desempenho'].value_counts()
                
                fig_pie = px.pie(
                    values=faixas_count.values,
                    names=faixas_count.index,
                    title='Distribuição por Faixa de Desempenho',
                    color_discrete_map={
                        'Excelente (80-100%)': '#2E8B57',
                        'Bom (60-79%)': '#32CD32',
                        'Regular (40-59%)': '#FFD700',
                        'Abaixo do Esperado (<40%)': '#DC143C'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Top 10 e Bottom 10 alunos
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("🏆 Top 10 Alunos")
                top_students = students_df.head(10)[['ALU_NOME', 'ESC_NOME', 'taxa_acerto', 'total_questoes']]
                st.dataframe(top_students, use_container_width=True)
            
            with col4:
                st.subheader("⚠️ Alunos que Precisam de Atenção")
                bottom_students = students_df.tail(10)[['ALU_NOME', 'ESC_NOME', 'taxa_acerto', 'total_questoes']]
                st.dataframe(bottom_students, use_container_width=True)
            
            # Análise por escola
            st.subheader("🏫 Desempenho por Escola")
            school_performance = students_df.groupby('ESC_NOME').agg({
                'taxa_acerto': 'mean',
                'ALU_ID': 'count',
                'total_questoes': 'sum'
            }).round(2).reset_index()
            school_performance.columns = ['Escola', 'Taxa Média (%)', 'Qtd Alunos', 'Total Questões']
            school_performance = school_performance.sort_values('Taxa Média (%)', ascending=False)
            
            fig_school = px.bar(
                school_performance,
                x='Escola',
                y='Taxa Média (%)',
                color='Taxa Média (%)',
                title='Taxa Média de Acerto por Escola',
                color_continuous_scale='RdYlGn',
                hover_data=['Qtd Alunos', 'Total Questões']
            )
            fig_school.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_school, use_container_width=True)
        
        else:
            st.warning("⚠️ Nenhum dado de aluno encontrado para os filtros selecionados")
    
    def competency_analysis(self, filters: Dict[str, Any]):
        """Análise por competências (descritores)"""
        st.header("🎯 Análise por Competências")
        
        where_clause = self.build_where_clause(filters)
        
        # Query para análise por descritores
        competency_query = f"""
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
        
        competency_df = self.get_data(competency_query)
        
        if not competency_df.empty:
            # Gráfico de barras das competências
            st.subheader("📊 Taxa de Acerto por Competência")
            
            fig_comp = px.bar(
                competency_df.head(20),  # Mostrar top 20 para melhor visualização
                x='taxa_acerto',
                y='MTI_CODIGO',
                orientation='h',
                title='Taxa de Acerto por Competência (20 menores taxas)',
                labels={'taxa_acerto': 'Taxa de Acerto (%)', 'MTI_CODIGO': 'Código da Competência'},
                color='taxa_acerto',
                color_continuous_scale='RdYlGn',
                hover_data=['alunos_avaliados', 'total_questoes']
            )
            fig_comp.update_layout(height=700)
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Tabelas de competências críticas e de destaque
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚨 Competências Críticas (Menores Taxas)")
                critical_comp = competency_df.head(5)[['MTI_CODIGO', 'MTI_DESCRITOR', 'taxa_acerto', 'alunos_avaliados']]
                st.dataframe(critical_comp, use_container_width=True)
            
            with col2:
                st.subheader("⭐ Competências de Destaque (Maiores Taxas)")
                best_comp = competency_df.tail(5)[['MTI_CODIGO', 'MTI_DESCRITOR', 'taxa_acerto', 'alunos_avaliados']]
                st.dataframe(best_comp, use_container_width=True)
        
        else:
            st.warning("⚠️ Nenhum dado de competência encontrado para os filtros selecionados")
    
    def render(self):
        """Renderiza o painel de análise detalhada"""
        st.title(self.panel_title)
        st.markdown("### Análise granular com múltiplos filtros para investigação detalhada")
        st.markdown("---")
        
        # Mostrar informações do ambiente
        self.show_environment_info()
        
        # Criar filtros avançados
        filters = self.create_advanced_filters()
        
        if filters:
            # Exibir resumo da seleção
            self.show_summary_metrics(filters)
            st.markdown("---")
            
            # Análise de desempenho dos alunos
            self.student_performance_analysis(filters)
            st.markdown("---")
            
            # Análise por competências
            self.competency_analysis(filters)
            
            # Informações adicionais
            with st.expander("ℹ️ Sobre este Painel"):
                st.markdown("""
                ### 🎯 Funcionalidades do Painel de Análise Detalhada
                
                Este painel permite análises granulares através de:
                
                #### 🔍 **Filtros Múltiplos:**
                - **Estado (UF)**: Seleção de unidades federativas
                - **Município**: Filtro por cidades específicas
                - **Escola**: Análise por instituições de ensino
                - **Ano**: Comparação temporal de avaliações
                - **Disciplina**: Foco em áreas específicas do conhecimento
                - **Teste**: Análise de instrumentos avaliativos específicos
                - **Série**: Segmentação por níveis educacionais
                
                #### 📊 **Análises Fornecidas:**
                - **Taxa de acerto geral e individual**
                - **Distribuição de desempenho em faixas**
                - **Ranking de alunos (melhores e que precisam de atenção)**
                - **Comparação entre escolas**
                - **Análise por competências/descritores**
                
                #### 🚀 **Otimizações Star Schema:**
                - Consultas otimizadas com JOINs diretos
                - Agregações pré-calculadas na tabela fato
                - Performance superior para análises complexas
                """)


def main():
    """Função principal da galeria"""
    st.title("🎨 Galeria de Painéis SAEV")
    st.markdown("### Sistema Avançado de Análise Educacional - Múltiplos Painéis Especializados")
    
    # Menu de seleção de painéis
    st.sidebar.title("🎨 Galeria de Painéis")
    st.sidebar.markdown("Selecione o painel desejado:")
    
    panel_options = {
        "🎯 Análise Detalhada por Filtros": "detailed_analysis",
        "📊 Dashboard Geral (Em Desenvolvimento)": "general_dashboard", 
        "🏫 Análise por Escola (Em Desenvolvimento)": "school_analysis",
        "🏙️ Análise por Município (Em Desenvolvimento)": "municipality_analysis",
        "📈 Análise Temporal (Em Desenvolvimento)": "temporal_analysis"
    }
    
    selected_panel = st.sidebar.selectbox(
        "Escolha o Painel:",
        list(panel_options.keys())
    )
    
    st.markdown("---")
    
    # Renderizar painel selecionado
    if panel_options[selected_panel] == "detailed_analysis":
        panel = DetailedAnalysisPanel()
        panel.render()
    
    else:
        # Painéis em desenvolvimento
        st.header(selected_panel)
        st.info("🚧 Este painel está em desenvolvimento e será disponibilizado em breve!")
        
        st.markdown("### 🔄 Painéis Disponíveis:")
        st.markdown("- ✅ **Análise Detalhada por Filtros** - Funcional")
        st.markdown("- 🚧 **Dashboard Geral** - Em desenvolvimento")
        st.markdown("- 🚧 **Análise por Escola** - Em desenvolvimento") 
        st.markdown("- 🚧 **Análise por Município** - Em desenvolvimento")
        st.markdown("- 🚧 **Análise Temporal** - Em desenvolvimento")
        
        st.markdown("### 🎯 Próximos Painéis:")
        st.markdown("""
        1. **Dashboard Geral**: Visão panorâmica de todos os dados
        2. **Análise por Escola**: Foco em análises institucionais
        3. **Análise por Município**: Comparações regionais
        4. **Análise Temporal**: Evolução histórica dos indicadores
        5. **Análise de Competências**: Foco em habilidades específicas
        """)


if __name__ == "__main__":
    main()
