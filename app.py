import pandas as pd
from datetime import datetime, timedelta

def generar_informe_mantenimiento():
    # URL pública del Google Sheet para exportar a CSV
    sheet_id = "1kQ9T08Taj_Le1vWS-wXj-m-5rC-1mrkn77dhRkefuak"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    try:
        df = pd.read_csv(url)
    except Exception as e:
        print(f"Error al leer la hoja de cálculo: {e}")
        return
    
    # Normalizar nombres de columnas y fechas
    df['Fecha de Resolución'] = pd.to_datetime(df['Fecha de Resolución'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Filtrar tareas de los últimos 7 días con estado Completado
    hoy = datetime.now()
    hace_una_semana = hoy - timedelta(days=7)
    
    mask = (df['Fecha de Resolución'] >= hace_una_semana) & (df['Estado'] == 'Completado')
    df_semana = df[mask]
    
    total_tareas = len(df_semana)
    total_horas = df_semana['Tiempo Invertido (hs)'].sum() if not df_semana.empty else 0
    sectores = df_semana['Sector / Equipo'].unique().tolist() if not df_semana.empty else []
    
    # Redacción automática del informe ejecutivo
    periodo_str = f"Período: {hace_una_semana.strftime('%d/%m/%Y')} al {hoy.strftime('%d/%m/%Y')}"
    sectores_str = ', '.join(str(s) for s in sectores) if sectores else 'Ninguno'
    
    informe_texto = (
        "INFORME SEMANAL DE GESTIÓN DE MANTENIMIENTO\n"
        f"{periodo_str}\n\n"
        "1. RESUMEN OPERATIVO:\n"
        f"- Total de intervenciones completadas: {total_tareas}\n"
        f"- Tiempo total invertido: {total_horas} horas\n"
        f"- Sectores atendidos: {sectores_str}\n\n"
        "2. DETALLE DE TAREAS EJECUTADAS:"
    )
    
    for index, row in df_semana.iterrows():
        sector = row.get('Sector / Equipo', 'N/A')
        descripcion = row.get('Descripción de la Falla/Tarea', 'N/A')
        horas = row.get('Tiempo Invertido (hs)', 0)
        informe_texto += f"\n- [{sector}] {descripcion} (Horas: {horas})"
    
    informe_texto += (
        "\n\n3. OBSERVACIONES:\n"
        "Se dio cumplimiento al plan de mantenimiento semanal asegurando la disponibilidad operativa de los equipos críticos de planta."
    )
    
    print(informe_texto)
    return informe_texto

if __name__ == "__main__":
    generar_informe_mantenimiento()
