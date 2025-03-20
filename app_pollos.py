
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="App de Crianza de Pollos", layout="wide")

st.title("🐔 App de Crianza de Pollos de Engorde")

# Entradas
st.sidebar.header("🔢 Parámetros de Entrada")
machos = st.sidebar.number_input("Cantidad de machos", min_value=0, value=100)
hembras = st.sidebar.number_input("Cantidad de hembras", min_value=0, value=100)
valor_caja = st.sidebar.number_input("Valor por caja ($)", min_value=0, value=195000)
n_cajas = st.sidebar.number_input("Cantidad de cajas", min_value=1, value=2)

# Cálculos básicos
total_pollos = machos + hembras
inv_semilla = n_cajas * valor_caja
consumo_machos = 502300 * machos / 100
consumo_hembras = 455700 * hembras / 100
consumo_total = consumo_machos + consumo_hembras
bultos_m = consumo_machos / 40000
bultos_h = consumo_hembras / 40000
bultos_total = bultos_m + bultos_h

# Costos por etapa
etapas = ["Preinicio", "Inicio", "Engorde"]
bultos_etapa = [1.06, 4.9, 18]
precios = [95000, 92000, 90000]
costos = [round(b * p, 2) for b, p in zip(bultos_etapa, precios)]

# Inversión total
inv_alimentos = sum(costos)
inv_total = inv_semilla + inv_alimentos + 12000

# Ganancia estimada
muertes = machos * 0.11 + hembras * 0.09
ventas_estimadas = round((machos + hembras - muertes) * 905 / 195 * 5376000 / 100, 2)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Consumo Total")
    st.metric("Consumo Total (gr)", f"{int(consumo_total):,}")
    st.metric("Bultos Totales", f"{bultos_total:.2f}")
    st.metric("Inversión Semilla", f"${inv_semilla:,.0f}")
    st.metric("Inversión Total", f"${inv_total:,.0f}")

with col2:
    st.subheader("💰 Ventas y Ganancia")
    st.metric("Pollos Vendidos Estimados", f"{int(machos + hembras - muertes)}")
    st.metric("Ventas Estimadas", f"${ventas_estimadas:,.0f}")
    st.metric("Ganancia Estimada", f"${ventas_estimadas - inv_total:,.0f}")

# Gráfica de inversión vs ventas
st.subheader("📈 Comparativa de Inversión vs Ventas")
fig, ax = plt.subplots()
labels = ["Inversión", "Ventas"]
valores = [inv_total, ventas_estimadas]
ax.bar(labels, valores, color=["orange", "green"])
st.pyplot(fig)

# Exportar resultados
st.subheader("📤 Exportar Resultados")

df_export = pd.DataFrame({
    "Concepto": ["Cantidad Machos", "Cantidad Hembras", "Consumo Total (gr)", "Bultos Totales",
                 "Inversión Total", "Ventas Estimadas", "Ganancia Estimada"],
    "Valor": [machos, hembras, consumo_total, bultos_total, inv_total, ventas_estimadas,
              ventas_estimadas - inv_total]
})

excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    df_export.to_excel(writer, index=False, sheet_name="Resumen")
st.download_button(
    label="📥 Descargar Excel",
    data=excel_buffer,
    file_name="resumen_pollos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
