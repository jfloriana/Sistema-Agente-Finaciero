import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://rnycpzeewpwmmjibmojj.supabase.co")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJueWNwemVld3B3bW1qaWJtb2pqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1MzU3NjcsImV4cCI6MjA3NzExMTc2N30.9Y-6l8f_70zQMo9RP0ETciQ_is-fqXWk7ioKyqyvVcg")
    N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "")
    APP_NAME = "Asesor Financiero Personal IA"
    DEBUG = st.secrets.get("DEBUG", "False").lower() == "true"
    DEFAULT_CURRENCY = "USD"
    
    INCOME_CATEGORIES = ["Salario", "Freelance", "Inversiones", "Bonos", "Regalos", "Reembolsos", "Otros Ingresos"]
    EXPENSE_CATEGORIES = ["Alimentación", "Transporte", "Vivienda", "Entretenimiento", "Salud", "Educación", "Ropa", "Tecnología", "Servicios", "Impuestos", "Seguros", "Deudas", "Otros Gastos"]
    GOAL_CATEGORIES = ["Ahorro Emergencia", "Vacaciones", "Automóvil", "Casa", "Educación", "Inversiones", "Retiro", "Salud", "Otros"]
    
    SAVINGS_RATE_TARGET = 20.0
    EMERGENCY_FUND_TARGET = 6
    HIGH_SPENDING_ALERT = 0.4

config = Config()