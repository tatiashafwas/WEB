import streamlit as st
import os
import base64
from datetime import date
import pandas as pd  # Library untuk manipulasi data

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
        st.error(f"Logo Dinas tidak ditemukan di path: {logo_dinas_path}")

# Menampilkan judul aplikasi
st.title("Pencatatan Data Harian Tera/Tera Ulang")
st.markdown(
    """
    <div style="text-align: center; font-size: 15px; margin-top: 20px;">
    Aplikasi ini membantu mencatat data tera dan tera ulang secara efisien.
    </div>
    """,
    unsafe_allow_html=True,
)

# Definisi path untuk file CSV
data_file_path = "data_tera_ulang.csv"  # Definisikan path file data

# Menu aplikasi di sidebar
menu = ["Tambah Data", "Lihat Data", "Tentang"]
pilihan = st.sidebar.selectbox("Pilih Menu", menu)

# Fungsi utama berdasarkan menu yang dipilih
if pilihan == "Tambah Data":
    st.subheader("Tambah Data Baru")
    with st.form("form_tambah_data"):
        # Input untuk tanggal
        tanggal = st.date_input("Tanggal", value=date.today())

        # Input untuk nama perusahaan dan alamat
        nama_perusahaan = st.text_input("Nama Perusahaan")
        alamat = st.text_input("Alamat")

        # Input untuk jumlah jenis UTTP
        st.markdown("### Jenis UTTP")
        jumlah_jenis_uttp = st.number_input("Jumlah Jenis UTTP", min_value=8, max_value=50, value=8)

        # Dinamis: Membuat input teks sesuai jumlah UTTP
        jenis_uttp_inputs = []
        jumlah_unit_inputs = []
        for i in range(1, int(jumlah_jenis_uttp) + 1):
            col1, col2 = st.columns([2, 1])
            with col1:
                jenis_uttp = st.text_input(f"Jenis UTTP {i}", placeholder="Opsional")
            with col2:
                jumlah_unit = st.number_input(f"Jumlah UTTP {i}", min_value=0, value=0)
            jenis_uttp_inputs.append(jenis_uttp)
            jumlah_unit_inputs.append(jumlah_unit)

        # Input untuk jenis tera, kegiatan, dan status
        jenis_tera = st.selectbox("Jenis Tera", ["Tera", "Tera Ulang"])
        kegiatan = st.selectbox("Kegiatan", ["Sidang Kantor", "Sidang Pasar", "Loko UAPV", "Loko MT"])
        status = st.selectbox("Status", ["Sah", "Batal"])

        # Tombol simpan
        submit = st.form_submit_button("Simpan Data")

        if submit:
            # Validasi untuk memastikan semua input diisi kecuali UTTP opsional
            if nama_perusahaan and alamat:
                st.success(f"Data berhasil disimpan untuk tanggal {tanggal}!")
                st.write(f"Nama Perusahaan: {nama_perusahaan}")
                st.write(f"Alamat: {alamat}")
                st.write(f"Jenis Tera: {jenis_tera}, Kegiatan: {kegiatan}, Status: {status}")
                for i, jenis in enumerate(jenis_uttp_inputs):
                    if jenis:  # Hanya tampilkan jika ada isi
                        st.write(f"Jenis UTTP {i+1}: {jenis}, Jumlah UTTP: {jumlah_unit_inputs[i]}")
                
                # Simpan data ke file CSV
                data = {
                    'Tanggal': [tanggal],
                    'Nama Perusahaan': [nama_perusahaan],
                    'Alamat': [alamat],
                    'Jenis Tera': [jenis_tera],
                    'Kegiatan': [kegiatan],
                    'Status': [status]
                }
                for i, jenis in enumerate(jenis_uttp_inputs):
                    if jenis:
                        data[f"Jenis UTTP {i+1}"] = [jenis]
                        data[f"Jumlah UTTP {i+1}"] = [jumlah_unit_inputs[i]]
                
                df = pd.DataFrame(data)
                try:
                    if not os.path.exists(data_file_path):
                        # Jika file tidak ditemukan, buat file baru dengan header
                        with open(data_file_path, 'w') as f:
                            f.write('Tanggal,Nama Perusahaan,Alamat,Jenis Tera,Kegiatan,Status\n')
                    df.to_csv(data_file_path, mode='a', index=False, header=False)  # mode='a' untuk append
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menulis ke file CSV: {e}")

            else:
                st.error("Harap isi semua kolom wajib (Nama Perusahaan dan Alamat)!")

elif pilihan == "Lihat Data":
    st.subheader("Data Tera/Tera Ulang")
    if os.path.exists(data_file_path):
        data = pd.read_csv(data_file_path)  # Load data
        st.dataframe(data)  # Tampilkan data dalam bentuk DataFrame
    else:
        st.error("File data tidak ditemukan!")

elif pilihan == "Tentang":
    st.subheader("Tentang Aplikasi")
    st.markdown(
        """
        <div style="text-align: justify;">
        Aplikasi ini dirancang untuk memudahkan pencatatan data tera/tera ulang
        oleh UPTD Metrologi Legal Kota Surabaya.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; font-size: 14px;">
    © 2024 UPTD Metrologi Legal. Hak cipta dilindungi undang-undang.
    </div>
    """,
    unsafe_allow_html=True,
)
