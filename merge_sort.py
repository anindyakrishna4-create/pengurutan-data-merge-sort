# List global untuk menyimpan riwayat langkah
HISTORY = []

def merge_sort(data_list):
    # Bersihkan history jika dipanggil berulang kali di Streamlit
    global HISTORY
    HISTORY = []
    
    # Panggil fungsi rekursif utama
    _merge_sort_recursive(data_list, 0, len(data_list) - 1)
    
    # Tambahkan state terakhir (selesai)
    HISTORY.append({'array': data_list[:], 'highlight': (-1, -1, -1, 'Selesai'), 'action': 'Pengurutan Selesai'})
    
    return data_list, HISTORY

def _merge_sort_recursive(arr, start_idx, end_idx):
    if start_idx >= end_idx:
        return
    
    mid_idx = (start_idx + end_idx) // 2
    
    # 1. Fase Divide (Rekursi)
    _merge_sort_recursive(arr, start_idx, mid_idx)
    _merge_sort_recursive(arr, mid_idx + 1, end_idx)
    
    # 2. Fase Merge (Gabungkan)
    _merge(arr, start_idx, mid_idx, end_idx)
    
def _merge(arr, start, mid, end):
    
    left_sub = arr[start:mid + 1]
    right_sub = arr[mid + 1:end + 1]
    
    i = j = 0
    k = start # k adalah indeks gabungan di array utama

    # Proses Penggabungan (Gabungkan dua sub-array terurut)
    while i < len(left_sub) and j < len(right_sub):
        
        # Catat state saat Perbandingan
        HISTORY.append({
            'array': arr[:],
            'highlight': (start, end, start + i, mid + 1 + j, 'Bandingkan'), # Rentang, Kiri, Kanan
            'action': f'Membandingkan: Sub-array Kiri[{start+i}] dan Kanan[{mid+1+j}]'
        })
        
        if left_sub[i] <= right_sub[j]:
            arr[k] = left_sub[i]
            i += 1
        else:
            arr[k] = right_sub[j]
            j += 1
        
        k += 1

    # Tambahkan sisa elemen kiri (jika ada)
    while i < len(left_sub):
        arr[k] = left_sub[i]
        k += 1
        i += 1

    # Tambahkan sisa elemen kanan (jika ada)
    while j < len(right_sub):
        arr[k] = right_sub[j]
        k += 1
        j += 1
        
    # Catat state setelah Merge Selesai
    HISTORY.append({
        'array': arr[:],
        'highlight': (start, end, -1, -1, 'Gabung Selesai'), # start dan end: rentang yang baru diurutkan
        'action': f'MERGE SELESAI: Rentang Indeks [{start} hingga {end}] kini terurut.'
    })
    
    return arr
