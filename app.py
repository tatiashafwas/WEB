import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Fungsi untuk memuat data dari file CSV
def load_data():
    try:
        data = pd.read_csv("data_tera.csv")
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Tanggal", "Nama Perusahaan", "Alamat", "Jenis UTTP", "Jenis Tera", "Kegiatan", "Status"])
    return data

# Fungsi untuk menyimpan data ke file CSV
def save_data(data):
    data.to_csv("data_tera.csv", index=False)

# Fungsi untuk menyimpan data ke file Excel menggunakan pandas
def save_to_excel(data):
    filename = "data_tera.xlsx"
    data.to_excel(filename, index=False, sheet_name="Data Tera")
    return filename

# Fungsi utama aplikasi
def main():
    # Menampilkan logo dan judul di pojok kiri atas
    logo_path = "C:/Users/tatia shafwa s/OneDrive/Documents/Tera Ulang/LOGO-METRO.png"  # Path gambar yang sudah digabungkan
    if os.path.exists(logo_path):
        # Menampilkan gambar dengan ukuran lebih kecil dan di posisi kiri atas
        st.markdown(
            f"""
            <style>
            .logo {{
                position: absolute;
                top: 20px;  /* Logo lebih tinggi */
                left: 20px;  /* Logo lebih ke kiri */
                width: 120px;  /* Ukuran logo yang lebih kecil */
                height: auto;
            }}
            .main-header {{
                font-size: 36px;
                color: #FFFFFF;
                text-align: center;
                font-weight: bold;
                margin-top: 140px; /* Memberikan jarak lebih besar agar judul lebih rendah */
                margin-bottom: 20px;
            }}
            .sidebar {{
                margin-top: 160px;  /* Pastikan sidebar tetap di bawah logo dan judul */
            }}
            .sidebar .css-1d391kg {{
                margin-top: 0px;  /* Atur margin untuk elemen dropdown agar tidak terganggu */
            }}
            </style>
            <img src="data:image/png;base64,{get_image_base64(logo_path)}" class="logo">
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"Gambar tidak ditemukan di path {logo_path}")

    # Menampilkan waktu dan tanggal saat ini
    current_datetime = datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")
    st.markdown(f"<div style='text-align: center; font-size: 20px;'>Waktu saat ini: {current_datetime}</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">Aplikasi Pencatatan Data Harian Tera/Tera Ulang</div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    st.sidebar.markdown(
        """
        <div class="sidebar-title">Menu Utama</div>
        """,
        unsafe_allow_html=True,
    )

    menu = ["Tambah Data", "Lihat Data", "Tentang"]
    pilihan = st.sidebar.selectbox("Pilih Menu", menu)

    if pilihan == "Tambah Data":
        st.subheader("Tambah Data Baru")
        with st.form("form_tambah_data"):
            tanggal = st.date_input("Tanggal", datetime.today())
            nama_perusahaan = st.text_input("Nama Perusahaan")
            alamat = st.text_input("Alamat")
            
            # Kolom dinamis untuk Jenis UTTP
            st.markdown("**Jenis UTTP (Masukkan hingga 8 jenis)**")
            jenis_UTTP_list = []
            for i in range(1, 9):  # Hingga 8 kolom
                jenis = st.text_input(f"Jenis UTTP {i}", key=f"jenis_UTTP_{i}")
                if jenis:  # Hanya tambahkan jika tidak kosong
                    jenis_UTTP_list.append(jenis)

            jenis_tera = st.selectbox("Jenis Tera", ["Tera", "Tera Ulang"])
            kegiatan = st.selectbox("Kegiatan", ["Sidang Kantor", "Sidang Pasar", "Loko UAPV", "Loko MT"])
            status = st.selectbox("Status", ["Sah", "Batal"])
            submit = st.form_submit_button("Simpan Data")

            if submit:
                if nama_perusahaan and alamat and kegiatan and jenis_UTTP_list:
                    data = load_data()
                    new_data = {
                        "Tanggal": tanggal.strftime("%Y-%m-%d"),
                        "Nama Perusahaan": nama_perusahaan,
                        "Alamat": alamat,
                        "Jenis UTTP": ", ".join(jenis_UTTP_list),  # Gabungkan ke satu string
                        "Jenis Tera": jenis_tera,
                        "Kegiatan": kegiatan,
                        "Status": status,
                    }
                    data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
                    save_data(data)
                    st.success("Data berhasil disimpan!")
                else:
                    st.error("Harap isi semua kolom yang wajib!")

    elif pilihan == "Lihat Data":
        st.subheader("Data Tera/Tera Ulang")
        data = load_data()
        if not data.empty:
            st.dataframe(data)

            # Tombol ekspor ke Excel
            if st.button("Ekspor Data ke Excel"):
                try:
                    excel_file = save_to_excel(data)
                    st.success(f"Data berhasil diekspor ke file {excel_file}")
                    with open(excel_file, "rb") as file:
                        st.download_button(
                            label="Unduh File Excel",
                            data=file,
                            file_name="data_tera.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                except Exception as e:
                    st.error(f"Gagal mengekspor data: {e}")

    elif pilihan == "Tentang":
        st.subheader("Tentang Aplikasi")
        st.markdown(
            """
            <div style="text-align: justify;">
            Aplikasi ini dibuat untuk memudahkan pencatatan data harian tera/tera ulang.
            Dikembangkan menggunakan Python dan Streamlit. 
            Dengan fitur sederhana, pengguna dapat mencatat dan melihat data yang tersimpan.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Fungsi untuk mengonversi gambar ke base64
def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Pastikan blok ini benar
if __name__ == "__main__":
    main()