import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import base64
from io import BytesIO

# Importar módulos personalizados
from utils.database import init_supabase, get_user_transactions, get_financial_goals, add_transaction
from utils.analysis import calculate_financial_metrics, generate_ai_recommendations
from utils.reports import PDFReport, generate_financial_report

# Configuración de la página
st.set_page_config(
    page_title="Asesor Financiero Personal IA",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .premium-feature {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
    }
    .success-alert {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .warning-alert {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar Supabase
@st.cache_resource
def init_supabase_client():
    return init_supabase()

# Funciones principales de la aplicación
def show_dashboard(supabase_client, user_id):
    st.markdown('<div class="main-header">💰 Dashboard Financiero</div>', unsafe_allow_html=True)
    
    # Obtener datos del usuario
    transactions = get_user_transactions(supabase_client, user_id)
    goals = get_financial_goals(supabase_client, user_id)
    
    # Calcular métricas
    metrics = calculate_financial_metrics(transactions)
    
    # Mostrar métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Ingresos Mensuales",
            f"${metrics.get('monthly_income', 0):,.2f}",
            delta=f"+${metrics.get('income_growth', 0):.2f}" if metrics.get('income_growth', 0) > 0 else f"-${abs(metrics.get('income_growth', 0)):.2f}"
        )
    
    with col2:
        st.metric(
            "Gastos Mensuales",
            f"${metrics.get('monthly_expenses', 0):,.2f}",
            delta=f"+${metrics.get('expense_growth', 0):.2f}" if metrics.get('expense_growth', 0) > 0 else f"-${abs(metrics.get('expense_growth', 0)):.2f}",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Ahorro Neto",
            f"${metrics.get('net_savings', 0):,.2f}",
            delta=f"{metrics.get('savings_rate', 0):.1f}%"
        )
    
    with col4:
        health_trend = metrics.get('health_trend', '')
        delta_value = None
        if health_trend:
            try:
                delta_value = f"{health_trend}"
            except:
                delta_value = health_trend
        st.metric(
            "Salud Financiera",
            metrics.get('financial_health', 'N/A'),
            delta=delta_value
        )
    
    # Gráficos y análisis
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de gastos por categoría
        if metrics.get('expenses_by_category'):
            fig_expenses = px.pie(
                values=list(metrics['expenses_by_category'].values()),
                names=list(metrics['expenses_by_category'].keys()),
                title="Distribución de Gastos por Categoría"
            )
            st.plotly_chart(fig_expenses, use_container_width=True)
        else:
            st.info("No hay datos de gastos para mostrar")
    
    with col2:
        # Tendencias mensuales
        if metrics.get('monthly_trends'):
            fig_trend = px.line(
                x=list(metrics['monthly_trends'].keys()),
                y=list(metrics['monthly_trends'].values()),
                title="Tendencia de Ahorro Mensual",
                labels={'x': 'Mes', 'y': 'Ahorro ($)'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No hay datos de tendencias para mostrar")
    
    # Recomendaciones IA
    st.subheader("🤖 Recomendaciones de IA")
    recommendations = generate_ai_recommendations(metrics, goals)
    
    if recommendations:
        for i, rec in enumerate(recommendations[:3]):
            with st.expander(f"💡 Recomendación {i+1}: {rec['title']}"):
                st.write(rec['description'])
                if rec.get('action'):
                    if st.button(f"Implementar: {rec['action']}", key=f"action_{i}"):
                        st.success(f"Acción '{rec['action']}' implementada")
    else:
        st.info("No hay recomendaciones disponibles en este momento")

def show_transactions(supabase_client, user_id):
    st.title("💳 Gestión de Transacciones")
    
    # Formulario para agregar transacción
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.selectbox(
                "Tipo de Transacción",
                ["income", "expense"],
                format_func=lambda x: "Ingreso" if x == "income" else "Gasto"
            )
            amount = st.number_input("Monto", min_value=0.01, step=0.01, format="%.2f")
            category = st.selectbox(
                "Categoría",
                ["Alimentación", "Transporte", "Vivienda", "Entretenimiento", "Salud", 
                 "Educación", "Ropa", "Tecnología", "Otros", "Salario", "Inversiones"]
            )
        
        with col2:
            description = st.text_input("Descripción")
            date = st.date_input("Fecha", datetime.now())
            tags = st.text_input("Etiquetas (separadas por coma)")
        
        submitted = st.form_submit_button("Agregar Transacción")
        
        if submitted:
            try:
                transaction_data = {
                    "user_id": user_id,
                    "amount": float(amount),
                    "description": description,
                    "category": category,
                    "transaction_type": transaction_type,
                    "date": date.isoformat(),
                    "tags": tags
                }
                result = add_transaction(supabase_client, transaction_data)
                if result:
                    st.success("✅ Transacción agregada exitosamente!")
                else:
                    st.error("❌ Error al agregar transacción")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Mostrar transacciones recientes
    st.subheader("Historial de Transacciones")
    transactions = get_user_transactions(supabase_client, user_id)
    
    if transactions:
        df = pd.DataFrame(transactions)
        # Asegurarse de que las columnas necesarias existan
        available_columns = ['date', 'description', 'category', 'amount', 'transaction_type']
        display_columns = [col for col in available_columns if col in df.columns]
        
        if display_columns:
            st.dataframe(df[display_columns], use_container_width=True)
        else:
            st.warning("No hay columnas válidas para mostrar")
            
        # Mostrar estadísticas básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            total_income = df[df['transaction_type'] == 'income']['amount'].sum() if 'amount' in df.columns else 0
            st.metric("Total Ingresos", f"${total_income:,.2f}")
        with col2:
            total_expenses = df[df['transaction_type'] == 'expense']['amount'].sum() if 'amount' in df.columns else 0
            st.metric("Total Gastos", f"${total_expenses:,.2f}")
        with col3:
            net_savings = total_income - total_expenses
            st.metric("Ahorro Neto", f"${net_savings:,.2f}")
    else:
        st.info("No hay transacciones registradas. Agrega tu primera transacción.")

def show_financial_goals(supabase_client, user_id):
    st.title("🎯 Metas Financieras")
    
    # Formulario para crear meta
    with st.form("goal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Título de la Meta")
            target_amount = st.number_input("Monto Objetivo", min_value=0.01, step=0.01, format="%.2f")
            category = st.selectbox(
                "Categoría de la Meta",
                ["Ahorro Emergencia", "Vacaciones", "Automóvil", "Casa", "Educación", 
                 "Inversiones", "Retiro", "Otros"]
            )
        
        with col2:
            deadline = st.date_input("Fecha Límite", min_value=datetime.now().date())
            current_amount = st.number_input("Monto Actual", min_value=0.0, step=0.01, format="%.2f")
            priority = st.select_slider("Prioridad", options=["Baja", "Media", "Alta"])
        
        submitted = st.form_submit_button("Crear Meta")
        
        if submitted:
            try:
                # Para demostración, mostramos un mensaje ya que no tenemos la tabla en BD
                st.success("✅ Meta creada exitosamente (modo demostración)")
                st.info("En una implementación completa, esto se guardaría en la base de datos")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Mostrar metas existentes
    goals = get_financial_goals(supabase_client, user_id)
    
    if goals:
        for goal in goals:
            # Usar nombres de campos consistentes
            target = goal.get('target_amount') or goal.get('monto_objetivo', 1)
            current = goal.get('current_amount') or goal.get('monto_actual', 0)
            progress = (current / target) * 100 if target > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                goal_title = goal.get('title') or goal.get('titulo', 'Meta sin título')
                st.subheader(goal_title)
                st.progress(progress / 100)
                st.write(f"**Progreso:** ${current:,.2f} / ${target:,.2f} ({progress:.1f}%)")
                
                goal_category = goal.get('category') or goal.get('categoria', 'Sin categoría')
                goal_priority = goal.get('priority') or goal.get('prioridad', 'Media')
                goal_deadline = goal.get('deadline') or goal.get('fecha_limite', 'No definida')
                
                st.write(f"**Categoría:** {goal_category} | **Prioridad:** {goal_priority}")
                st.write(f"**Fecha límite:** {goal_deadline}")
            
            with col2:
                # Actualizar progreso (solo demostración)
                new_amount = st.number_input(
                    "Actualizar monto",
                    min_value=0.0,
                    value=float(current),
                    key=f"update_{goal.get('id', 'unknown')}"
                )
                if st.button("Actualizar", key=f"btn_{goal.get('id', 'unknown')}"):
                    st.success("Monto actualizado (modo demostración)")
                    st.experimental_rerun()
            
            st.divider()
    else:
        st.info("No tienes metas financieras configuradas. ¡Crea tu primera meta!")

def show_ai_analysis(supabase_client, user_id):
    st.title("📈 Análisis con IA")
    
    # Obtener datos para análisis
    transactions = get_user_transactions(supabase_client, user_id)
    goals = get_financial_goals(supabase_client, user_id)
    
    if not transactions:
        st.warning("Necesitas agregar transacciones para generar análisis.")
        return
    
    # Métricas avanzadas
    metrics = calculate_financial_metrics(transactions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Análisis de patrones de gasto
        st.subheader("🔍 Patrones de Gastos")
        
        if metrics.get('spending_patterns'):
            for pattern in metrics['spending_patterns']:
                st.write(f"• {pattern}")
        else:
            st.info("No se detectaron patrones específicos")
        
        # Alertas inteligentes
        st.subheader("🚨 Alertas Inteligentes")
        if metrics.get('alerts'):
            for alert in metrics['alerts']:
                if alert['severity'] == 'high':
                    st.error(f"⚠️ {alert['message']}")
                elif alert['severity'] == 'medium':
                    st.warning(f"🔶 {alert['message']}")
                else:
                    st.info(f"ℹ️ {alert['message']}")
        else:
            st.success("✅ No hay alertas críticas")
    
    with col2:
        # Recomendaciones personalizadas
        st.subheader("💡 Recomendaciones Personalizadas")
        recommendations = generate_ai_recommendations(metrics, goals)
        
        if recommendations:
            for rec in recommendations:
                emoji = "💰" if rec['type'] == 'savings' else "📊" if rec['type'] == 'investment' else "🎯"
                st.write(f"{emoji} **{rec['title']}**")
                st.write(rec['description'])
                st.divider()
        else:
            st.info("No hay recomendaciones disponibles")
    
    # Análisis predictivo
    st.subheader("🔮 Análisis Predictivo")
    
    if st.button("Generar Proyección Financiera"):
        with st.spinner("Generando proyección con IA..."):
            # Simular análisis predictivo
            future_months = 6
            projection_data = {
                'Meses': [f'Mes {i+1}' for i in range(future_months)],
                'Ahorro Proyectado': np.random.normal(metrics.get('net_savings', 500), 100, future_months).cumsum(),
                'Ingresos Proyectados': np.random.normal(metrics.get('monthly_income', 2000), 200, future_months),
                'Gastos Proyectados': np.random.normal(metrics.get('monthly_expenses', 1500), 150, future_months)
            }
            
            df_projection = pd.DataFrame(projection_data)
            
            fig = px.line(df_projection, x='Meses', y=['Ahorro Proyectado', 'Ingresos Proyectados', 'Gastos Proyectados'],
                         title="Proyección Financiera - Próximos 6 Meses")
            st.plotly_chart(fig, use_container_width=True)

def show_reports(supabase_client, user_id):
    st.title("📊 Reportes y Exportación")
    
    # Generar reporte financiero
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Reporte Mensual")
        
        report_month = st.selectbox(
            "Seleccionar Mes",
            options=["Enero 2024", "Febrero 2024", "Marzo 2024", "Abril 2024"]
        )
        
        if st.button("📈 Generar Reporte Detallado"):
            transactions = get_user_transactions(supabase_client, user_id)
            goals = get_financial_goals(supabase_client, user_id)
            metrics = calculate_financial_metrics(transactions)
            
            # Mostrar resumen
            st.subheader("Resumen Ejecutivo")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ingresos Totales", f"${metrics.get('monthly_income', 0):,.2f}")
            with col2:
                st.metric("Gastos Totales", f"${metrics.get('monthly_expenses', 0):,.2f}")
            with col3:
                st.metric("Tasa de Ahorro", f"{metrics.get('savings_rate', 0):.1f}%")
            
            # Mostrar recomendaciones
            st.subheader("Recomendaciones Principales")
            recommendations = generate_ai_recommendations(metrics, goals)
            for rec in recommendations[:2]:
                st.write(f"**{rec['title']}**")
                st.write(rec['description'])
                st.divider()
    
    with col2:
        st.subheader("Exportar Datos")
        
        export_format = st.radio(
            "Formato de Exportación",
            ["PDF", "CSV", "Excel"]
        )
        
        if st.button("📤 Exportar Datos"):
            transactions = get_user_transactions(supabase_client, user_id)
            
            if not transactions:
                st.warning("No hay datos para exportar")
                return
                
            if export_format == "PDF":
                try:
                    pdf = generate_financial_report(user_id, transactions)
                    pdf_output = BytesIO()
                    pdf.output(pdf_output)
                    pdf_bytes = pdf_output.getvalue()
                    
                    b64 = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="reporte_financiero.pdf">Descargar Reporte PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("✅ PDF generado correctamente")
                except Exception as e:
                    st.error(f"❌ Error generando PDF: {e}")
            
            elif export_format == "CSV":
                try:
                    df = pd.DataFrame(transactions)
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="transacciones.csv">Descargar CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("✅ CSV generado correctamente")
                except Exception as e:
                    st.error(f"❌ Error generando CSV: {e}")
            
            elif export_format == "Excel":
                try:
                    df = pd.DataFrame(transactions)
                    excel_buffer = BytesIO()
                    df.to_excel(excel_buffer, index=False)
                    excel_bytes = excel_buffer.getvalue()
                    b64 = base64.b64encode(excel_bytes).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="transacciones.xlsx">Descargar Excel</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("✅ Excel generado correctamente")
                except Exception as e:
                    st.error(f"❌ Error generando Excel: {e}")

def show_settings(supabase_client, user_id):
    st.title("⚙️ Configuración")
    
    # Configuración de perfil
    st.subheader("👤 Perfil de Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nombre", value="Usuario Demo")
        st.text_input("Email", value="usuario@demo.com")
        st.selectbox("Moneda Principal", ["USD", "EUR", "MXN", "COP"])
    
    with col2:
        st.selectbox("Idioma", ["Español", "English"])
        st.selectbox("Formato de Fecha", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        st.number_input("Meta de Ahorro Mensual", min_value=0, value=500)
    
    # Configuración de notificaciones
    st.subheader("🔔 Notificaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Alertas de gastos excesivos", value=True)
        st.checkbox("Recordatorios de metas", value=True)
        st.checkbox("Resumen semanal", value=True)
    
    with col2:
        st.checkbox("Noticias financieras", value=False)
        st.checkbox("Ofertas de inversión", value=False)
        st.checkbox("Actualizaciones de la app", value=True)
    
    if st.button("💾 Guardar Configuración"):
        st.success("Configuración guardada exitosamente!")

# Aplicación principal
def main():
    load_css()
    
    # Inicializar cliente Supabase
    supabase_client = init_supabase_client()
    
    # Configuración de usuario (en producción usar autenticación)
    user_id = "user_demo_123"
    user_tier = "Premium"
    
    # Sidebar
    st.sidebar.title("💰 Asesor Financiero IA")
    st.sidebar.markdown("---")
    
    # Menú de navegación
    menu_options = [
        "📊 Dashboard",
        "💳 Transacciones", 
        "🎯 Metas Financieras",
        "🤖 Análisis IA",
        "📊 Reportes",
        "⚙️ Configuración"
    ]
    
    selected_menu = st.sidebar.selectbox("Navegación", menu_options)
    
    # Información del usuario en sidebar
    st.sidebar.markdown("---")
    st.sidebar.info(f"👤 Usuario: {user_id}")
    st.sidebar.info(f"💎 Plan: {user_tier}")
    
    # Mostrar página seleccionada
    if selected_menu == "📊 Dashboard":
        show_dashboard(supabase_client, user_id)
    elif selected_menu == "💳 Transacciones":
        show_transactions(supabase_client, user_id)
    elif selected_menu == "🎯 Metas Financieras":
        show_financial_goals(supabase_client, user_id)
    elif selected_menu == "🤖 Análisis IA":
        show_ai_analysis(supabase_client, user_id)
    elif selected_menu == "📊 Reportes":
        show_reports(supabase_client, user_id)
    elif selected_menu == "⚙️ Configuración":
        show_settings(supabase_client, user_id)

if __name__ == "__main__":
    main()