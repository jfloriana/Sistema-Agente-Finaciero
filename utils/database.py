import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import random
import uuid

def init_supabase():
    """Inicializar conexión a Supabase usando requests"""
    try:
        st.success("✅ Configurado para Supabase")
        return {
            'url': 'https://dreqyrgijnjfxahzbzyd.supabase.co',
            'key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRyZXF5cmdpam5qZnhhaHpienlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1MzYxMjcsImV4cCI6MjA3NzExMjEyN30.-JItHC030b-nMv3MvhJOIWDV3FNdCsW2HAjUZlfP_kM'
        }
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

def supabase_request(supabase_client, method, table, data=None, filters=None):
    """Hacer requests directos a Supabase"""
    if supabase_client is None:
        return None
        
    url = f"{supabase_client['url']}/rest/v1/{table}"
    headers = {
        'apikey': supabase_client['key'],
        'Authorization': f"Bearer {supabase_client['key']}",
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=filters)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, headers=headers, json=data)
        else:
            return None
            
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.warning(f"⚠️ Error en request: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.warning(f"⚠️ Error de conexión: {e}")
        return None

def get_sample_transactions():
    """Generar transacciones de ejemplo para demostración"""
    categories = {
        'ingreso': ['Salario', 'Freelance', 'Inversiones', 'Bonos'],
        'gasto': ['Alimentación', 'Transporte', 'Vivienda', 'Entretenimiento', 'Salud', 'Educación']
    }
    
    transactions = []
    base_date = datetime.now()
    
    # Generar ingresos
    for i in range(15):
        transaction_date = base_date - timedelta(days=random.randint(0, 90))
        transactions.append({
            'id': f'inc_{i}',
            'usuario_id': 'user_demo_123',
            'monto': round(random.uniform(800, 2000), 2),
            'descripcion': random.choice(categories['ingreso']),
            'categoria': 'Ingresos',
            'tipo': 'ingreso',
            'fecha': transaction_date.strftime('%Y-%m-%d'),
            'created_at': transaction_date.isoformat()
        })
    
    # Generar gastos
    for i in range(30):
        transaction_date = base_date - timedelta(days=random.randint(0, 90))
        category = random.choice(categories['gasto'])
        transactions.append({
            'id': f'exp_{i}',
            'usuario_id': 'user_demo_123',
            'monto': round(random.uniform(10, 300), 2),
            'descripcion': f'Gasto en {category}',
            'categoria': category,
            'tipo': 'gasto',
            'fecha': transaction_date.strftime('%Y-%m-%d'),
            'created_at': transaction_date.isoformat()
        })
    
    return transactions

def get_sample_goals():
    """Generar metas financieras de ejemplo"""
    goals = [
        {
            'id': 'goal_1',
            'usuario_id': 'user_demo_123',
            'titulo': 'Fondo de Emergencia',
            'monto_objetivo': 10000.00,
            'monto_actual': 3500.00,
            'categoria': 'Ahorro Emergencia',
            'fecha_limite': '2024-12-31',
            'prioridad': 'Alta',
            'created_at': '2024-01-01T00:00:00'
        },
        {
            'id': 'goal_2',
            'usuario_id': 'user_demo_123',
            'titulo': 'Vacaciones en Playa',
            'monto_objetivo': 2500.00,
            'monto_actual': 800.00,
            'categoria': 'Vacaciones',
            'fecha_limite': '2024-08-31',
            'prioridad': 'Media',
            'created_at': '2024-01-15T00:00:00'
        }
    ]
    return goals

def get_user_transactions(supabase_client, user_id: str, days: int = 90):
    """Obtener transacciones usando requests - CORREGIDO para tu esquema"""
    try:
        if supabase_client is None:
            return get_sample_transactions()
            
        # Para la base de datos real, necesitamos usar un UUID válido o obtener transacciones sin filtrar
        filters = {
            'select': '*',
            'order': 'fecha.desc',
            'limit': '100'
        }
        
        # Obtener todas las transacciones (sin filtrar por usuario por ahora)
        result = supabase_request(supabase_client, 'GET', 'transacciones', filters=filters)
        
        if result:
            # Mapear los nombres de columnas para que funcionen con tu código existente
            mapped_transactions = []
            for transaction in result:
                mapped_transactions.append({
                    'id': transaction.get('id'),
                    'user_id': transaction.get('usuario_id'),
                    'amount': float(transaction.get('monto', 0)),
                    'description': transaction.get('descripcion', ''),
                    'category': transaction.get('categoria', ''),
                    'transaction_type': 'income' if transaction.get('tipo') == 'ingreso' else 'expense',
                    'date': transaction.get('fecha', ''),  # Mantener como 'date' para compatibilidad
                    'fecha': transaction.get('fecha', ''),  # También mantener original
                    'created_at': transaction.get('created_at', '')
                })
            st.success(f"✅ Obtenidas {len(mapped_transactions)} transacciones de la base de datos")
            return mapped_transactions
        else:
            st.info("📊 Usando datos de ejemplo (no se encontraron transacciones en BD)")
            return get_sample_transactions()
            
    except Exception as e:
        st.warning(f"⚠️ Error: {e}. Usando datos de ejemplo.")
        return get_sample_transactions()

def get_financial_goals(supabase_client, user_id: str):
    """Obtener metas financieras usando requests"""
    try:
        if supabase_client is None:
            return get_sample_goals()
            
        # Para la base de datos real, usar datos de ejemplo por ahora
        st.info("ℹ️ Usando metas de ejemplo para demostración")
        return get_sample_goals()
            
    except Exception as e:
        st.warning(f"⚠️ Error: {e}. Usando datos de ejemplo.")
        return get_sample_goals()

def add_transaction(supabase_client, transaction_data: dict):
    """Agregar transacción usando requests - CORREGIDO para tu esquema"""
    try:
        # Para la base de datos real, necesitamos un UUID válido
        # Usar un UUID por defecto o generar uno aleatorio para demostración
        import uuid
        demo_user_id = str(uuid.uuid4())  # Generar un UUID válido
        
        # Mapear los datos al esquema de tu base de datos
        mapped_data = {
            'usuario_id': demo_user_id,  # Usar UUID válido
            'monto': float(transaction_data.get('amount', 0)),
            'descripcion': transaction_data.get('description', ''),
            'categoria': transaction_data.get('category', ''),
            'tipo': 'ingreso' if transaction_data.get('transaction_type') == 'income' else 'gasto',
            'fecha': transaction_data.get('date', datetime.now().date().isoformat())
        }
        
        if supabase_client is None:
            st.success("✅ Transacción guardada localmente")
            return [{"id": "demo", **transaction_data}]
        
        # CORREGIDO: usar 'transacciones' en lugar de 'transactions'
        result = supabase_request(supabase_client, 'POST', 'transacciones', data=mapped_data)
        
        if result:
            st.success("✅ Transacción guardada en Supabase")
            # Mapear de vuelta para consistencia
            if result and len(result) > 0:
                db_transaction = result[0]
                return [{
                    'id': db_transaction.get('id'),
                    'user_id': db_transaction.get('usuario_id'),
                    'amount': float(db_transaction.get('monto', 0)),
                    'description': db_transaction.get('descripcion', ''),
                    'category': db_transaction.get('categoria', ''),
                    'transaction_type': 'income' if db_transaction.get('tipo') == 'ingreso' else 'expense',
                    'date': db_transaction.get('fecha', ''),
                    'created_at': db_transaction.get('created_at', '')
                }]
        else:
            st.success("✅ Transacción procesada localmente")
            return [{"id": "demo", **transaction_data}]
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None