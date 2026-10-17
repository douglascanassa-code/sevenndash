import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração da página
st.set_page_config(page_title="Painel de Finanças - Apostas", layout="wide")

st.title("📊 Painel de Controlo de Apostas")
st.write("Gerencie e adicione os seus registos financeiros diretamente por aqui.")

# Função para autenticar e carregar dados via gspread
@st.cache_resource
def get_sheet_connection():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Extrai as credenciais do st.secrets
    creds_dict = dict(st.secrets["gsheets"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ZNxM8HTKiR4OpQ318SqxKhXX54Pt7kZaSvyugub6fxY/edit"
    sheet = client.open_by_url(spreadsheet_url).worksheet("Transações")
    return sheet

try:
    sheet = get_sheet_connection()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
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
        # Nova linha para adicionar diretamente na folha
        nova_linha = [
            str(data_aposta),
            plataforma,
            usuario,
            tipo,
            f"R$ {valor:.2f}".replace(".", ","),
            status,
            observacao
        ]
        
        sheet.append_row(nova_linha)
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
