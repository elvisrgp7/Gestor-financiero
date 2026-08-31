import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Mi Gestor Financiero",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS modernos para imitar el diseño limpio anterior
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Categorías predefinidas
CATEGORIAS_GASTO = ['Vivienda', 'Alimentación', 'Servicios', 'Transporte', 'Educación', 'Ocio', 'Salud', 'Otros']
CATEGORIAS_INGRESO = ['Sueldo', 'Beca', 'Inversiones (BVL)', 'Intereses', 'Regalo', 'Otros']

# Historial inicial 2026 (extraído de tu Excel)
HISTORIAL_2026 = [
    { 'date': '2026-01-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-01-10', 'description': 'Internet casa', 'amount': 25.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-01-15', 'description': 'Internet celular', 'amount': 36.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-01-20', 'description': 'Pago Préstamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-01-08', 'description': 'Compras semana 1', 'amount': 50.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-01-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-02-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-02-10', 'description': 'Internet casa', 'amount': 25.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-02-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-03-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-03-10', 'description': 'Compras de la semana', 'amount': 60.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-04-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-04-12', 'description': 'Pichanga', 'amount': 15.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-04-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-05-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-05-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-06-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-06-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-07-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-07-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-08-05', 'description': 'Cuarto', 'amount': 125.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-08-10', 'description': 'Internet casa', 'amount': 25.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-08-15', 'description': 'Internet celular', 'amount': 36.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-08-02', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
]

if 'transactions' not in st.session_state:
    st.session_state.transactions = HISTORIAL_2026

# Título principal
st.title("💼 Mi Gestor Financiero")
st.markdown("Control de ingresos y gastos optimizado en Streamlit.")

st.sidebar.header("⚙️ Opciones")
current_year_month = datetime.now().strftime("%Y-%m")
selected_month = st.sidebar.text_input("Filtrar por Mes (YYYY-MM)", value="2026-08")

# Botón para reiniciar/recargar historial base
if st.sidebar.button("Cargar/Restaurar Historial 2026"):
    st.session_state.transactions = HISTORIAL_2026
    st.sidebar.success("¡Historial restaurado!")

df = pd.DataFrame(st.session_state.transactions)

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    # Filtrar por mes seleccionado
    df_filtered = df[df['date'].dt.strftime('%Y-%m') == selected_month].copy()
    df_filtered.sort_values(by='date', ascending=False, inplace=True)
    
    total_income = df_filtered[df_filtered['type'] == 'ingreso']['amount'].sum()
    total_expense = df_filtered[df_filtered['type'] == 'gasto']['amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.cols(3)
    col1.metric("Balance del Mes", f"S/ {balance:,.2f}")
    col2.metric("Ingresos", f"S/ {total_income:,.2f}")
    col3.metric("Gastos", f"S/ {total_expense:,.2f}")
else:
    df_filtered = pd.DataFrame(columns=['date', 'description', 'amount', 'category', 'type'])
    total_income, total_expense, balance = 0, 0, 0

st.divider()

tab1, tab2 = st.tabs(["➕ Nuevo Registro", "📋 Movimientos"])

with tab1:
    st.subheader("Agregar Movimiento")
    with st.form("transaction_form", clear_on_submit=True):
        form_type = st.radio("Tipo", ["gasto", "ingreso"], horizontal=True)
        form_date = st.date_input("Fecha", value=datetime.now())
        form_description = st.text_input("Detalle (Ej. Pago de cuarto)")
        
        categories = CATEGORIAS_GASTO if form_type == 'gasto' else CATEGORIAS_INGRESO
        form_category = st.selectbox("Categoría", categories)
        form_amount = st.number_input("Monto (S/)", min_value=0.01, step=1.0)
        
        submitted = st.form_submit_button("Guardar Registro")
        if submitted:
            if form_description:
                new_item = {
                    'date': form_date.strftime('%Y-%m-%d'),
                    'description': form_description,
                    'amount': float(form_amount),
                    'category': form_category,
                    'type': form_type
                }
                st.session_state.transactions.append(new_item)
                st.success("¡Movimiento agregado exitosamente!")
                st.rerun()
            else:
                st.error("Por favor ingresa un detalle.")

with tab2:
    st.subheader(f"Movimientos de {selected_month}")
    if df_filtered.empty:
        st.info("No hay movimientos registrados para este mes.")
    else:
        for idx, row in df_filtered.reset_index().iterrows():
            sign = "+" if row['type'] == 'ingreso' else "-"
            color = "green" if row['type'] == 'ingreso' else "red"
            
            col_a, col_b, col_c = st.columns([4, 2, 1])
            with col_a:
                st.markdown(f"**{row['description']}**<br><small style='color:gray;'>{row['date'].strftime('%Y-%m-%d')} • {row['category']}</small>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<span style='color:{color}; font-weight:bold; font-size:1.1em;'>{sign}S/ {row['amount']:,.2f}</span>", unsafe_allow_html=True)
            with col_c:
                if st.button("🗑️", key=f"del_{idx}"):
                    # Eliminar de la lista principal basado en los valores
                    orig_idx = df[(df['date'] == row['date']) & (df['description'] == row['description']) & (df['amount'] == row['amount'])].index
                    if not orig_idx.empty:
                        st.session_state.transactions.pop(orig_idx[0])
                        st.rerun()
            st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
