import sqlite3
import csv
import sys
import hashlib

def carregar_municipios(nome_arquivo):
    with open(nome_arquivo, encoding='utf-8') as f:
        # Remove linhas em branco e espaços
        return set(linha.strip() for linha in f if linha.strip())

def md5_hash(texto):
    # Retorna o hash MD5 em hexadecimal
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

def main():
    if len(sys.argv) < 3:
        print("Uso: python importa_csv.py arquivo.csv cidade_teste.txt [banco.db]")
        sys.exit(1)

    csv_file = sys.argv[1]
    cidades_file = sys.argv[2]
    db_file = sys.argv[3] if len(sys.argv) > 3 else "avaliacao_teste.db"

    municipios_validos = carregar_municipios(cidades_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        colunas = reader.fieldnames

        # Prepara o comando de insert
        campos = ','.join(colunas)
        valores = ','.join(['?' for _ in colunas])
        insert_sql = f'INSERT INTO avaliacao ({campos}) VALUES ({valores})'

        for row in reader:
            # Filtra município
            if row['MUN_NOME'] not in municipios_validos:
                continue

            # Criptografa o nome do aluno usando MD5
            row['ALU_NOME'] = md5_hash(row['ALU_NOME'])
            row['ALU_CPF'] = md5_hash(row['ALU_CPF'])
            row['MUN_NOME'] = md5_hash(row['MUN_NOME'])
            row['ESC_NOME'] = md5_hash(row['ESC_NOME'])
            dados = [row[col] for col in colunas]
            cursor.execute(insert_sql, dados)

    conn.commit()
    print(f"Importação concluída para municípios selecionados: {csv_file} → {db_file}")
    conn.close()

if __name__ == "__main__":
    main()
