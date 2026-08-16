# 📘 Documentação Técnica — Desafio LH Nautical
**Autor:** Equipe de Engenharia e Ciência de Dados  
**Data:** Agosto de 2026  
**Banco de Dados:** PostgreSQL (Neon Cloud)  
**Aplicação Web:** Streamlit hospedado no Render  

---

## 📑 Sumário Executive
A **LH Nautical** é uma varejista do setor náutico que opera lojas físicas (POS), armazéns e e-commerce. Esta documentação detalha a arquitetura do pipeline de dados, a modelagem relacional dos 24 arquivos CSV operacionais, as análises de negócio solicitadas pelos stakeholders (Gabriel Santos, Marina Costa e Sr. Almir), além dos modelos preditivos e de recomendação desenvolvidos.

---

## 1. Análise Exploratória de Dados (EDA) & Validação de Qualidade

### Diagnóstico da Tabela `orders`
* **Volume de Dados:** 48.998 linhas e 13 colunas.
* **Janela Temporal:** 01/01/2020 a 01/01/2027.
* **Métricas Financeiras (`total`):**
  * Valor Mínimo: R$ 32,62
  * Valor Máximo: R$ 127.262,02
  * Valor Médio: R$ 28.704,99

### Diagnóstico de Confiabilidade
* **Outliers:** A elevada variância entre o valor mínimo e máximo decorre da natureza do catálogo náutico, onde itens de alto valor agregado (motores de popa e lanchas) convivem com peças de baixo custo.
* **Valores Nulos:** Chaves primárias e valores de pedidos possuem integridade total (0% nulos). A coluna `salesperson_id` possui ~49,2% de valores nulos, refletindo o comportamento real de compras realizadas via Canal E-commerce (sem vendedor associado).

---

## 2. Engenharia de Dados: Inferência de Schema e Carga no PostgreSQL

### 2.1 Gerador Automático de DDL (`gerar_schema.py`)
Para cumprir a premissa de não utilizar bibliotecas externas (como Pandas ou Polars), foi desenvolvido um algoritmo em Python puro utilizando o pacote nativo `csv`. O script analisa as primeiras 200 linhas de cada um dos 24 arquivos CSV para inferir tipos de dados SQL (`BIGINT`, `NUMERIC`, `TIMESTAMP`, `DATE`, `BOOLEAN`, `VARCHAR`).

### 2.2 Pipeline de Ingestão (`carregar_dados.py`)
A ingestão dos 24 arquivos no PostgreSQL Neon foi performada via comando otimizado `COPY` usando `psycopg2.copy_expert`.

* **Validação de Linhas Carregadas:**
  * `customers`: 2.000 linhas
  * `orders`: 48.998 linhas
  * `order_items`: 147.320 linhas
  * `payments`: 53.546 linhas[cite: 3]
  * **Total Agregado de Teste:** 251.864 linhas[cite: 3]

---

## 3. Análise de Negócios & SQL

### 3.1 Identificação dos Clientes "Elite / Fiéis"
Visando atender à demanda da Gerente de Negócios (Marina Costa)[cite: 3], identificaram-se os clientes com maior Ticket Médio que atendem ao critério restritivo de diversidade de compras (atravessando no mínimo 13 categorias distintas de produtos)[cite: 3].

```sql
WITH metricas_pedidos AS (
    SELECT 
        customer_id, 
        SUM(total) AS faturamento_total, 
        COUNT(id) AS frequencia, 
        SUM(total) / COUNT(id) AS ticket_medio
    FROM orders 
    GROUP BY customer_id
),
diversidade_cliente AS (
    SELECT 
        o.customer_id, 
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
)
SELECT m.customer_id, m.ticket_medio, d.diversidade_categorias
FROM metricas_pedidos m
JOIN diversidade_cliente d ON m.customer_id = d.customer_id
WHERE d.diversidade_categorias >= 13
ORDER BY m.ticket_medio DESC, m.customer_id ASC
LIMIT 10;
3.2 Correção de Viés nas Lojas Físicas via Dimensão de CalendárioPara responder ao Sr. Almir sem distorções causadas por dias de loja aberta com zero vendas, construiu-se uma Dimensão de Datas com generate_series()[cite: 3]. O cálculo foi cruzado via LEFT JOIN preenchendo datas sem registros com 0 através de COALESCE[cite: 3].SQLWITH calendario AS (
    SELECT generate_series(
        (SELECT MIN(created_at::date) FROM orders),
        (SELECT MAX(created_at::date) FROM orders),
        '1 day'::interval
    )::date AS data
),
vendas_diarias AS (
    SELECT created_at::date AS data, SUM(total) AS faturamento_dia
    FROM orders
    WHERE LOWER(channel) = 'pos'
    GROUP BY created_at::date
)
SELECT 
    CASE EXTRACT(DOW FROM c.data)
        WHEN 0 THEN 'Domingo' WHEN 1 THEN 'Segunda-feira' WHEN 2 THEN 'Terça-feira'
        WHEN 3 THEN 'Quarta-feira' WHEN 4 THEN 'Quinta-feira' WHEN 5 THEN 'Sexta-feira' WHEN 6 THEN 'Sábado'
    END AS dia_semana,
    ROUND(AVG(COALESCE(v.faturamento_dia, 0)), 2) AS media_vendas
FROM calendario c
LEFT JOIN vendas_diarias v ON c.data = v.data
GROUP BY EXTRACT(DOW FROM c.data), dia_semana 
ORDER BY media_vendas ASC;
4. Ciência de Dados & Modelagem Preditiva4.1 Previsão de Demanda — "Bússola de Bordo 702"Modelo Utilizado: Média Móvel de 3 Meses (Baseline)[cite: 3].Garantia contra Data Leakage: A previsão para o mês $t$ considera estritamente a média das vendas dos meses $t-3, t-2, t-1$[cite: 3].Resultados (Q1 2026):Previsão Total Acumulada para Q1 2026: 293 unidades (Soma Exata: 292,67)[cite: 3].Erro Médio Absoluto (MAE): 29,22[cite: 3].Diagnóstico Crítico do ModeloO baseline não é adequado para este produto[cite: 3]. O item apresenta sazonalidade de verão acentuada (picos de venda entre Novembro e Janeiro superiores a 120-150 unidades)[cite: 3]. A média móvel gera um efeito de atraso (lag), subestimando gravemente o pico de demanda de Janeiro (previu 80 contra 152 reais), o que causaria rupturas de estoque[cite: 3].4.2 Motor de Recomendação — Item-Based Collaborative FilteringDesenvolvido para criar a vitrine "Quem comprou isso, também levou..." para o item "Motor de Popa 1949"[cite: 3].Metodologia: Matriz de Interação Binária Usuário $\times$ Produto processada por Similaridade de Cosseno:

Similaridade(A, B) = A.BA2B2 = CA CBCA.CB

$$\text{Similaridade}(A, B) = \frac{|C_A \cap C_B|}{\sqrt{|C_A|} \cdot \sqrt{|C_B|}}$$[cite: 3]

Produto Recomendado Top 1: Motor de Popa 5331 (Similaridade de Cosseno: 0,2566)[cite: 3].Limitação Técnica: Vulnerável ao problema de Cold Start (Início Frio), onde produtos recém-lançados ou com baixo histórico de vendas nunca são recomendados devido à esparsidade dos vetores[cite: 3].
---