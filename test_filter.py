#!/usr/bin/env python3
"""
Teste para verificar se o filtro de série está funcionando
"""
import sqlite3
import pandas as pd

def test_series_filter():
    """Testa o filtro de série"""
    db_path = "db/avaliacao_teste.db"
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    
    # Obter séries disponíveis
    series_query = "SELECT DISTINCT SER_NOME FROM avaliacao ORDER BY SER_NOME"
    series_df = pd.read_sql_query(series_query, conn)
    series_list = series_df['SER_NOME'].tolist()
    
    print("📊 Séries disponíveis:")
    for i, serie in enumerate(series_list, 1):
        print(f"   {i}. {serie}")
    
    # Verificar se 1º Ano EF existe
    if "1º Ano EF" in series_list:
        print("\n✅ '1º Ano EF' encontrado na lista!")
        print("🎯 O filtro deve selecionar '1º Ano EF' por padrão")
        
        # Contar registros para 1º Ano EF
        count_query = "SELECT COUNT(*) as total FROM avaliacao WHERE SER_NOME = '1º Ano EF'"
        count_df = pd.read_sql_query(count_query, conn)
        total = count_df['total'].iloc[0]
        print(f"📈 Total de registros para '1º Ano EF': {total:,}")
        
    else:
        print("\n❌ '1º Ano EF' NÃO encontrado!")
        print("🔄 Será usado o primeiro da lista:", series_list[0] if series_list else "Nenhum")
    
    conn.close()

if __name__ == "__main__":
    test_series_filter()
