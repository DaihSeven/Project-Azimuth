import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PASTA_CSV = os.getenv("PASTA_CSV", "1-lh_nautical_csv")

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
            sql_copy = f"COPY {tabela} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');"
            cursor.copy_expert(sql=sql_copy, file=f)

        conn.commit()

    cursor.close()
    conn.close()
    print("\nTodos os 24 arquivos foram carregados com sucesso!")


if __name__ == "__main__":
    carregar_arquivos()

