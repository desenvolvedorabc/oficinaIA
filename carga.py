import sqlite3
import csv
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Uso: python importa_csv.py arquivo.csv [banco.db]")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_file = sys.argv[2] if len(sys.argv) > 2 else "avaliacao.db"

    # Conecta ou cria o banco de dados
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Abre o arquivo CSV
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        colunas = reader.fieldnames

        # Prepara o comando de insert
        campos = ','.join(colunas)
        valores = ','.join(['?' for _ in colunas])
        insert_sql = f'INSERT INTO avaliacao ({campos}) VALUES ({valores})'

        # Insere cada linha
        for row in reader:
            dados = [row[col] for col in colunas]
            cursor.execute(insert_sql, dados)

    conn.commit()
    print(f"Importação concluída: {csv_file} para {db_file}")
    conn.close()

if __name__ == "__main__":
    main()
