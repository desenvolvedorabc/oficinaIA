#!/usr/bin/env python3
"""
Script de carga de dados para ambiente de PRODUÇÃO
Carrega dados CSV para o banco SQLite com transformação Star Schema
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data.etl import SAEVDataProcessor

def main():
    """Função principal do script de carga"""
    print("="*80)
    print("🎯 SAEV - CARGA DE DADOS PARA PRODUÇÃO")
    print("="*80)
    
    if len(sys.argv) > 2:
        print("❌ Uso incorreto!")
        print("📋 Uso: python carga.py [banco.db]")
        print("📋 Exemplo: python carga.py db/avaliacao_prod.db")
        print()
        print("📝 Parâmetros:")
        print("   📁 Origem: data/raw/ (todos os arquivos CSV)")
        print("   🗄️  banco.db - Banco de dados de destino (opcional)")
        print()
        print("💡 O script processará TODOS os arquivos CSV da pasta data/raw automaticamente")
        sys.exit(1)

    db_file = sys.argv[1] if len(sys.argv) > 1 else "db/avaliacao_prod.db"
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
    
    print(f"📁 Pasta de origem: {csv_folder}")
    print(f"📄 Arquivos encontrados: {len(csv_files)}")
    for csv_file in sorted(csv_files):
        print(f"   • {csv_file.name}")
    print(f"🗄️  Banco de dados: {db_file}")
    print()
    
    # Confirmar se é ambiente de produção
    if "prod" in db_file.lower():
        print("⚠️  ATENÇÃO: Você está carregando dados para PRODUÇÃO!")
        resposta = input("❓ Deseja continuar? (sim/não): ").lower().strip()
        if resposta not in ['sim', 's', 'yes', 'y']:
            print("❌ Operação cancelada pelo usuário.")
            sys.exit(0)
        print()
    
    try:
        # Criar processador de dados
        processor = SAEVDataProcessor(db_file)
        
        # Executar processo completo de ETL
        processor.full_etl_process(
            csv_folder=csv_folder,  # Usar pasta em vez de arquivo único
            test_mode=False,  # Modo produção
            apply_star_schema=True,
            overwrite_db=True
        )
        
        print()
        print("="*80)
        print("🎉 CARGA CONCLUÍDA COM SUCESSO!")
        print(f"📊 Dados disponíveis em: {db_file}")
        print("⭐ Star Schema aplicado para análises otimizadas")
        print("="*80)
        
    except Exception as e:
        print()
        print("="*80)
        print(f"💥 ERRO NA CARGA: {e}")
        print("="*80)
        sys.exit(1)

if __name__ == "__main__":
    main()
