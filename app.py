import streamlit as st
import os
import base64

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

# Menu aplikasi di sidebar
menu = ["Tambah Data", "Lihat Data", "Tentang"]
pilihan = st.sidebar.selectbox("Pilih Menu", menu)

# Fungsi utama berdasarkan menu yang dipilih
if pilihan == "Tambah Data":
    st.subheader("Tambah Data Baru")
    with st.form("form_tambah_data"):
        # Input untuk nama perusahaan dan alamat
        nama_perusahaan = st.text_input("Nama Perusahaan")
        alamat = st.text_input("Alamat")

        # Input untuk jumlah jenis UTTP
        st.markdown("### Jenis UTTP")
        jumlah_jenis_uttp = st.number_input("Jumlah Jenis UTTP", min_value=1, max_value=50, value=8)
        
        # Dinamis: Membuat input teks sesuai jumlah UTTP
        jenis_uttp_inputs = []
        jumlah_unit_inputs = []
        for i in range(1, int(jumlah_jenis_uttp) + 1):
            col1, col2 = st.columns([2, 1])
            with col1:
                jenis_uttp = st.text_input(f"Jenis UTTP {i}")
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
            # Validasi untuk memastikan semua input diisi
            if nama_perusahaan and alamat and all(jenis_uttp_inputs):
                st.success(f"Data berhasil disimpan!")
                for i, jenis in enumerate(jenis_uttp_inputs):
                    st.write(f"Jenis UTTP {i+1}: {jenis}, Jumlah UTTP: {jumlah_unit_inputs[i]}")
            else:
                st.error("Harap isi semua kolom, termasuk semua Jenis UTTP dan jumlah unitnya!")

elif pilihan == "Lihat Data":
    st.subheader("Data Tera/Tera Ulang")
    st.write("Tampilkan data di sini.")

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
