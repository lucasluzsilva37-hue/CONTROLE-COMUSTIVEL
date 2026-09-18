import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Dashboard de Combustível", layout="wide")
st.title("⛽ Dashboard de Controle de Combustível")

if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame({
        'data': pd.Series(dtype='object'),
        'valor': pd.Series(dtype='float64'),
        'preco_litro': pd.Series(dtype='float64'),
        'km': pd.Series(dtype='float64'),
        'litros': pd.Series(dtype='float64')
    })

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Registrar Abastecimento")
    with st.form("add_abastecimento", clear_on_submit=True):
        data = st.date_input("Data do abastecimento", datetime.date.today())
        valor = st.number_input("Valor total pago (R$)", min_value=0.0, format="%.2f")
        preco_litro = st.number_input("Preço por litro (R$)", min_value=0.0, format="%.3f")
        km = st.number_input("Quilometragem (km)", min_value=0.0, format="%.1f")
        submit = st.form_submit_button("Registrar")

        if submit and valor > 0 and preco_litro > 0 and km > 0:
            litros = valor / preco_litro
            novo_registro = pd.DataFrame({
                'data': [pd.to_datetime(data).date()],
                'valor': [float(valor)],
                'preco_litro': [float(preco_litro)],
                'km': [float(km)],
                'litros': [float(litros)]
            })
            st.session_state.historico = pd.concat([st.session_state.historico, novo_registro], ignore_index=True)
            st.success("Abastecimento registrado com sucesso!")
            st.rerun()

with col2:
    st.subheader("Métricas e Histórico")
    if not st.session_state.historico.empty:
        df_calc = st.session_state.historico.copy()
        df_calc['valor'] = pd.to_numeric(df_calc['valor'], errors='coerce').fillna(0.0)
        df_calc['litros'] = pd.to_numeric(df_calc['litros'], errors='coerce').fillna(0.0)
        df_calc['km'] = pd.to_numeric(df_calc['km'], errors='coerce').fillna(0.0)

        total_gasto = df_calc['valor'].sum()
        total_litros = df_calc['litros'].sum()
        
        primeira_km = df_calc['km'].min()
        ultima_km = df_calc['km'].max()
        km_rodados = ultima_km - primeira_km
        
        custo_km = total_gasto / km_rodados if km_rodados > 0 else 0.0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Custo Médio", f"R$ {custo_km:.2f}/km")
        m2.metric("Total Gasto", f"R$ {total_gasto:.2f}")
        m3.metric("Total Litros", f"{total_litros:.2f} L")

        st.write("### Histórico e Edição")
        st.caption("Marque a caixa de seleção à esquerda de uma linha e pressione a tecla Delete para remover.")
        
        dados_editados = st.data_editor(
            st.session_state.historico,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
                "preco_litro": st.column_config.NumberColumn("Preço/Litro (R$)", format="R$ %.3f"),
                "km": st.column_config.NumberColumn("KM Atual", format="%.1f km"),
                "litros": st.column_config.NumberColumn("Litros Abastecidos", format="%.2f L"),
            }
        )
        
        st.session_state.historico = dados_editados.dropna(how='all')

        st.subheader("📊 Gastos Mensais")
        df_grafico = st.session_state.historico.copy()
        df_grafico['data_dt'] = pd.to_datetime(df_grafico['data'], errors='coerce')
        df_grafico = df_grafico.dropna(subset=['data_dt'])

        if not df_grafico.empty:
            df_grafico['periodo'] = df_grafico['data_dt'].dt.to_period('M')
            df_mensal = df_grafico.groupby('periodo')['valor'].sum().reset_index().sort_values('periodo')
            df_mensal['mes_ano'] = df_mensal['periodo'].dt.strftime('%m/%Y')
            
            st.bar_chart(data=df_mensal.set_index('mes_ano')['valor'], use_container_width=True)
    else:
        st.info("Nenhum abastecimento registrado até o momento.")
