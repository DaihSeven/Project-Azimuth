import os
import csv

PASTA_CSV = "1-lh_nautical_csv"
ARQUIVO_SQL = "sql/schema.sql"

BIGINT_MIN = -9223372036854775807
BIGINT_MAX = 9223372036854775807


def e_timestamp(v):
    if len(v) >= 19 and v[4] == "-" and v[7] == "-" and v[10] in (" ", "T") and v[13] == ":" and v[16] == ":":
        return v[0:4].isdigit()
    return False


def e_data(v):
    if len(v) == 10 and v[4] == "-" and v[7] == "-":
        return v[0:4].isdigit() and v[5:7].isdigit() and v[8:10].isdigit()
    return False


def detectar_tipo(valores):
    if not valores:
        return "VARCHAR(255)"

    if all(v.lower() in ("true", "false", "t", "f") for v in valores):
        return "BOOLEAN"

    eh_int = True
    for v in valores:
        try:
            num = int(v)
            if num < BIGINT_MIN or num > BIGINT_MAX:
                eh_int = False
                break
        except ValueError:
            eh_int = False
            break
    if eh_int:
        return "BIGINT"

    eh_numeric = True
    for v in valores:
        try:
            float(v)
        except ValueError:
            eh_numeric = False
            break
    if eh_numeric:
        return "NUMERIC"

    if all(e_timestamp(v) for v in valores):
        return "TIMESTAMP"

    if all(e_data(v) for v in valores):
        return "DATE"

    if max(len(v) for v in valores) > 255:
        return "TEXT"

    return "VARCHAR(255)"


def main():
    arquivos = sorted([f for f in os.listdir(PASTA_CSV) if f.endswith(".csv")])

    with open(ARQUIVO_SQL, "w", encoding="utf-8") as saida:
        for arquivo in arquivos:
            tabela = arquivo.replace(".csv", "").lower()
            caminho = os.path.join(PASTA_CSV, arquivo)

            with open(caminho, "r", encoding="utf-8-sig") as f:
                leitor = csv.reader(f)
                cabecalho = next(leitor, None)

                if not cabecalho:
                    continue

                colunas = [col.strip().lower() for col in cabecalho]
                amostras = {col: [] for col in colunas}

                for linha in leitor:
                    for idx, val in enumerate(linha):
                        val_limpo = val.strip()
                        if idx < len(colunas) and val_limpo != "":
                            amostras[colunas[idx]].append(val_limpo)

                defs = []
                for col in colunas:
                    tipo = detectar_tipo(amostras[col])
                    defs.append(f"    {col} {tipo}")

                sql = f"CREATE TABLE IF NOT EXISTS {tabela} (\n" + ",\n".join(defs) + "\n);\n\n"
                saida.write(sql)

    print(f"Novo {ARQUIVO_SQL} gerado com sucesso!")


if __name__ == "__main__":
    main()