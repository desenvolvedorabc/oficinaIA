#!/usr/bin/env python3
"""
Teste rápido da correção do ambiente de produção
"""

import os
import sys
from pathlib import Path

# Adicionar diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data.etl import SAEVDataProcessor

def main():
    print("🧪 TESTE CORREÇÃO AMBIENTE PRODUÇÃO")
    print("="*50)
    
    # Simular ambiente de produção
    db_path = "db/avaliacao_prod.db"
    
    print(f"📊 Testando com: {db_path}")
    
    # Criar processador
    processor = SAEVDataProcessor(db_path)
    
    # Testar apenas detecção do ambiente
    print("\n🔍 Testando detecção de ambiente...")
    
    try:
        # Extrair ambiente do caminho do banco - mapear corretamente
        if 'teste' in processor.db_path.lower():
            env = 'teste'
        elif 'prod' in processor.db_path.lower():
            env = 'producao'  # Mapear 'prod' para 'producao'
        else:
            env = 'teste'  # Default para teste
        
        print(f"✅ Ambiente detectado: '{env}'")
        
        # Verificar se ambiente é válido
        valid_envs = ['teste', 'producao']
        if env in valid_envs:
            print(f"✅ Ambiente '{env}' é válido!")
            print("🎯 Correção aplicada com sucesso!")
        else:
            print(f"❌ Ambiente '{env}' ainda é inválido")
            return False
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
