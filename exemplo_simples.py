#!/usr/bin/env python3
"""
Exemplo Simples - Como usar Relatórios e Análises do SAEV
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

def exemplo_relatorios():
    """Exemplo de como gerar relatórios"""
    print("📋 EXEMPLO: Gerando Relatórios")
    print("="*40)
    
    try:
        # Importar o que precisamos
        from src.reports.generator import SAEVReports
        from src.config import config
        
        # 1. Forma mais simples (detecção automática do banco)
        print("1️⃣ Usando detecção automática:")
        reports = SAEVReports()  # Sem parâmetros = detecção automática
        
        # 2. Forma específica (escolhendo o ambiente)
        print("2️⃣ Usando ambiente específico:")
        db_path_teste = config.get_database_path('teste')
        reports_teste = SAEVReports(db_path_teste)
        
        # 3. Gerar um relatório de exemplo
        print("3️⃣ Gerando relatório municipal...")
        arquivo = reports.generate_municipal_report(2023, "Matemática")
        print(f"✅ Relatório salvo em: {arquivo}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Certifique-se de que há dados no banco")

def exemplo_analytics():
    """Exemplo de como fazer análises"""
    print("\n🔬 EXEMPLO: Fazendo Análises Estatísticas")
    print("="*45)
    
    try:
        # Importar o que precisamos
        from src.analytics.advanced import SAEVAnalytics
        from src.config import config
        
        # 1. Forma mais simples (detecção automática)
        print("1️⃣ Usando detecção automática:")
        analytics = SAEVAnalytics()  # Sem parâmetros = detecção automática
        
        # 2. Fazer clustering de escolas
        print("2️⃣ Fazendo clustering de escolas...")
        resultado = analytics.school_clustering(2023, "Matemática")
        
        if 'error' not in resultado:
            print(f"✅ Identificados {resultado['n_clusters']} grupos de escolas")
            print("📊 Grupos encontrados:")
            for cluster_id, nome in resultado['cluster_names'].items():
                print(f"   • Grupo {cluster_id + 1}: {nome}")
        else:
            print(f"⚠️ {resultado['error']}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Certifique-se de que há dados suficientes no banco")

def mostrar_codigo():
    """Mostra o código que você pode usar"""
    print("\n💻 CÓDIGO PARA VOCÊ USAR:")
    print("="*30)
    
    codigo = '''
# RELATÓRIOS - Copie e cole este código:

from src.reports.generator import SAEVReports

# Método 1: Detecção automática (mais fácil)
reports = SAEVReports()
arquivo = reports.generate_municipal_report(2023, "Matemática")
print(f"Relatório: {arquivo}")

# Método 2: Especificando o banco
from src.config import config
db_path = config.get_database_path('teste')  # ou 'producao'
reports = SAEVReports(db_path)

# ANÁLISES - Copie e cole este código:

from src.analytics.advanced import SAEVAnalytics

# Método 1: Detecção automática (mais fácil)
analytics = SAEVAnalytics()
resultado = analytics.school_clustering(2023, "Português")
print(f"Grupos: {resultado['n_clusters']}")

# Método 2: Especificando o banco
analytics = SAEVAnalytics(db_path)
equidade = analytics.equity_analysis(2023, "Matemática")
print(f"Municípios analisados: {len(equidade)}")
    '''
    
    print(codigo)

if __name__ == "__main__":
    print("🚀 EXEMPLOS PRÁTICOS - Relatórios e Análises SAEV")
    print("Este script mostra como usar as funcionalidades avançadas")
    
    # Verificar se há dados
    try:
        from src.config import config
        import sqlite3
        
        db_path = config.get_database_path()
        
        if not Path(db_path).exists():
            print(f"\n❌ Banco não encontrado: {db_path}")
            print("💡 Execute: ./iniciar.sh e configure um ambiente")
            sys.exit(1)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM avaliacao")
        total = cursor.fetchone()[0]
        conn.close()
        
        if total == 0:
            print(f"\n⚠️ Banco vazio: {db_path}")
            print("💡 Execute um script de carga para adicionar dados")
            sys.exit(1)
        
        print(f"\n✅ Banco encontrado: {Path(db_path).name} ({total:,} registros)")
        
    except Exception as e:
        print(f"\n❌ Erro ao verificar dados: {e}")
        sys.exit(1)
    
    # Executar exemplos
    exemplo_relatorios()
    exemplo_analytics() 
    mostrar_codigo()
    
    print("\n🎉 Exemplos concluídos!")
    print("💡 Use os códigos acima em seus próprios scripts Python")
