import csv
import math
import os

PASTA_CSV = "1-lh_nautical_csv"


def sistema_recomendacao():
    products = {}  
    target_id = None
    target_name_query = "Motor de Popa 1949"

    with open(
        os.path.join(PASTA_CSV, "products.csv"), mode="r", encoding="utf-8-sig"
    ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            p_id = row["id"]
            p_name = row["name"].strip()
            products[p_id] = p_name
            if target_name_query.lower() in p_name.lower():
                target_id = p_id

    variant_to_prod = {}  
    with open(
        os.path.join(PASTA_CSV, "product_variants.csv"),
        mode="r",
        encoding="utf-8-sig",
    ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant_to_prod[row["id"]] = row["product_id"]

    order_to_customer = {}  
    with open(
        os.path.join(PASTA_CSV, "orders.csv"), mode="r", encoding="utf-8-sig"
    ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_to_customer[row["id"]] = row["customer_id"]

    prod_customers = {p_id: set() for p_id in products.keys()}

    with open(
        os.path.join(PASTA_CSV, "order_items.csv"),
        mode="r",
        encoding="utf-8-sig",
    ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            v_id = row["product_variant_id"]
            o_id = row["order_id"]
            p_id = variant_to_prod.get(v_id)
            c_id = order_to_customer.get(o_id)

            if p_id and c_id and p_id in prod_customers:
                prod_customers[p_id].add(c_id)

    if not target_id:
        print(f"Produto '{target_name_query}' não encontrado no catálogo!")
        return

    target_custs = prod_customers[target_id]
    len_target = len(target_custs)

    similaridades = []

    for p_id, custs in prod_customers.items():
        if p_id == target_id:
            continue 

        len_other = len(custs)
        if len_other == 0 or len_target == 0:
            similaridades.append((products[p_id], 0.0))
            continue

        intersecao = len(target_custs.intersection(custs))

        cos_sim = intersecao / (math.sqrt(len_target) * math.sqrt(len_other))
        similaridades.append((products[p_id], cos_sim))

    similaridades.sort(key=lambda x: x[1], reverse=True)

    print(f"=== RECOMENDAÇÕES PARA: {products[target_id]} ===")
    print(f"Total de compradores do item alvo: {len_target}\n")
    print("Top 5 Produtos Mais Similares:")
    for i, (p_name, sim) in enumerate(similaridades[:5], 1):
        print(f"{i}. {p_name} | Similaridade de Cosseno: {sim:.4f}")


if __name__ == "__main__":
    sistema_recomendacao()