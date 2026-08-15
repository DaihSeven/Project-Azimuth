import os
import csv

PASTA_CSV = "1-lh_nautical_csv"


def calcular_previsao():
    # 1. Identifica o ID do produto "Bússola de Bordo 702"
    bussola_ids = set()
    with open(os.path.join(PASTA_CSV, "products.csv"), mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Bússola de Bordo 702" in row["name"]:
                bussola_ids.add(row["id"])

    # 2. Identifica as variantes associadas
    variant_ids = set()
    with open(os.path.join(PASTA_CSV, "product_variants.csv"), mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product_id"] in bussola_ids:
                variant_ids.add(row["id"])

    # 3. Identifica as quantidades vendidas por id_pedido
    order_quantities = {}
    with open(os.path.join(PASTA_CSV, "order_items.csv"), mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product_variant_id"] in variant_ids:
                oid = row["order_id"]
                qty = int(float(row["quantity"]))
                order_quantities[oid] = order_quantities.get(oid, 0) + qty

    # 4. Associa a data do pedido e agrupa o faturamento/quantidade mensal
    vendas_mensais = {}
    with open(os.path.join(PASTA_CSV, "orders.csv"), mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            oid = row["id"]
            if oid in order_quantities:
                # Extrai YYYY-MM
                ano_mes = row["created_at"][:7]
                vendas_mensais[ano_mes] = vendas_mensais.get(ano_mes, 0) + order_quantities[oid]

    # 5. Gera a lista contínua de meses do histórico até março de 2026
    meses = []
    for ano in range(2020, 2027):
        for mes in range(1, 13):
            m_str = f"{ano}-{mes:02d}"
            meses.append(m_str)
            if m_str == "2026-03":
                break
        if "2026-03" in meses:
            break

    # Preenche zero para meses sem vendas
    vendas_reais = [vendas_mensais.get(m, 0) for m in meses]

    # 6. Cálculo da Média Móvel de 3 Meses (sem data leakage)
    previsoes = {}
    for i in range(len(meses)):
        if i < 3:
            previsoes[meses[i]] = None
        else:
            # Média dos 3 meses anteriores
            ultimos_3 = vendas_reais[i-3:i]
            previsoes[meses[i]] = sum(ultimos_3) / 3.0

    # 7. Avaliação no Período de Teste (Q1 2026: Jan, Fev, Mar)
    q1_2026 = ["2026-01", "2026-02", "2026-03"]
    soma_prev = 0.0
    erros_abs = []

    print("--- DETALHAMENTO DO PRIMEIRO TRIMESTRE DE 2026 ---")
    for m in q1_2026:
        idx = meses.index(m)
        real = vendas_reais[idx]
        prev = previsoes[m]
        soma_prev += prev
        erro = abs(real - prev)
        erros_abs.append(erro)
        print(f"Mês: {m} | Venda Real: {real} | Previsão (Média Móvel 3M): {prev:.2f} | Erro Absoluto: {erro:.2f}")

    mae = sum(erros_abs) / len(erros_abs)

    print("\n--- RESPOSTA DA QUESTÃO 6.2 ---")
    print(f"Soma Exata das Previsões: {soma_prev:.2f}")
    print(f"Soma Total Arredondada (Inteiro): {round(soma_prev)}")
    print(f"MAE (Mean Absolute Error): {mae:.2f}")


if __name__ == "__main__":
    calcular_previsao()

