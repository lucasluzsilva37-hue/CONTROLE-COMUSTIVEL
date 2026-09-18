import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Dashboard de Combustível", layout="wide")
st.title("⛽ Dashboard de Controle de Combustível")

if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=['data', 'valor', 'preco_litro', 'km', 'litros'])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Registrar Abastecimento")
    with st.form("add_abastecimento"):
        data = st.date_input("Data do abastecimento", datetime.date.today())
        valor = st.number_input("Valor total pago (R$)", min_value=0.0, format="%.2f")
        preco_litro = st.number_input("Preço por litro (R$)", min_value=0.0, format="%.3f")
        km = st.number_input("Quilometragem (km)", min_value=0.0, format="%.1f")
        submit = st.form_submit_button("Registrar")

        if submit and valor > 0 and preco_litro > 0 and km > 0:
            litros = valor / preco_litro
            novo_registro = pd.DataFrame({'data': [data], 'valor': [valor], 'preco_litro': [preco_litro], 'km': [km], 'litros': [litros]})
            st.session_state.historico = pd.concat([st.session_state.historico, novo_registro], ignore_index=True)
            st.success("Abastecimento registrado!")

with col2:
    st.subheader("Métricas e Histórico")
    if not st.session_state.historico.empty:
        total_gasto = st.session_state.historico['valor'].sum()
        total_litros = st.session_state.historico['litros'].sum()
        
        primeira_km = st.session_state.historico['km'].min()
        ultima_km = st.session_state.historico['km'].max()
        km_rodados = ultima_km - primeira_km
        
        custo_km = total_gasto / km_rodados if km_rodados > 0 else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Custo Médio (R$/km)", f"R$ {custo_km:.2f}")
        m2.metric("Total Gasto", f"R$ {total_gasto:.2f}")
        m3.metric("Total Litros", f"{total_litros:.2f} L")

        st.write("### Histórico Recente")
        st.dataframe(st.session_state.historico.tail())

        st.subheader("📊 Gráfico de Gastos")
        df_plot = st.session_state.historico.copy()
        df_plot['data'] = pd.to_datetime(df_plot['data'])
        df_mensal = df_plot.set_index('data').resample('M')['valor'].sum().reset_index()
        df_mensal['data'] = df_mensal['data'].dt.strftime('%B/%Y')
        
        st.bar_chart(df_mensal.set_index('data')['valor'])
    else:
        st.info("Nenhum dado registrado ainda.")
