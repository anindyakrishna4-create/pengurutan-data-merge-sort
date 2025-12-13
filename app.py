# File: app.py (Hanya Revisi pada Loop Simulasi)

# ... (kode app.py bagian atas tetap sama) ...

    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        # Pastikan kita menerima 5 elemen:
        (start, end, idx_left, idx_right, action_type) = state['highlight']
        action = state['action']

        # Membuat Dataframe untuk Visualisasi Altair
        df_vis = pd.DataFrame({
            'Index': [f'Posisi {i}' for i in range(len(current_array))],
            'Nilai': current_array,
            
            # Logika Tipe untuk Pewarnaan
            'Tipe': [
                # Pivot Kiri/Kanan hanya relevan saat Bandingkan
                'Pivot/Key Kiri' if action_type == 'Bandingkan' and i == idx_left else 
                'Pivot/Key Kanan' if action_type == 'Bandingkan' and i == idx_right else 
                # Rentang Merge Selesai: Highlight seluruh rentang yang baru diurutkan
                'Rentang Merge Selesai' if action_type == 'Gabung Selesai' and start <= i <= end else
                'Selesai' if action_type == 'Selesai' else # Highlight semua dengan warna Selesai
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
                            # Tambahkan warna untuk status Selesai
                            scale=alt.Scale(domain=['Pivot/Key Kiri', 'Pivot/Key Kanan', 'Rentang Merge Selesai', 'Selesai', 'Normal'], 
                                            range=['#6AA84F', '#F1C232', '#4A86E8', '#000000', '#999999']), # Hitam untuk Selesai
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
# ... (kode app.py bagian akhir tetap sama) ...
