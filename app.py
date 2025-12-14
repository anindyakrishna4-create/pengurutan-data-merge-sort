# File: app.py

import streamlit as st
import pandas as pd
import time
from merge_sort import merge_sort 
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Merge Sort",
    layout="wide"
)

st.title("🧪 Virtual Lab: Merge Sort Interaktif")
st.markdown("### Visualisasi Algoritma Pengurutan Data (Divide and Conquer)")

st.sidebar.header("Konfigurasi Data")

# --- Input Pengguna ---
default_data = "38, 27, 43, 3, 9, 82, 10"
input_data_str = st.sidebar.text_input(
    "Masukkan data (pisahkan dengan koma):", 
    default_data
)
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    initial_data = list(data_list)
except ValueError:
    st.error("Masukkan data dalam format angka yang dipisahkan oleh koma (misalnya: 10, 5, 8).")
    st.stop()
    
# --- Penjelasan ---
st.markdown("""
#### Cara Kerja Merge Sort:
Perhatikan bagaimana array dibagi dan kemudian digabungkan kembali (Merge). Selama proses **Merge**, elemen-elemen dalam rentang **Hijau** dan **Kuning** dibandingkan dan disisipkan kembali ke posisi yang benar dalam rentang gabungan **Biru**.
""")

st.write(f"**Data Awal:** {initial_data}")

# --- Visualisasi Awal ---
if st.button("Mulai Simulasi Merge Sort"):
    
    # PENTING: Kirim data_list sebagai salinan baru agar Merge Sort bisa memodifikasinya
    sorted_data, history = merge_sort(list(data_list))
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    vis_placeholder = st.empty()
    
    # --- Loop Simulasi --- (Dipastikan indentasi 4 spasi)
    for step, state in enumerate(history):
        current_array = state['array']
        # UNPACKING 5 ELEMEN: (start, end, idx_left, idx_right, action_type)
        (start, end, idx_left, idx_right, action_type) = state['highlight']
        action = state['action']

        # Membuat Dataframe untuk Visualisasi Altair
        df_vis = pd.DataFrame({
            'Index': [f'Posisi {i}' for i in range(len(current_array))],
            'Nilai': current_array,
            # Tentukan warna berdasarkan status:
            'Tipe': [
                'Pivot/Key Kiri' if action_type == 'Bandingkan' and i == idx_left else 
                'Pivot/Key Kanan' if action_type == 'Bandingkan' and i == idx_right else 
                'Rentang Merge Selesai' if action_type == 'Gabung Selesai' and start <= i <= end else
                'Selesai' if action_type == 'Selesai' else
                'Normal'
                for i in range(len(current_array))
            ]
        })
        
        # --- MEMBUAT GRAFIK BATANG VERTIKAL TANPA LABEL INDEX ---
        
        chart = alt.Chart(df_vis).mark_bar().encode(
            x=alt.X('Index', 
                    sort=alt.EncodingSortField(field="Index", order='ascending'),
                    axis=None), 
            
            y=alt.Y('Nilai', scale=alt.Scale(domain=[0, max(initial_data) * 1.1])), 
            
            color=alt.Color('Tipe', 
                            scale=alt.Scale(domain=['Pivot/Key Kiri', 'Pivot/Key Kanan', 'Rentang Merge Selesai', 'Selesai', 'Normal'], 
                                            range=['#6AA84F', '#F1C232', '#4A86E8', '#000000', '#999999']), 
                            legend=None),
            tooltip=['Index', 'Nilai', 'Tipe']
        ).properties(
            title=f"Visualisasi Merge Sort (Langkah {step+1}) | Aksi: {action_type}"
        ).interactive()

        # Tampilkan visualisasi di placeholder
        with vis_placeholder.container():
            st.altair_chart(chart, use_container_width=True)
            
            # Tampilkan status di bawah chart
            st.info(f"**Langkah ke-{step+1}** | **Aksi:** {action}")
            if action_type == 'Selesai':
                 st.success("Array telah terurut! Selesai.")
            elif action_type == 'Bandingkan':
                 st.caption("Hijau dan Kuning: Elemen yang sedang dibandingkan dari sub-array kiri dan kanan.")
            elif action_type == 'Gabung Selesai':
                 st.caption(f"Rentang [{start}-{end}] telah diurutkan dan digabungkan.")


        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir ---
    st.balloons()
    st.success(f"**Pengurutan Selesai!**")
    st.write(f"**Data Terurut:** {sorted_data}")
    st.info(f"Algoritma Merge Sort selesai dalam **{len(history)-1}** langkah visualisasi (Merge/Perbandingan).")
