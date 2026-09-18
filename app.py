import streamlit as st

st.set_page_config(page_title="Controle de Combustível", layout="centered")
st.title("⛽ Controle de Gastos com Combustível")

if 'historico' not in st.session_state:
    st.session_state.historico = []

with st.form("add_abastecimento"):
    valor = st.number_input("Valor pago (R$)", min_value=0.0, format="%.2f")
    km = st.number_input("Quilometragem do odômetro (km)", min_value=0.0, format="%.1f")
    submit = st.form_submit_button("Registrar Abastecimento")

    if submit and valor > 0 and km > 0:
        st.session_state.historico.append({'valor': valor, 'km': km})
        st.success("Abastecimento registrado com sucesso!")

if st.session_state.historico:
    st.subheader("📊 Histórico e Cálculos")
    total_gasto = sum(item['valor'] for item in st.session_state.historico)
    
    if len(st.session_state.historico) > 1:
        primeira_km = st.session_state.historico[0]['km']
        ultima_km = st.session_state.historico[-1]['km']
        km_rodados = ultima_km - primeira_km
        
        if km_rodados > 0:
            custo_km = total_gasto / km_rodados
            st.metric(label="Custo Médio Total (R$/km rodado)", value=f"R$ {custo_km:.2f}")
            st.write(f"Total de km rodados desde o primeiro registro: {km_rodados:.1f} km")
            st.write(f"Valor total gasto: R$ {total_gasto:.2f}")
        else:
            st.info("A quilometragem não mudou. Registre novas distâncias para calcular o custo por km.")
    else:
        st.info("Registre pelo menos dois abastecimentos para calcular o rendimento.")
