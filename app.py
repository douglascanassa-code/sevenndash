import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Painel de Finanças - Apostas", layout="wide")

st.title("📊 Painel de Controlo de Apostas")
st.write("A carregar os dados financeiros em tempo real a partir do Google Sheets...")

# Criar a ligação ao Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Ler os dados da folha (Certifique-se de que a folha se chama 'Sheet1' ou mude o nome abaixo)
try:
    df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZNxM8HTKiR4OpQ318SqxKhXX54Pt7kZaSvyugub6fxY/edit", worksheet="Sheet1", ttl="10m")
    # Mostrar métricas rápidas ou a tabela na aplicação
    st.success("Dados carregados com sucesso!")
    st.dataframe(df)
    
    # Exemplo básico de métricas (ajuste os nomes das colunas conforme a sua tabela)
    if not df.empty:
        st.subheader("Resumo Geral")
        st.metric(label="Total de Registos", value=len(df))
        
except Exception as e:
    st.error(f"Erro ao ligar ao Google Sheets: {e}")
    st.info("Certifique-se de que partilhou a sua folha do Google Sheets com o email de serviço do Streamlit e configurou os Secrets.")
