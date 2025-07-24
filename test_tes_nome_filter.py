#!/usr/bin/env python3
"""
Teste para verificar se o novo filtro de TES_NOME está funcionando
"""
import sqlite3
import pandas as pd

def test_test_filter():
    """Testa o filtro de teste"""
    db_path = "db/avaliacao_teste.db"
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    
    # Obter disciplinas disponíveis
    disciplines_query = "SELECT DISTINCT DIS_NOME FROM avaliacao ORDER BY DIS_NOME"
    disciplines_df = pd.read_sql_query(disciplines_query, conn)
    print("📚 Disciplinas disponíveis:")
    for disc in disciplines_df['DIS_NOME'].tolist():
        print(f"   • {disc}")
    
    # Testar para cada disciplina
    for discipline in disciplines_df['DIS_NOME'].tolist():
        print(f"\n🔍 Testes para '{discipline}':")
        tests_query = f"SELECT DISTINCT TES_NOME FROM avaliacao WHERE DIS_NOME = '{discipline}' ORDER BY TES_NOME"
        tests_df = pd.read_sql_query(tests_query, conn)
        
        for test in tests_df['TES_NOME'].tolist():
            # Contar registros para este teste
            count_query = f"SELECT COUNT(*) as total FROM avaliacao WHERE DIS_NOME = '{discipline}' AND TES_NOME = '{test}'"
            count_df = pd.read_sql_query(count_query, conn)
            total = count_df['total'].iloc[0]
            print(f"   📊 {test}: {total:,} registros")
    
    conn.close()
    print("\n✅ Teste do filtro de TES_NOME concluído!")

if __name__ == "__main__":
    test_test_filter()
