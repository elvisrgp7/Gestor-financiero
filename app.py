import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Mi Gestor Financiero",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

CATEGORIAS_GASTO = ['Vivienda', 'Alimentación', 'Servicios', 'Transporte', 'Educación', 'Ocio', 'Salud', 'Otros']
CATEGORIAS_INGRESO = ['Sueldo', 'Beca', 'Inversiones (BVL)', 'Intereses', 'Regalo', 'Otros']

HISTORIAL_2026 = [
    # --- ENERO 2026 ---
    { 'date': '2026-01-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-01-31', 'description': 'Internet celular', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-01-07', 'description': 'Pichanga', 'amount': 18.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-01-03', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-01-10', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-01-17', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-01-24', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-01-04', 'description': 'Salidita GYm', 'amount': 35.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-01-05', 'description': 'Pasajes + desayunos (del 5 al 9)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-01-12', 'description': 'Pasajes + desayunos (del 12 al 16)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-01-19', 'description': 'Pasajes + desayunos (del 19 al 23)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-01-26', 'description': 'Pasajes + desayunos (del 26 al 30)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-01-15', 'description': 'gas', 'amount': 25.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-01-21', 'description': 'pichanga', 'amount': 17.2, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-01-31', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-01-31', 'description': 'Ingresos SBS', 'amount': 1200.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-01-31', 'description': 'Ingreso intereses', 'amount': 10.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- FEBRERO 2026 ---
    { 'date': '2026-02-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-02-28', 'description': 'Internet celular', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-02-06', 'description': 'pasaje pache', 'amount': 39.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-02-08', 'description': 'plantillas', 'amount': 5.0, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-02-10', 'description': 'medicina', 'amount': 9.6, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-02-12', 'description': 'Luz mamá', 'amount': 5.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-02-01', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-02-08', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-02-15', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-02-22', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-02-14', 'description': 'Pichanga', 'amount': 19.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-02-02', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-02-09', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-02-16', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-02-23', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-02-18', 'description': 'Corte de Cabello', 'amount': 12.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-02-28', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-02-21', 'description': 'Pichanga', 'amount': 17.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-02-22', 'description': 'Recargo', 'amount': 5.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-02-25', 'description': 'Pollada Colaboración', 'amount': 22.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-02-27', 'description': 'Voleyball', 'amount': 18.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-02-28', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-02-28', 'description': 'Ingreso intereses', 'amount': 20.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- MARZO 2026 ---
    { 'date': '2026-03-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-03-31', 'description': 'Internet celular', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-03-04', 'description': 'Luz', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-03-08', 'description': 'Deudas de Moquegua', 'amount': 88.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-03-10', 'description': 'Luz mamá', 'amount': 5.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-03-01', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-08', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-15', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-22', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-29', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-02', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-03-09', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-03-16', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-03-23', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-03-12', 'description': 'Acondicionador', 'amount': 11.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-03-31', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-03-14', 'description': 'Aceituna', 'amount': 132.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-03-15', 'description': 'Pichanga', 'amount': 18.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-03-18', 'description': 'Pichanga', 'amount': 20.9, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-03-24', 'description': 'Short', 'amount': 24.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-03-31', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-03-31', 'description': 'Ingreso intereses', 'amount': 10.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- ABRIL 2026 ---
    { 'date': '2026-04-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-04-30', 'description': 'Internet celular', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-04-03', 'description': 'Regalo mamá', 'amount': 200.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-08', 'description': 'Recargo Pedro', 'amount': 5.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-10', 'description': 'medicina', 'amount': 6.0, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-04-12', 'description': 'medicina tesoro', 'amount': 6.5, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-04-04', 'description': 'Pichanga', 'amount': 32.55, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-04-05', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-04-12', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-04-19', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-04-26', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-04-02', 'description': 'Pasajes + desayunos', 'amount': 27.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-04-09', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-04-16', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-04-23', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-04-27', 'description': 'Pasajes + desayunos', 'amount': 30.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-04-11', 'description': 'recicle', 'amount': 8.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-30', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-14', 'description': 'polera', 'amount': 33.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-15', 'description': 'gas', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-04-18', 'description': 'corte de cabello', 'amount': 12.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-04-22', 'description': 'pichanga', 'amount': 16.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-04-25', 'description': 'pichanga', 'amount': 29.5, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-04-30', 'description': 'Ingresos SBS + veredas', 'amount': 1750.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-04-30', 'description': 'Ingreso intereses', 'amount': 14.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- MAYO 2026 ---
    { 'date': '2026-05-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-05-31', 'description': 'Internet celular (anticipado)', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-05-06', 'description': 'regalo naty', 'amount': 36.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-05-10', 'description': 'Pichanga', 'amount': 19.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-05-15', 'description': 'Pichanga', 'amount': 23.3, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-05-03', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-10', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-17', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-24', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-31', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-04', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-05-11', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-05-18', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-05-25', 'description': 'Pasajes + desayunos', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-05-22', 'description': 'Pichanga', 'amount': 15.8, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-05-31', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-05-12', 'description': 'Pollito', 'amount': 26.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-05-15', 'description': 'gas', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-05-23', 'description': 'Pichanga', 'amount': 35.5, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-05-31', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-05-31', 'description': 'Ingreso intereses', 'amount': 16.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- JUNIO 2026 ---
    { 'date': '2026-06-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-06-30', 'description': 'Internet celular (anticipado)', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-06-30', 'description': 'Internt fijo', 'amount': 70.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-06-10', 'description': 'medicina gripa', 'amount': 17.0, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-06-10', 'description': 'shampoo Tio nacho', 'amount': 20.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-27', 'description': 'Pichanga 27.06', 'amount': 19.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-06-07', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-06-14', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-06-21', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-06-28', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-06-12', 'description': 'Emisión de DNIe', 'amount': 33.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-12', 'description': 'Llave para lavadora', 'amount': 12.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-06-03', 'description': 'Pasajes + desayunos (del 1 al 5)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-06-10', 'description': 'Pasajes + desayunos (del 8 al 12)', 'amount': 35.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-06-17', 'description': 'Pasajes + desayunos (del 15 al 19)', 'amount': 39.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-06-24', 'description': 'Pasajes + desayunos (del 22 al 26)', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-06-29', 'description': 'Pichanga 29.06', 'amount': 23.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-06-15', 'description': 'Salida tio manuel', 'amount': 23.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-06-30', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-05', 'description': 'Biotina 05/06', 'amount': 53.83, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-06-18', 'description': 'lavadora', 'amount': 10.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-19', 'description': 'Pastillas', 'amount': 19.0, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-06-22', 'description': 'buzo + polo', 'amount': 32.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-25', 'description': 'Depósito papa', 'amount': 50.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-27', 'description': 'Corte de cabello 27/06', 'amount': 15.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-06-30', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-06-30', 'description': 'Ingreso intereses', 'amount': 16.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- JULIO 2026 ---
    { 'date': '2026-07-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-07-31', 'description': 'Internet celular (anticipado)', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-07-31', 'description': 'Internt fijo', 'amount': 70.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-07-08', 'description': 'Recogo DNI', 'amount': 3.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-07-10', 'description': 'crema mon', 'amount': 17.0, 'category': 'Salud', 'type': 'gasto' },
    { 'date': '2026-07-05', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-07-12', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-07-19', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-07-26', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-07-02', 'description': 'Pasajes + desayunos (del 30 al 3)', 'amount': 34.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-07-08', 'description': 'Pasajes + desayunos (del 6 al 10)', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-07-15', 'description': 'Pasajes + desayunos (del 13 al 17)', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-07-22', 'description': 'Pasajes + desayunos (del 20 al 24)', 'amount': 34.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-07-29', 'description': 'Pasajes + desayunos (del 27 al 31)', 'amount': 17.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-07-18', 'description': 'cumple teffa', 'amount': 132.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-07-11', 'description': 'Pichanga 11.07', 'amount': 25.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-07-31', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-07-04', 'description': 'Pichanga 04.07', 'amount': 31.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-07-14', 'description': 'Gas', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-07-25', 'description': 'Cine + salida', 'amount': 84.0, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-07-28', 'description': 'Cevichito', 'amount': 16.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-07-31', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-07-31', 'description': 'Ingreso intereses', 'amount': 17.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- AGOSTO 2026 ---
    { 'date': '2026-08-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-08-31', 'description': 'Internet celular (anticipado)', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-08-31', 'description': 'Internt fijo', 'amount': 70.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-08-02', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-09', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-16', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-23', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-30', 'description': 'compras de la semana', 'amount': 110.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-05', 'description': 'del 3 al 7 Pasajes + desayunos', 'amount': 34.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-08-12', 'description': 'del 10 al 14 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-08-19', 'description': 'del 17 al 21 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-08-26', 'description': 'del 24 al 28 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-08-10', 'description': 'pedido Temu', 'amount': 67.64, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-08-15', 'description': 'Pedido Temu Mama', 'amount': 50.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-08-08', 'description': 'Shampo + Jabon', 'amount': 53.8, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-08-18', 'description': 'cevichito', 'amount': 10.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-08-31', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-08-14', 'description': 'Pasaje mom', 'amount': 130.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-08-11', 'description': 'gas', 'amount': 26.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-08-15', 'description': 'pichanga 15/08', 'amount': 26.7, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-08-22', 'description': 'PICHANGA 22/08', 'amount': 27.52, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-08-23', 'description': 'Pichanga 23/08', 'amount': 18.8, 'category': 'Ocio', 'type': 'gasto' },
    { 'date': '2026-08-28', 'description': 'Protector Celular', 'amount': 20.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-08-31', 'description': 'Ingresos SBS', 'amount': 2250.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-08-31', 'description': 'Ingreso intereses', 'amount': 15.0, 'category': 'Intereses', 'type': 'ingreso' },

    # --- SETIEMBRE 2026 ---
    { 'date': '2026-09-12', 'description': 'Cuarto', 'amount': 175.0, 'category': 'Vivienda', 'type': 'gasto' },
    { 'date': '2026-09-30', 'description': 'Internet celular (anticipado)', 'amount': 27.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-09-30', 'description': 'Internt fijo', 'amount': 70.0, 'category': 'Servicios', 'type': 'gasto' },
    { 'date': '2026-09-06', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-09-13', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-09-20', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-09-27', 'description': 'compras de la semana', 'amount': 120.0, 'category': 'Alimentación', 'type': 'gasto' },
    { 'date': '2026-09-02', 'description': 'del 31/9 al 4 Pasajes + desayunos', 'amount': 34.0, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-09-09', 'description': 'del 7 al 11 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-09-16', 'description': 'del 14 al 18 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-09-23', 'description': 'del 21 al 58 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-09-30', 'description': 'del 28 al 2/10 Pasajes + desayunos', 'amount': 42.5, 'category': 'Transporte', 'type': 'gasto' },
    { 'date': '2026-09-30', 'description': 'Pago Prestamo', 'amount': 143.0, 'category': 'Otros', 'type': 'gasto' },
    { 'date': '2026-09-30', 'description': 'Ingresos SBS', 'amount': 1500.0, 'category': 'Sueldo', 'type': 'ingreso' },
    { 'date': '2026-09-30', 'description': 'Ingreso intereses', 'amount': 10.0, 'category': 'Intereses', 'type': 'ingreso' },
]

if 'transactions' not in st.session_state:
    st.session_state.transactions = HISTORIAL_2026

if 'edit_idx' not in st.session_state:
    st.session_state.edit_idx = None

st.title("💼 Mi Gestor Financiero")
st.markdown("Control inteligente de ingresos, gastos y reportes en tiempo real desde Enero 2026.")

st.sidebar.header("⚙️ Configuración y Filtros")

meses_opciones = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10', '2026-11', '2026-12']
nombres_meses = {
    '2026-01': 'Enero 2026', '2026-02': 'Febrero 2026', '2026-03': 'Marzo 2026', 
    '2026-04': 'Abril 2026', '2026-05': 'Mayo 2026', '2026-06': 'Junio 2026', 
    '2026-07': 'Julio 2026', '2026-08': 'Agosto 2026', '2026-09': 'Setiembre 2026',
    '2026-10': 'Octubre 2026', '2026-11': 'Noviembre 2026', '2026-12': 'Diciembre 2026'
}

selected_month = st.sidebar.selectbox(
    "Seleccionar Mes", 
    options=meses_opciones, 
    format_func=lambda x: nombres_meses.get(x, x),
    index=0 # Por defecto Enero 2026
)

search_query = st.sidebar.text_input("🔍 Buscar en detalle", value="")

with st.sidebar.expander("⚙️ Opciones avanzadas"):
    st.markdown("<small style='color:gray;'>¿Alteraste o eliminaste datos por error? Aquí puedes volver a cargar todo el Excel original del 2026.</small>", unsafe_allow_html=True)
    if st.button("🔄 Restaurar Todo el Historial 2026"):
        st.session_state.transactions = HISTORIAL_2026
        st.session_state.edit_idx = None
        st.success("¡Historial completo restaurado con éxito!")
        st.rerun()

df = pd.DataFrame(st.session_state.transactions)

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    df_filtered = df[df['date'].dt.strftime('%Y-%m') == selected_month].copy()
    
    if search_query:
        df_filtered = df_filtered[df_filtered['description'].str.contains(search_query, case=False, na=False)]
        
    df_filtered.sort_values(by='date', ascending=False, inplace=True)
    
    total_income = df_filtered[df_filtered['type'] == 'ingreso']['amount'].sum()
    total_expense = df_filtered[df_filtered['type'] == 'gasto']['amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Balance / Ahorro", f"S/ {balance:,.2f}")
    col2.metric("Ingresos", f"S/ {total_income:,.2f}")
    col3.metric("Gastos", f"S/ {total_expense:,.2f}")
else:
    df_filtered = pd.DataFrame(columns=['date', 'description', 'amount', 'category', 'type'])
    total_income, total_expense, balance = 0, 0, 0

st.divider()

if not df_filtered.empty:
    with st.expander("📊 Ver Gráfico de Gastos por Categoría"):
        df_gastos = df_filtered[df_filtered['type'] == 'gasto']
        if not df_gastos.empty:
            cat_sum = df_gastos.groupby('category')['amount'].sum()
            st.bar_chart(cat_sum)
        else:
            st.info("No hay gastos registrados en este mes para graficar.")

tab1, tab2 = st.tabs(["➕ Nuevo Registro", "📋 Movimientos y Exportar"])

with tab1:
    st.subheader("Agregar Movimiento")
    with st.form("transaction_form", clear_on_submit=True):
        form_type = st.radio("Tipo", ["gasto", "ingreso"], horizontal=True)
        form_date = st.date_input("Fecha", value=datetime.now())
        form_description = st.text_input("Detalle (Ej. Compras del supermercado)")
        
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
    st.subheader(f"Movimientos de {nombres_meses.get(selected_month, selected_month)}")
    
    if not df_filtered.empty:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar estos movimientos en CSV (Excel)",
            data=csv_data,
            file_name=f'movimientos_{selected_month}.csv',
            mime='text/csv',
        )
        st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.edit_idx is not None:
        st.markdown("---")
        st.info(f"✏️ Estás editando el movimiento seleccionado.")
        t_to_edit = st.session_state.transactions[st.session_state.edit_idx]
        
        with st.form("edit_form"):
            e_type = st.radio("Tipo", ["gasto", "ingreso"], horizontal=True, index=0 if t_to_edit['type'] == 'gasto' else 1)
            e_date = st.date_input("Fecha", value=pd.to_datetime(t_to_edit['date']))
            e_desc = st.text_input("Detalle", value=t_to_edit['description'])
            e_cats = CATEGORIAS_GASTO if e_type == 'gasto' else CATEGORIAS_INGRESO
            cat_idx = e_cats.index(t_to_edit['category']) if t_to_edit['category'] in e_cats else 0
            e_cat = st.selectbox("Categoría", e_cats, index=cat_idx)
            e_amount = st.number_input("Monto (S/)", min_value=0.01, step=1.0, value=float(t_to_edit['amount']))
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                saved = st.form_submit_button("Guardar Cambios")
            with col_cancel:
                cancelled = st.form_submit_button("Cancelar Edición")
                
            if saved:
                st.session_state.transactions[st.session_state.edit_idx] = {
                    'date': e_date.strftime('%Y-%m-%d'),
                    'description': e_desc,
                    'amount': float(e_amount),
                    'category': e_cat,
                    'type': e_type
                }
                st.session_state.edit_idx = None
                st.success("¡Movimiento actualizado exitosamente!")
                st.rerun()
            if cancelled:
                st.session_state.edit_idx = None
                st.rerun()
        st.markdown("---")

    if df_filtered.empty:
        st.info("No hay movimientos registrados para este mes o búsqueda.")
    else:
        for idx, row in df_filtered.reset_index().iterrows():
            sign = "+" if row['type'] == 'ingreso' else "-"
            color = "green" if row['type'] == 'ingreso' else "red"
            
            col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
            with col_a:
                st.markdown(f"**{row['description']}**<br><small style='color:gray;'>{row['date'].strftime('%Y-%m-%d')} • {row['category']}</small>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<span style='color:{color}; font-weight:bold; font-size:1.1em;'>{sign}S/ {row['amount']:,.2f}</span>", unsafe_allow_html=True)
            with col_c:
                orig_idx = df[(df['date'] == row['date']) & (df['description'] == row['description']) & (df['amount'] == row['amount']) & (df['category'] == row['category'])].index
                if st.button("✏️", key=f"edit_btn_{idx}", help="Editar"):
                    if not orig_idx.empty:
                        st.session_state.edit_idx = orig_idx[0]
                        st.rerun()
            with col_d:
                if st.button("🗑️", key=f"del_{idx}", help="Eliminar"):
                    if not orig_idx.empty:
                        st.session_state.transactions.pop(orig_idx[0])
                        if st.session_state.edit_idx == orig_idx[0]:
                            st.session_state.edit_idx = None
                        st.rerun()
            st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
