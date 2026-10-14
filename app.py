import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuración de la página
st.set_page_config(page_title="Informe Semanal de Mantenimiento", layout="wide")
st.title("🛠️ Generador de Informe de Mantenimiento")

# 2. Leer los datos desde Google Sheets
@st.cache_data(ttl=600) # Se actualiza cada 10 minutos
def cargar_datos():
    # Reemplazá con el ID de tu Google Sheet
    sheet_id = "1kQ9T08Taj_Le1vWS-wXj-m-5rC-1mrkn77dhRkefuak"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    df = pd.read_csv(url)
    
    # Convertir las columnas de fecha a formato datetime de pandas
    df['Fecha de Solicitud'] = pd.to_datetime(df['Fecha de Solicitud'], errors='coerce')
    df['Fecha de Resolución'] = pd.to_datetime(df['Fecha de Resolución'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    return df

df = cargar_datos()

# 3. Filtros en la barra lateral
st.sidebar.header("Filtros del Informe")

# Selección de fechas (Por defecto los últimos 7 días)
hoy = datetime.now()
hace_una_semana = hoy - timedelta(days=7)

fecha_inicio = st.sidebar.date_input("Fecha de inicio", hace_una_semana)
fecha_fin = st.sidebar.date_input("Fecha de fin", hoy)

# 4. Procesamiento de los datos
# Filtrar por las fechas seleccionadas y solo tareas completadas
mascara_fechas = (df['Fecha de Resolución'].dt.date >= fecha_inicio) & (df['Fecha de Resolución'].dt.date <= fecha_fin)
df_filtrado = df[mascara_fechas]
df_completadas = df_filtrado[df_filtrado['Estado'] == 'Completado']

# 5. Dashboard / Métricas Principales
st.subheader(f"Resumen del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}")

col1, col2, col3 = st.columns(3)
col1.metric("Tareas Completadas", len(df_completadas))
col2.metric("Horas Invertidas", round(df_completadas['Tiempo Invertido (hs)'].sum(), 1))
col3.metric("Tareas Pendientes Generales", len(df[df['Estado'] == 'Pendiente']))

st.divider()

# 6. Tabla para el informe
st.subheader("Detalle de Tareas Realizadas")

# Seleccionar solo las columnas relevantes para la gerencia
columnas_informe = ['Fecha de Resolución', 'Sector / Equipo', 'Descripción de la Falla/Tarea', 'Tiempo Invertido (hs)', 'Materiales Utilizados']
df_informe = df_completadas[columnas_informe].sort_values(by='Fecha de Resolución', ascending=False)

# Formatear la fecha para que se vea más limpia
df_informe['Fecha de Resolución'] = df_informe['Fecha de Resolución'].dt.strftime('%d/%m/%Y')

st.dataframe(df_informe, use_container_width=True, hide_index=True)

# 7. Botón de exportación
csv = df_informe.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar Informe Semanal (CSV)",
    data=csv,
    file_name=f"Informe_Mantenimiento_{hoy.strftime('%Y%m%d')}.csv",
    mime="text/csv",
)
