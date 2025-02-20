import streamlit as st
import pandas as pd
import altair as alt
import os

# Configuración de la aplicación
st.title("📊 Gráfico de Presión Arterial")

# Ruta del archivo CSV
csv_path = os.path.join(os.path.dirname(__file__), "../data/jc_pressure.csv")

# Cargar datos con caché para mejorar rendimiento
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

df = load_data()

if df is not None:
    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    # Verificar que las columnas necesarias existen
    required_columns = {"Time", "Systolic", "Diastolic"}
    if required_columns.issubset(df.columns):
        # Convertir columna de tiempo a datetime si es necesario
        if not pd.api.types.is_datetime64_any_dtype(df["Time"]):
            df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

        # Transformar datos para Altair
        df_melted = df.melt(id_vars=["Time"], value_vars=["Systolic", "Diastolic"],
                            var_name="Type", value_name="Pressure")

        # Crear gráfico interactivo
        chart = (
            alt.Chart(df_melted)
            .mark_line(point=True)  # Línea con puntos
            .encode(
                x="Time:T",
                y="Pressure:Q",
                color="Type:N",  # Diferenciar Systolic y Diastolic
                tooltip=["Time", "Type", "Pressure"]
            )
            .interactive()
        )

        # Mostrar gráfico
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning(f"El archivo debe contener las columnas {required_columns}.")
else:
    st.error("No se pudieron cargar los datos.")
