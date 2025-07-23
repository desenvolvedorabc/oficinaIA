#!/usr/bin/env python3
"""
Script de Demonstração das Funcionalidades Avançadas do SAEV
Este script mostra como usar os recursos de relatórios e análises do sistema.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent))

from src.config import config
from src.reports.generator import SAEVReports
from src.analytics.advanced import SAEVAnalytics

def print_header(title):
    """Imprime um cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🔬 {title}")
    print("="*60)

def demonstrate_reports():
    """Demonstra a funcionalidade de relatórios"""
    print_header("DEMONSTRAÇÃO DE RELATÓRIOS AUTOMATIZADOS")
    
    try:
        # Detectar ambiente e obter caminho do banco
        environment = config.detect_environment()
        db_path = config.get_database_path(environment)
        
        print(f"📊 Usando ambiente: {environment.upper()}")
        print(f"📁 Banco de dados: {db_path}")
        
        # Criar instância do gerador de relatórios
        reports = SAEVReports(db_path)
        
        # 1. Relatório Municipal
        print("\n🏘️ Gerando Relatório Municipal...")
        try:
            arquivo_municipal = reports.generate_municipal_report(2023, "Matemática")
            print(f"✅ Relatório municipal gerado: {arquivo_municipal}")
        except Exception as e:
            print(f"⚠️ Erro ao gerar relatório municipal: {e}")
        
        # 2. Relatório de Escolas
        print("\n🏫 Gerando Relatório de Escolas...")
        try:
            arquivo_escolas = reports.generate_school_report(2023, "Português")
            print(f"✅ Relatório de escolas gerado: {arquivo_escolas}")
        except Exception as e:
            print(f"⚠️ Erro ao gerar relatório de escolas: {e}")
        
        # 3. Relatório de Competências
        print("\n🎯 Gerando Relatório de Competências...")
        try:
            arquivo_competencias = reports.generate_competency_report(2023, "Matemática")
            print(f"✅ Relatório de competências gerado: {arquivo_competencias}")
        except Exception as e:
            print(f"⚠️ Erro ao gerar relatório de competências: {e}")
        
        print("\n💡 Os relatórios foram salvos na pasta 'reports/' em formato Excel")
        
    except Exception as e:
        print(f"❌ Erro geral nos relatórios: {e}")

def demonstrate_analytics():
    """Demonstra as análises estatísticas avançadas"""
    print_header("DEMONSTRAÇÃO DE ANÁLISES ESTATÍSTICAS AVANÇADAS")
    
    try:
        # Detectar ambiente e obter caminho do banco
        environment = config.detect_environment()
        db_path = config.get_database_path(environment)
        
        print(f"📊 Usando ambiente: {environment.upper()}")
        print(f"📁 Banco de dados: {db_path}")
        
        # Criar instância do analisador
        analytics = SAEVAnalytics(db_path)
        
        # 1. Clustering de Escolas
        print("\n🔬 Realizando Clustering de Escolas...")
        try:
            resultado_clustering = analytics.school_clustering(2023, "Matemática")
            if 'error' not in resultado_clustering:
                print(f"✅ Clustering concluído: {resultado_clustering['n_clusters']} grupos identificados")
                
                # Mostrar nomes dos clusters
                for cluster_id, nome in resultado_clustering['cluster_names'].items():
                    escolas_no_cluster = len(resultado_clustering['data'][
                        resultado_clustering['data']['cluster'] == cluster_id
                    ])
                    print(f"   📊 Grupo {cluster_id + 1}: {nome} ({escolas_no_cluster} escolas)")
            else:
                print(f"⚠️ {resultado_clustering['error']}")
        except Exception as e:
            print(f"⚠️ Erro no clustering: {e}")
        
        # 2. Análise de Equidade
        print("\n⚖️ Analisando Equidade Educacional...")
        try:
            resultado_equidade = analytics.equity_analysis(2023, "Português")
            print(f"✅ Análise de equidade concluída para {len(resultado_equidade)} municípios")
            
            # Mostrar municípios com melhor e pior equidade
            melhor_equidade = resultado_equidade.nsmallest(3, 'coef_variacao')
            pior_equidade = resultado_equidade.nlargest(3, 'coef_variacao')
            
            print("\n🏆 Municípios com MELHOR equidade (menor variação):")
            for _, row in melhor_equidade.iterrows():
                print(f"   • {row['MUN_NOME']}: {row['nivel_equidade']} (CV: {row['coef_variacao']:.1f}%)")
            
            print("\n⚠️ Municípios que precisam de ATENÇÃO (maior variação):")
            for _, row in pior_equidade.iterrows():
                print(f"   • {row['MUN_NOME']}: {row['nivel_equidade']} (CV: {row['coef_variacao']:.1f}%)")
                
        except Exception as e:
            print(f"⚠️ Erro na análise de equidade: {e}")
        
        # 3. Análise de Correlação entre Competências
        print("\n🔗 Analisando Correlações entre Competências...")
        try:
            resultado_correlacao = analytics.competency_correlation_analysis(2023, "Matemática")
            
            print("✅ Análise de correlação concluída")
            
            # Mostrar correlações mais fortes
            top_correlacoes = resultado_correlacao['top_correlations'].head(3)
            print("\n🔝 Competências mais correlacionadas:")
            for _, row in top_correlacoes.iterrows():
                print(f"   • {row['competencia_1']} ↔ {row['competencia_2']}: {row['correlacao']:.3f}")
                
        except Exception as e:
            print(f"⚠️ Erro na análise de correlação: {e}")
            
    except Exception as e:
        print(f"❌ Erro geral nas análises: {e}")

