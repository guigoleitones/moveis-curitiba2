import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="🏠 Imóveis Curitiba", layout="wide", initial_sidebar_state="expanded")

# CSS customizado
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    h1 {color: #2c3e50; text-align: center;}
    h2 {color: #34495e;}
    .imovel-card {background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
    .preco {color: #27ae60; font-size: 24px; font-weight: bold;}
    .bairro {color: #e74c3c; font-weight: bold;}
    .site {background: #3498db; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px;}
    .data {color: #7f8c8d; font-size: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Imóveis em Curitiba")
st.write("Encontre os melhores imóveis para alugar em Curitiba - Atualizados 3x por dia")

# URL da planilha
url = "https://docs.google.com/spreadsheets/d/1HZ11ayBVI8K-cpRBNDgS8Mf6J3pjwDGQgnwWkweHLxw/export?format=csv"

try:
    df = pd.read_csv(url)
    df['Data Coletado'] = pd.to_datetime(df['Data Coletado'], format='%d/%m/%Y', errors='coerce')
    df = df.sort_values('Data Coletado', ascending=False)
    
    # ===== FILTROS =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        bairro_filter = st.selectbox("📍 Bairro", ["Todos"] + sorted(df["Bairro"].unique().tolist()))
    
    with col2:
        site_filter = st.selectbox("🏢 Site", ["Todos"] + sorted(df["Site"].unique().tolist()))
    
    with col3:
        preco_min = st.number_input("💰 Preço mínimo (R$)", value=0, step=100)
    
    with col4:
        preco_max = st.number_input("💰 Preço máximo (R$)", value=10000, step=100)
    
    # ===== PROCESSAR PREÇOS =====
    df['Preco_Num'] = df['Preço'].str.replace('R$ ', '').str.replace('.', '').astype(float)
    
    # ===== APLICAR FILTROS =====
    df_filtrado = df.copy()
    
    if bairro_filter != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Bairro"] == bairro_filter]
    
    if site_filter != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Site"] == site_filter]
    
    df_filtrado = df_filtrado[(df_filtrado['Preco_Num'] >= preco_min) & (df_filtrado['Preco_Num'] <= preco_max)]
    
    # ===== ESTATÍSTICAS =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de imóveis", len(df_filtrado))
    
    with col2:
        st.metric("💰 Preço médio", f"R$ {df_filtrado['Preco_Num'].mean():.0f}")
    
    with col3:
        st.metric("📍 Bairros", df_filtrado["Bairro"].nunique())
    
    with col4:
        st.metric("🏢 Sites", df_filtrado["Site"].nunique())
    
    st.divider()
    
    # ===== MOSTRAR IMÓVEIS =====
    if len(df_filtrado) > 0:
        for idx, row in df_filtrado.iterrows():
            st.markdown(f"""
            <div class="imovel-card">
                <h3>{row['Título']}</h3>
                <p><span class="preco">{row['Preço']}</span> | <span class="bairro">{row['Bairro']}</span> | <span class="site">{row['Site']}</span> | <span class="data">{row['Data Coletado'].strftime('%d/%m/%Y')}</span></p>
                <p><strong>Descrição:</strong> {row['Descrição']}</p>
                <a href="{row['Link']}" target="_blank" style="background: #3498db; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none;">🔗 Ver anúncio</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ Nenhum imóvel encontrado com esses filtros.")
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("Aguarde alguns segundos e recarregue a página.")
