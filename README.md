# Project-Azimuth

# ⚓ LH Nautical — Pipeline de Dados, Inteligência Preditiva & Dashboard

Este repositório contém a solução completa para o desafio técnico da **LH Nautical**. O projeto engloba desde a ingestão bruta e modelagem relacional em PostgreSQL (Neon DB), passando por análises exploratórias avançadas, algoritmos preditivos de demanda, motor de recomendação por similaridade e um dashboard interativo hospedado no Render.

---

## 📂 Estrutura do Repositório

```text
Project-Azimuth/
├── 1-lh_nautical_csv/      # 24 arquivos CSV contendo os dados brutos da operação
├── dashboard/              # Dashboard detalhado
│   └── Dashboard - LH Nautical.pdf     # Dashboard em pdf
├── docs/                   # Documentação detalhada e relatórios
│   └── Documentação Técnica do Desafio LH Nautical.pdf     # Documentação completa do projeto
├── er/                     # Entidade e Relacionamento
│   └── lh_autical-2.pdf    # Diagrama Entidade e Relacionamento em pdf
├── python/
│   ├── app.py              # Aplicação Streamlit (Dashboard Interativo)
│   ├── carregar_dados.py   # Script de carga via COPY do PostgreSQL
│   ├── gerar_schema.py     # Gerador de DDL em Python puro
│   ├── previsao_demanda.py # Modelo de Média Móvel (Q6)
│   └── recomendacao.py     # Motor de Recomendação via Cosseno (Q7)
├── sql/
│   ├── schema.sql          # Estrutura DDL gerada para o PostgreSQL
│   ├── shemaDBdiagram.sql  # Estrutura da ER do DBdiagram
├── .env.example            # Modelo de variáveis de ambiente
├── .gitignore              # Proteção contra commit de credenciais
├── requirements.txt        # Dependências da aplicação



```

## 🛠️ Tecnologias Utilizadas
```
Linguagem: Python 3.14

Banco de Dados: PostgreSQL (Neon DB - Serverless Cloud)

Visualização: Streamlit, Plotly Express

Manipulação de Dados: Pandas, NumPy, Psycopg2

Deploy: Render (Web Service)
```

## 🚀 Como Executar o Projeto Localmente

1. Pré-requisitos
```
Python 3.10+ instalado.

Instância do PostgreSQL configurada (ex: Neon DB).
```
2. Passo a Passo

- Clone o repositório:

```
git clone https://github.com/DaihSeven/Project-Azimuth.git
cd Project-Azimuth
```
- Instale as dependências:

```
pip install -r requirements.txt
```
- Configure as Variáveis de Ambiente:

- Crie um arquivo .env na raiz do projeto contendo:

- Snippet de código do .env
```
DATABASE_URL="postgresql://usuario:senha@host/neondb?sslmode=require"
PASTA_CSV="1-lh_nautical_csv"
```
- Gerar Schema e Ingerir os Dados (Opcional se o banco já estiver populado):

```
python python/gerar_schema.py
python python/carregar_dados.py
```
- Executar a Aplicação Web:

```
streamlit run python/app.py
```
## Dashboard 

[Dashboard online](https://project-azimuth.onrender.com/)

[Dashboard pdf](./dashboard/Dashboard%20-%20LH%20Nautical.pdf)

<i>
Curiosidade sobre o nome do projeto Project Azimuth: Azimute é a coordenada usada na navegação astronômica para medir direções. E este projeto significa para uma empresa uma forma de direcionar melhor suas informações, dados e recursos.
</i>