def show_usage_examples():
    """Mostra exemplos de uso do código"""
    print_header("EXEMPLOS DE CÓDIGO PARA USO PRÓPRIO")
    
    print("""
📝 Para usar essas funcionalidades em seus próprios scripts Python:

1️⃣ RELATÓRIOS:
   
   from src.reports.generator import SAEVReports
   from src.config import config
   
   # Obter caminho do banco automaticamente
   db_path = config.get_database_path()  # ou especificar: 'teste' ou 'producao'
   
   # Criar gerador de relatórios
   reports = SAEVReports(db_path)
   
   # Gerar relatório municipal
   arquivo = reports.generate_municipal_report(2023, "Matemática")
   print(f"Relatório salvo em: {arquivo}")

2️⃣ ANÁLISES AVANÇADAS:
   
   from src.analytics.advanced import SAEVAnalytics
   from src.config import config
   
   # Obter caminho do banco automaticamente
   db_path = config.get_database_path()
   
   # Criar analisador
   analytics = SAEVAnalytics(db_path)
   
   # Fazer clustering de escolas
   resultado = analytics.school_clustering(2023, "Português")
   print(f"Identificados {resultado['n_clusters']} grupos de escolas")
   
   # Analisar equidade
   equidade = analytics.equity_analysis(2023, "Matemática")
   print(f"Análise de equidade para {len(equidade)} municípios")

3️⃣ EXECUTAR NO JUPYTER NOTEBOOK:
   
   # Primeiro, adicione o caminho do projeto:
   import sys
   sys.path.append('/caminho/para/oficinaIA')
   
   # Depois use os exemplos acima normalmente

4️⃣ EXECUTAR COMO SCRIPT:
   
   # Salve o código em um arquivo .py e execute:
   python meu_script_de_analise.py
    """)

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO DAS FUNCIONALIDADES AVANÇADAS DO SAEV")
    print("Este script demonstra como usar relatórios e análises do sistema")
    
    # Verificar se há dados disponíveis
    try:
        environment = config.detect_environment()
        db_path = config.get_database_path(environment)
        
        if not Path(db_path).exists():
            print(f"\n❌ Banco de dados não encontrado: {db_path}")
            print("💡 Execute primeiro um script de carga ou use ./iniciar.sh para configurar")
            return
        
        # Verificar se há dados na tabela
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM avaliacao")
        total_records = cursor.fetchone()[0]
        conn.close()
        
        if total_records == 0:
            print(f"\n⚠️ O banco existe mas não tem dados: {db_path}")
            print("💡 Execute um script de carga para importar dados")
            return
        
        print(f"\n✅ Banco encontrado com {total_records:,} registros")
        
    except Exception as e:
        print(f"\n❌ Erro ao verificar dados: {e}")
        return
    
    # Menu de opções
    while True:
        print("\n" + "="*60)
        print("📋 MENU DE DEMONSTRAÇÕES:")
        print("1️⃣  Demonstrar Relatórios Automatizados")
        print("2️⃣  Demonstrar Análises Estatísticas")
        print("3️⃣  Mostrar Exemplos de Código")
        print("4️⃣  Executar Tudo")
        print("5️⃣  Sair")
        print("="*60)
        
        opcao = input("\n🎯 Escolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            demonstrate_reports()
        elif opcao == "2":
            demonstrate_analytics()
        elif opcao == "3":
            show_usage_examples()
        elif opcao == "4":
            demonstrate_reports()
            demonstrate_analytics()
            show_usage_examples()
        elif opcao == "5":
            print("\n👋 Demonstração finalizada!")
            break
        else:
            print(f"\n❌ Opção inválida: {opcao}")

if __name__ == "__main__":
    main()
