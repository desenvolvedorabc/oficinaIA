#!/usr/bin/env python3
"""
Script de carga de dados para ambiente de TESTE
Carrega dados CSV filtrados e anonimizados para o banco SQLite com transformação Star Schema
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data.etl import SAEVDataProcessor

def carregar_municipios(nome_arquivo):
    """Carrega lista de municípios válidos do arquivo"""
    try:
        with open(nome_arquivo, encoding='utf-8') as f:
            # Remove linhas em branco e espaços
            municipios = set(linha.strip() for linha in f if linha.strip())
        print(f"📋 Municípios carregados: {len(municipios)}")
        for municipio in sorted(municipios):
            print(f"   • {municipio}")
        return municipios
    except FileNotFoundError:
        print(f"❌ Arquivo de municípios não encontrado: {nome_arquivo}")
        sys.exit(1)

def main():
    """Função principal do script de carga de teste"""
    print("="*80)
    print("🧪 SAEV - CARGA DE DADOS PARA TESTE (Dados Anonimizados)")
    print("="*80)
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("❌ Uso incorreto!")
        print("📋 Uso: python carga_teste.py cidade_teste.txt [banco.db]")
        print("📋 Exemplo: python carga_teste.py cidade_teste.txt db/avaliacao_teste.db")
        print()
        print("📝 Parâmetros:")
        print("   📁 Origem: data/raw/ (todos os arquivos CSV)")
        print("   1️⃣  cidade_teste.txt - Arquivo com lista de cidades para filtrar")
        print("   2️⃣  banco.db         - Banco de dados de destino (opcional)")
        print()
        print("💡 O script processará TODOS os arquivos CSV da pasta data/raw automaticamente")
        sys.exit(1)

    cidades_file = sys.argv[1]
    db_file = sys.argv[2] if len(sys.argv) > 2 else "db/avaliacao_teste.db"
    csv_folder = "data/raw"

    # Verificar se a pasta data/raw existe
    if not Path(csv_folder).exists():
        print(f"❌ Pasta de dados não encontrada: {csv_folder}")
        print("💡 Certifique-se de que a pasta data/raw existe e contém arquivos CSV.")
        sys.exit(1)
    
    # Verificar se há arquivos CSV na pasta
    csv_files = list(Path(csv_folder).glob("*.csv"))
    if not csv_files:
        print(f"❌ Nenhum arquivo CSV encontrado em: {csv_folder}")
        print("💡 Adicione arquivos CSV na pasta data/raw.")
        sys.exit(1)
        
    if not Path(cidades_file).exists():
        print(f"❌ Arquivo de cidades não encontrado: {cidades_file}")
        print("💡 Este arquivo deve conter a lista de municípios para filtrar (um por linha).")
        print("💡 Exemplo de conteúdo do arquivo:")
        print("   São Paulo")
        print("   Rio de Janeiro")
        print("   Belo Horizonte")
        sys.exit(1)
    
    print(f"📁 Pasta de origem: {csv_folder}")
    print(f"📄 Arquivos encontrados: {len(csv_files)}")
    for csv_file in sorted(csv_files):
        print(f"   • {csv_file.name}")
    print(f"🏙️  Arquivo de cidades: {cidades_file}")
    print(f"🗄️  Banco de dados: {db_file}")
    print()
    
    # Carregar municípios válidos
    print("🏙️  Carregando municípios válidos...")
    municipios_validos = carregar_municipios(cidades_file)
    print()
    
    try:
        # Criar processador de dados
        processor = SAEVDataProcessor(db_file)
        
        # Executar processo completo de ETL para teste com DuckDB
        processor.full_etl_process(
            csv_folder=csv_folder,  # Usar pasta em vez de arquivo único
            test_mode=True,  # Modo teste com anonimização
            allowed_cities=list(municipios_validos),
            apply_star_schema=True,
            overwrite_db=True,
            include_duckdb=True,    # NOVO: Migração automática para DuckDB
            force_duckdb=True       # NOVO: Forçar recriação do DuckDB
        )
        
        print()
        print("="*80)
        print("🎉 CARGA DE TESTE CONCLUÍDA COM SUCESSO!")
        print(f"📊 Dados anonimizados disponíveis em: {db_file}")
        print(f"🦆 Dados DuckDB disponíveis em: {db_file.replace('.db', '_duckdb.db')}")
        print("⭐ Star Schema aplicado para análises otimizadas")
        print("🔒 Dados sensíveis foram anonimizados com MD5")
        print("🚀 Performance otimizada com DuckDB")
        print()
        print("💡 Próximos passos:")
        print("   • Use './iniciar.sh' para dashboard SQLite")
        print("   • Use './galeria.sh' para galeria com DuckDB")
        print("="*80)
        
    except Exception as e:
        print()
        print("="*80)
        print(f"💥 ERRO NA CARGA: {e}")
        print("="*80)
        sys.exit(1)

if __name__ == "__main__":
    main()
