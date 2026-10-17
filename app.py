import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Painel de Finanças - Apostas", layout="wide")

st.title("📊 Painel de Controlo de Apostas")
st.write("Gerencie e adicione os seus registos financeiros diretamente por aqui.")

# Criar a ligação segura ao Google Sheets via Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Ler os dados da folha (ajuste o worksheet para a aba correta, ex: 'Transacoes' ou 'Operacoes')
try:
    # A leitura usa a autenticação segura configurada nos Secrets
    df = conn.read(worksheet="Transações", ttl="0m")
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()

# Formulário de Cadastro na Barra Lateral
st.sidebar.header("➕ Novo Registo")
with st.sidebar.form("form_cadastro"):
    data_aposta = st.date_input("Data")
    plataforma = st.text_input("Plataforma (ex: Bet365, Blaze)")
    usuario = st.text_input("Usuário / Conta")
    tipo = st.selectbox("Tipo", ["Depósito", "Saque", "Aposta", "Bônus"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    status = st.selectbox("Status", ["Concluído", "Pendente", "Cancelado"])
    observacao = st.text_area("Observação")
    
    submit_button = st.form_submit_button(label="Registar na Planilha")

if submit_button:
    try:
        # Novo registo formatado
        novo_registo = pd.DataFrame([{
            "Data": str(data_aposta),
            "Plataforma": plataforma,
            "Usuário/Conta": usuario,
            "Tipo": tipo,
            "Valor (R$)": f"R$ {valor:.2f}".replace(".", ","),
            "Status": status,
            "Observação": observacao
        }]
        )
        
        # Concatenar com os dados existentes
        updated_df = pd.concat([df, novo_registo], ignore_index=True)
        
        # Atualizar a planilha no Google Sheets
        conn.update(worksheet="Transações", data=updated_df)
        st.sidebar.success("Registo adicionado com sucesso à planilha!")
        st.rerun()
    except Exception as err:
        st.sidebar.error(f"Erro ao gravar dados: {err}")

# Exibir os dados na aplicação
if not df.empty:
    st.subheader("Registo de Transações")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Resumo Geral")
    st.metric(label="Total de Registos", value=len(df))
else:
    st.info("A tabela está vazia ou a aguardar dados.")
