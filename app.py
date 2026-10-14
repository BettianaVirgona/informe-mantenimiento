import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# Nota: Para crear Google Docs por API se usa gspread o la API oficial de Google Docs. 
# Abajo te dejo la estructura y la lógica de redacción inteligente que se inyecta en el documento.

def obtener_datos_mantenimiento():
    # ID de tu Hoja de Cálculo actual
    sheet_id = "1kQ9T08Taj_Le1vWS-wXj-m-5rC-1mrkn77dhRkefuak"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    df = pd.read_csv(url)
    return df

def procesar_informe_semanal():
    df = obtener_datos_mantenimiento()
    
    # Limpieza y conversión de fechas (adaptado a tus columnas actuales)
    df['Fecha de Solicitud'] = pd.to_datetime(df['Fecha de Solicitud'], errors='coerce')
    df['Fecha de Resolución'] = pd.to_datetime(df['Fecha de Resolución'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Filtrar última semana (últimos 7 días)
    hoy = datetime.now()
    hace_una_semana = hoy - timedelta(days=7)
    
    mask = (df['Fecha de Resolución'] >= hace_una_semana) & (df['Estado'] == 'Completado')
    df_semana = df[mask]
    
    # Métricas clave para el resumen ejecutivo
    total_tareas = len(df_semana)
    total_horas = df_semana['Tiempo Invertido (hs)'].sum()
    sectores_atendidos = df_semana['Sector / Equipo'].unique().tolist()
    
    # Redacción inteligente simulada (aquí es donde la IA estructura el texto formal)
    resumen_ejecutivo = f"""
    INFORME SEMANAL DE GESTIÓN DE MANTENIMIENTO
    Período: {hace_una_semana.strftime('%d/%m/%Y')} al {hoy.strftime('%d/%m/%Y')}
    
    1. Resumen Operativo:
    Durante el transcurso de la semana, el departamento de mantenimiento ejecutó un total de {total_tareas} intervenciones completadas con éxito, acumulando un tiempo de labor operativo de {total_horas} horas. Las tareas abarcaron de forma prioritaria los sectores de: {', '.join(str(s) for s in sectores_atendidos)}.
    
    2. Análisis de Actividades Críticas:
    Se dio resolución tanto a los pedidos externos solicitados por las distintas áreas como a las tareas menores preventivas programadas, garantizando la continuidad operativa de la planta y minimizando los tiempos de parada de línea.
    
    3. Insumos y Materiales Utilizados:
    Se gestionó el uso eficiente de repuestos y materiales declarados en el registro diario, manteniendo el stock bajo control y optimizando los recursos disponibles.
    """
    
    print(resumen_ejecutivo)
    return df_semana, resumen_ejecutivo

if __name__ == "__main__":
    procesar_informe_semanal()
