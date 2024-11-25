import streamlit as st
import os
import base64
from datetime import date

# Fungsi untuk mengonversi gambar ke Base64
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# Path ke file logo (ganti sesuai lokasi file Anda)
logo_uptd_path = r"City_of_Surabaya_Logo.png"
logo_dinas_path = r"LOGO-METRO.png"

# Cek keberadaan file logo dan konversi ke Base64
logo_uptd_base64 = get_image_base64(logo_uptd_path)
logo_dinas_base64 = get_image_base64(logo_dinas_path)

# Menampilkan header jika logo ditemukan
if logo_uptd_base64 and logo_dinas_base64:
    st.markdown(
        f"""
        <style>
        .header {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 10px 20px;
            background-color: #222; /* Background warna gelap */
            gap: 10px;
        }}
        .logo {{
            height: 80px; /* Ukuran tinggi logo */
        }}
        .text {{
            text-align: center;
            color: white;
            font-size: 20px;
            font-weight: bold;
        }}
        </style>
        <div class="header">
            <img src="data:image/png;base64,{logo_uptd_base64}" class="logo">
            <div class="text">
                <div>UPTD METROLOGI LEGAL KOTA SURABAYA</div>
                <div>Gedung ex. Siola, Jl. Tunjungan No.1-3 lantai 2, Genteng, Surabaya, East Java 60275</div>
                <div>(031) 52403192</div>
            </div>
            <img src="data:image/png;base64,{logo_dinas_base64}" class="logo">
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Menampilkan error jika logo tidak ditemukan
    if not logo_uptd_base64:
        st.error(f"Logo UPTD tidak ditemukan di path: {logo_uptd_path}")
    if not logo_dinas_base64:
        st.error(f"Logo D
