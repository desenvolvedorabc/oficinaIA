#!/usr/bin/env python3
"""
Script para aplicar transformação Star Schema em banco existente
Utiliza o módulo ETL para aplicar apenas a transformação Star Schema
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data.etl import SAEVDataProcessor

def main():
    """Função principal para aplicar Star Schema"""
    print("="*80)
    print("⭐ SAEV - APLICAR TRANSFORMAÇÃO STAR SCHEMA")
    print("="*80)
    
    if len(sys.argv) < 2:
        print("❌ Uso incorreto!")
        print("📋 Uso: python apply_star_schema.py banco.db")
        print("📋 Exemplo: python apply_star_schema.py db/avaliacao_prod.db")
        sys.exit(1)

    db_file = sys.argv[1]

    # Verificar se o banco existe
    if not Path(db_file).exists():
        print(f"❌ Banco de dados não encontrado: {db_file}")
        sys.exit(1)
    
    print(f"🗄️  Banco de dados: {db_file}")
    print()
    
    # Confirmar se é ambiente de produção
    if "prod" in db_file.lower():
        print("⚠️  ATENÇÃO: Você está modificando o banco de PRODUÇÃO!")
        resposta = input("❓ Deseja continuar? (sim/não): ").lower().strip()
        if resposta not in ['sim', 's', 'yes', 'y']:
            print("❌ Operação cancelada pelo usuário.")
            sys.exit(0)
        print()
    
    try:
        # Criar processador de dados
        processor = SAEVDataProcessor(db_file)
        
        # Validar dados existentes primeiro
        print("🔍 Validando dados existentes...")
        validation_results = processor.validate_data()
        
        if validation_results['total_records'] == 0:
            print("❌ Não há dados na tabela 'avaliacao'. Execute a carga primeiro.")
            sys.exit(1)
        
        print()
        
        # Aplicar apenas a transformação Star Schema
        processor.apply_star_schema()
        
        print()
        print("="*80)
        print("🎉 STAR SCHEMA APLICADO COM SUCESSO!")
        print(f"📊 Banco otimizado: {db_file}")
        print("⚡ Consultas agora executarão com melhor performance")
        print("="*80)
        
    except Exception as e:
        print()
        print("="*80)
        print(f"💥 ERRO NA APLICAÇÃO DO STAR SCHEMA: {e}")
        print("="*80)
        sys.exit(1)

if __name__ == "__main__":
    main()
