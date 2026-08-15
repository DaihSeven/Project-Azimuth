from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="LH Nautical - Dashboard", layout="wide")
st.title("⚓ LH Nautical — Painel Analítico de Vendas")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "1-lh_nautical_csv"

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    order_items = pd.read_csv(DATA_DIR / "order_items.csv")
    product_variants = pd.read_csv(DATA_DIR / "product_variants.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    categories = pd.read_csv(DATA_DIR / "categories.csv")

    df = order_items.merge(orders, left_on="order_id", right_on="id", suffixes=('_item', '_order'))
    df = df.merge(product_variants, left_on="product_variant_id", right_on="id")
    df = df.merge(products, left_on="product_id", right_on="id")
    df = df.merge(categories, left_on="category_id", right_on="id", suffixes=('_prod', '_cat'))

    df['placed_at'] = pd.to_datetime(df['placed_at'])
    df['channel_clean'] = df['channel'].astype(str).str.upper()
    
    return df

df = load_data()

# BLOCO 1: VISÃO GERAL
st.markdown("### 🟢 Visão Geral")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.write("") 
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    faturamento = df['line_total'].sum()
    total_pedidos = df['order_id'].nunique()
    ticket_medio = faturamento / total_pedidos if total_pedidos > 0 else 0

    col_kpi1.metric("Faturamento Total", f"R$ {faturamento/1e6:.2f}M")
    col_kpi2.metric("Total de Pedidos", f"{total_pedidos:,}")
    col_kpi3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

with col_right:
    fig_channel = px.pie(
        df, 
        names='channel_clean', 
        values='line_total', 
        hole=0.45,
        title="Distribuição de Vendas por Canal",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_channel.update_traces(textinfo='percent+label')
    fig_channel.update_layout(height=260, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_channel, use_container_width=True)

st.divider()

# BLOCO 2: CATEGORIAS (RANKING)
st.markdown("### 🟡 Ranking de Categorias por Faturamento")

cat_df = df.groupby('name_cat')['line_total'].sum().reset_index()
cat_df = cat_df.sort_values(by='line_total', ascending=True)

fig_cat = px.bar(
    cat_df, 
    x='line_total', 
    y='name_cat', 
    orientation='h',
    text_auto='.2s',
    title="Faturamento por Categoria (Hélices no Topo)",
    labels={'line_total': 'Faturamento (R$)', 'name_cat': 'Categoria'},
    color_discrete_sequence=['#1f77b4']
)
fig_cat.update_layout(height=480, margin=dict(t=40, b=20, l=20, r=20))
st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# BLOCO 3: TEMPORAL & POS
st.markdown("### 🔴 Análise Temporal & Loja Física (POS)")

col_a, col_b = st.columns(2)

with col_a:
    df['ano_mes'] = df['placed_at'].dt.to_period('M').astype(str)
    saz_df = df.groupby('ano_mes')['line_total'].sum().reset_index()

    fig_saz = px.line(
        saz_df, 
        x='ano_mes', 
        y='line_total', 
        markers=True,
        title="Sazonalidade Mensal de Vendas",
        labels={'ano_mes': 'Ano-Mês', 'line_total': 'Faturamento (R$)'}
    )
    fig_saz.update_layout(height=380)
    st.plotly_chart(fig_saz, use_container_width=True)

with col_b:
    df_pos = df[df['channel_clean'] == 'POS'].copy()
   
    mapa_dias = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    df_pos['dia_semana_en'] = df_pos['placed_at'].dt.day_name()
    df_pos['dia_semana'] = df_pos['dia_semana_en'].map(mapa_dias)
    
    ordem_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    pos_df = df_pos.groupby('dia_semana')['line_total'].sum().reindex(ordem_pt).reset_index()

    fig_pos = px.bar(
        pos_df, 
        x='dia_semana', 
        y='line_total',
        text_auto='.2s',
        title="Vendas por Dia da Semana — Loja Física (POS)",
        labels={'dia_semana': 'Dia da Semana', 'line_total': 'Faturamento (R$)'},
        color_discrete_sequence=['#ef553b']
    )
    fig_pos.update_layout(height=380)
    st.plotly_chart(fig_pos, use_container_width=True)