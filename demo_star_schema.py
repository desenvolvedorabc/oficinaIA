#!/usr/bin/env python3
"""
Script de demonstração do Star Schema SAEV
Testa a aplicação e consultas do modelo Star Schema
"""
import sqlite3
import time
import os
from pathlib import Path

def test_star_schema():
    """Testa a criação e performance do Star Schema"""
    
    # Verificar se o banco de teste existe
    db_path = "db/avaliacao_teste.db"
    if not Path(db_path).exists():
        print("❌ Banco de teste não encontrado!")
        print(f"   Procurando: {db_path}")
        return
    
    print("🚀 TESTE DO STAR SCHEMA SAEV")
    print("=" * 50)
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar estrutura original
    print("📊 Verificando estrutura original...")
    cursor.execute("SELECT COUNT(*) FROM avaliacao")
    original_count = cursor.fetchone()[0]
    print(f"   Registros na tabela original: {original_count:,}")
    
    # Aplicar Star Schema
    print("\n⭐ Aplicando transformação Star Schema...")
    start_time = time.time()
    
    try:
        # Ler e executar o script SQL
        with open("src/star_schema.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        # Executar o script (remover comandos .print que são específicos do sqlite3 CLI)
        sql_commands = sql_script.replace('.print', '-- .print')
        cursor.executescript(sql_commands)
        
        transform_time = time.time() - start_time
        print(f"✅ Transformação concluída em {transform_time:.2f} segundos!")
        
    except Exception as e:
        print(f"❌ Erro na transformação: {e}")
        conn.close()
        return
    
    # Verificar estruturas criadas
    print("\n📋 Verificando estruturas criadas...")
    
    tables = ['dim_aluno', 'dim_escola', 'dim_descritor', 'fato_resposta_aluno', 'teste']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count:,} registros")
        except Exception as e:
            print(f"   {table}: ❌ Não encontrada ({e})")
    
    # Teste de performance
    print("\n⚡ Teste de Performance...")
    
    # Consulta na tabela original
    print("   Testando consulta na tabela original...")
    start_time = time.time()
    cursor.execute("""
        SELECT ESC_NOME, COUNT(DISTINCT ALU_ID) as alunos, 
               ROUND(AVG(CAST(ATR_CERTO AS FLOAT)) * 100, 2) as taxa_acerto
        FROM avaliacao 
        WHERE DIS_NOME = 'Matemática' 
        GROUP BY ESC_NOME 
        ORDER BY taxa_acerto DESC 
        LIMIT 5
    """)
    results_original = cursor.fetchall()
    time_original = time.time() - start_time
    
    # Consulta no Star Schema
    print("   Testando consulta no Star Schema...")
    start_time = time.time()
    cursor.execute("""
        SELECT e.ESC_NOME, COUNT(DISTINCT f.ALU_ID) as alunos,
               ROUND((SUM(f.ACERTO) * 100.0) / (SUM(f.ACERTO) + SUM(f.ERRO)), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        JOIN dim_escola e ON f.ESC_INEP = e.ESC_INEP
        WHERE f.DIS_NOME = 'Matemática'
        GROUP BY e.ESC_NOME
        ORDER BY taxa_acerto DESC
        LIMIT 5
    """)
    results_star = cursor.fetchall()
    time_star = time.time() - start_time
    
    # Mostrar resultados
    print(f"\n📊 RESULTADOS DE PERFORMANCE:")
    print(f"   Consulta Original: {time_original:.4f}s")
    print(f"   Consulta Star Schema: {time_star:.4f}s")
    
    if time_original > 0:
        improvement = time_original / time_star if time_star > 0 else float('inf')
        print(f"   Melhoria: {improvement:.1f}x mais rápido!")
    
    print(f"\n🏆 TOP 5 ESCOLAS (Star Schema):")
    for i, (escola, alunos, taxa) in enumerate(results_star[:5], 1):
        # Decodificar nome se estiver em MD5 (ambiente de teste)
        escola_display = f"Escola {i}" if len(escola) == 32 else escola
        print(f"   {i}. {escola_display}: {alunos} alunos, {taxa}% acerto")
    
    # Teste de consulta avançada
    print(f"\n🎯 ANÁLISE DE COMPETÊNCIAS:")
    cursor.execute("""
        SELECT d.MTI_CODIGO, 
               SUM(f.ACERTO + f.ERRO) as total_respostas,
               ROUND((SUM(f.ACERTO) * 100.0) / (SUM(f.ACERTO) + SUM(f.ERRO)), 2) as taxa_acerto
        FROM fato_resposta_aluno f
        JOIN dim_descritor d ON f.MTI_CODIGO = d.MTI_CODIGO
        WHERE f.DIS_NOME = 'Matemática'
        GROUP BY d.MTI_CODIGO
        ORDER BY taxa_acerto ASC
        LIMIT 3
    """)
    
    competencias = cursor.fetchall()
    print("   Competências que mais precisam de atenção:")
    for i, (codigo, total, taxa) in enumerate(competencias, 1):
        print(f"   {i}. {codigo}: {total:,} respostas, {taxa}% acerto")
    
    conn.close()
    
    print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("💡 O Star Schema está pronto para análises de alta performance!")

if __name__ == "__main__":
    test_star_schema()
