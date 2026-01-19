from fpdf import FPDF
import pandas as pd
from datetime import datetime
from io import BytesIO
import base64

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Reporte Financiero Personal', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Reemplazar caracteres no soportados
        body = body.replace('•', '-').replace('€', 'EUR').replace('£', 'GBP')
        self.multi_cell(0, 10, body)
        self.ln()
    
    def financial_table(self, headers, data):
        self.set_font('Arial', 'B', 10)
        col_width = self.w / (len(headers) + 1)
        for header in headers:
            self.cell(col_width, 10, header, 1, 0, 'C')
        self.ln()
        self.set_font('Arial', '', 10)
        for row in data:
            for item in row:
                # Asegurar que el item sea string y reemplazar caracteres problemáticos
                item_str = str(item).replace('•', '-').replace('€', 'EUR').replace('£', 'GBP')
                self.cell(col_width, 10, item_str, 1, 0, 'C')
            self.ln()

def generate_financial_report(user_id: str, transactions: list) -> PDFReport:
    pdf = PDFReport()
    pdf.add_page()
    pdf.chapter_title('Resumen Ejecutivo')
    
    if transactions:
        df = pd.DataFrame(transactions)
        
        # Asegurar que tenemos la columna de monto y tipo
        amount_column = 'amount' if 'amount' in df.columns else 'monto'
        type_column = 'transaction_type' if 'transaction_type' in df.columns else 'tipo'
        
        # Convertir tipos de datos
        try:
            df[amount_column] = pd.to_numeric(df[amount_column])
        except:
            df[amount_column] = 0
            
        # Calcular métricas básicas
        if type_column in df.columns:
            monthly_income = df[df[type_column] == 'income'][amount_column].sum()
            monthly_expenses = df[df[type_column] == 'expense'][amount_column].sum()
        else:
            # Si no hay columna de tipo, asumir que todos son gastos para el cálculo
            monthly_income = 0
            monthly_expenses = df[amount_column].sum()
            
        net_savings = monthly_income - monthly_expenses
        savings_rate = (net_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        pdf.chapter_body(f"""
        Periodo analizado: Ultimos 90 dias
        Total de transacciones: {len(transactions)}
        Ingresos totales: ${monthly_income:,.2f}
        Gastos totales: ${monthly_expenses:,.2f}
        Ahorro neto: ${net_savings:,.2f}
        Tasa de ahorro: {savings_rate:.1f}%
        """)
    else:
        pdf.chapter_body("No hay datos de transacciones para generar el reporte.")
    
    if transactions:
        pdf.chapter_title('Analisis de Gastos por Categoria')
        df_expenses = pd.DataFrame([t for t in transactions if t.get('transaction_type') == 'expense' or t.get('tipo') == 'gasto'])
        if not df_expenses.empty:
            # Usar la columna correcta para categoría
            category_column = 'category' if 'category' in df_expenses.columns else 'categoria'
            amount_column = 'amount' if 'amount' in df_expenses.columns else 'monto'
            
            if category_column in df_expenses.columns and amount_column in df_expenses.columns:
                try:
                    df_expenses[amount_column] = pd.to_numeric(df_expenses[amount_column])
                    expenses_by_category = df_expenses.groupby(category_column)[amount_column].sum().sort_values(ascending=False)
                    table_data = []
                    for category, amount in expenses_by_category.items():
                        table_data.append([str(category), f"${amount:,.2f}"])
                    pdf.financial_table(['Categoria', 'Monto Total'], table_data)
                except Exception as e:
                    pdf.chapter_body(f"Error al analizar gastos: {str(e)}")
            else:
                pdf.chapter_body("No se encontraron datos de categorias para analizar")
        else:
            pdf.chapter_body("No hay datos de gastos para analizar")
    
    pdf.chapter_title('Recomendaciones Financieras')
    recommendations = """
    1. Revisa regularmente tus gastos por categoria
    2. Establece metas de ahorro especificas
    3. Considera automatizar tus ahorros
    4. Diversifica tus fuentes de ingreso
    5. Manten un fondo de emergencia de 3-6 meses de gastos
    """
    pdf.chapter_body(recommendations)
    
    pdf.chapter_title('Proximos Pasos')
    pdf.chapter_body("""
    - Revisa este reporte mensualmente
    - Ajusta tu presupuesto segun los hallazgos
    - Celebra tus logros financieros
    - Busca asesoramiento profesional para decisiones importantes
    """)
    return pdf

def create_csv_export(transactions: list) -> str:
    if not transactions:
        return ""
    df = pd.DataFrame(transactions)
    return df.to_csv(index=False)

def create_excel_export(transactions: list) -> BytesIO:
    if not transactions:
        return BytesIO()
    df = pd.DataFrame(transactions)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Transacciones', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Transacciones']
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        worksheet.set_column('D:D', 12, money_format)
    output.seek(0)
    return output