
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="App de Crianza de Pollos", layout="wide")
st.title("🐔 App de Crianza de Pollos de Engorde")

# Entrada de parámetros
st.sidebar.header("🔢 Parámetros de Entrada")
machos = st.sidebar.number_input("Cantidad de machos", min_value=0, value=100)
hembras = st.sidebar.number_input("Cantidad de hembras", min_value=0, value=100)
valor_caja = st.sidebar.number_input("Valor por caja ($)", min_value=0, value=195000)
n_cajas = st.sidebar.number_input("Cantidad de cajas", min_value=1, value=2)

# Datos base
total_pollos = machos + hembras
inv_semilla = valor_caja * n_cajas

# Consumo alimento total (gr)
consumo_machos = 502300 * machos / 100
consumo_hembras = 455700 * hembras / 100
consumo_total = consumo_machos + consumo_hembras
bultos_m = consumo_machos / 40000
bultos_h = consumo_hembras / 40000
bultos_total = bultos_m + bultos_h

# Costos por etapa (proyectado)
etapas = ["Preinicio", "Inicio", "Engorde"]
bultos_etapa = [1.06, 4.9, 18]
precios = [95000, 92000, 90000]
costos = [round(b * p, 2) for b, p in zip(bultos_etapa, precios)]
inv_alimentos = sum(costos)
otros_costos = 12000
inv_total = inv_semilla + inv_alimentos + otros_costos

# Pérdidas
muertes_m = int(machos * 0.11)
muertes_h = int(hembras * 0.09)
libra_m = muertes_m * 13.332 / 11
libra_h = muertes_h * 11.86942 / 9
libra_total = libra_m + libra_h

# Ganancia
vendidos = machos + hembras - muertes_m - muertes_h
ventas_estimadas = round((vendidos / 195) * 5376000, 2)
ganancia = ventas_estimadas - inv_total

# Sección: Inversión
st.header("💰 Inversión")
inv_df = pd.DataFrame({
    "Concepto": ["Inv. Semilla", "Inv. Alimentos", "Otros"],
    "Valor ($)": [inv_semilla, inv_alimentos, otros_costos]
})
inv_df.loc[len(inv_df.index)] = ["Total", inv_total]
st.dataframe(inv_df)

# Sección: Consumo total
st.header("🍽️ Consumo Total de Alimento")
col1, col2 = st.columns(2)
col1.metric("Machos (gr)", f"{int(consumo_machos):,}")
col1.metric("Hembras (gr)", f"{int(consumo_hembras):,}")
col2.metric("Bultos Machos", f"{bultos_m:.2f}")
col2.metric("Bultos Hembras", f"{bultos_h:.2f}")
st.metric("Total Bultos", f"{bultos_total:.2f}")

# Tabla de costos por etapa
st.subheader("📦 Costos por Etapa (Proyectado)")
costos_df = pd.DataFrame({
    "Etapa": etapas,
    "Bultos": bultos_etapa,
    "Valor Unitario ($)": precios,
    "Costo Total ($)": costos
})
st.dataframe(costos_df)

# Gráfica inversión vs ventas
st.subheader("📈 Gráfica: Inversión vs Ventas")
fig, ax = plt.subplots()
ax.bar(["Inversión Total", "Ventas Estimadas"], [inv_total, ventas_estimadas], color=["orange", "green"])
st.pyplot(fig)

# Tabla de pérdidas
st.subheader("❌ Pérdidas")
perdidas_df = pd.DataFrame({
    "": ["Muertes", "Lb Aprox", "Alimento Preinicio", "Alimento Inicio", "Alimento Engorde"],
    "Machos": [muertes_m, round(libra_m, 2), 600, 2685, 5220],
    "Hembras": [muertes_h, round(libra_h, 2), 108, 1894, 6616]
})
st.dataframe(perdidas_df)

# Resumen financiero
st.subheader("📊 Resumen Financiero")
resumen_df = pd.DataFrame({
    "Cantidad Vendida": [vendidos],
    "Libras": [905],
    "Ventas Estimadas ($)": [ventas_estimadas],
    "Ganancia Estimada ($)": [ganancia]
})
st.dataframe(resumen_df)

# Exportar resultados
st.subheader("📤 Exportar a Excel")
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    inv_df.to_excel(writer, sheet_name="Inversion", index=False)
    costos_df.to_excel(writer, sheet_name="CostosEtapas", index=False)
    perdidas_df.to_excel(writer, sheet_name="Perdidas", index=False)
    resumen_df.to_excel(writer, sheet_name="ResumenFinanciero", index=False)
st.download_button(
    label="📥 Descargar Excel",
    data=excel_buffer,
    file_name="resumen_pollos_completo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
