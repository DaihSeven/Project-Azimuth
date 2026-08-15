import os
import psycopg2

# Configuração da conexão com o banco Neon
DATABASE_URL = "postgresql://neondb_owner:npg_FSWUarYVJ74T@ep-small-star-axpsu62l-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"
PASTA_CSV = "1-lh_nautical_csv"


def carregar_arquivos():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    arquivos = sorted([f for f in os.listdir(PASTA_CSV) if f.endswith(".csv")])
    print(f"Iniciando carga de {len(arquivos)} tabelas...")

    for arquivo in arquivos:
        tabela = arquivo.replace(".csv", "").lower()
        caminho_arquivo = os.path.join(PASTA_CSV, arquivo)

        print(f"-> Inserindo dados em '{tabela}'...")
        with open(caminho_arquivo, mode="r", encoding="utf-8-sig") as f:
            # COPY nativo do PostgreSQL: lê o CSV mantendo os dados exatamente como estão
            sql_copy = f"COPY {tabela} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');"
            cursor.copy_expert(sql=sql_copy, file=f)

        conn.commit()

    cursor.close()
    conn.close()
    print("\nTodos os 24 arquivos foram carregados com sucesso!")


if __name__ == "__main__":
    carregar_arquivos()

