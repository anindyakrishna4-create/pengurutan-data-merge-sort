# File: merge_sort.py

# List global untuk menyimpan riwayat langkah
HISTORY = []

def merge_sort(data_list):
    """
    Mengimplementasikan Merge Sort, menggunakan array copy untuk memastikan
    modifikasi in-place dicatat dengan benar di history.
    """
    global HISTORY
    HISTORY = []
    
    # Membuat salinan array untuk dimodifikasi secara in-place
    data_to_sort = data_list[:] 
    n = len(data_to_sort)
    
    # Panggil fungsi rekursif utama
    _merge_sort_recursive(data_to_sort, 0, n - 1)
    
    # Tambahkan state terakhir (selesai)
    # Highlight: 5 elemen konsisten (-1, -1, -1, -1, 'Selesai')
    HISTORY.append({'array': data_to_sort[:], 'highlight': (-1, -1, -1, -1, 'Selesai'), 'action': 'Pengurutan Selesai'})
    
    # Kembalikan array yang sudah terurut.
    return data_to_sort, HISTORY

def _merge_sort_recursive(arr, start_idx, end_idx):
    if start_idx >= end_idx:
        return
    
    mid_idx = (start_idx + end_idx) // 2
    
    # Fase Divide (Rekursi)
    _merge_sort_recursive(arr, start_idx, mid_idx)
    _merge_sort_recursive(arr, mid_idx + 1, end_idx)
    
    # Fase Merge (Gabungkan)
    _merge(arr, start_idx, mid_idx, end_idx)
    
def _merge(arr, start, mid, end):
    
    left_sub = arr[start:mid + 1]
    right_sub = arr[mid + 1:end + 1]
    
    i = j = 0
    k = start # k adalah indeks di array utama (arr)

    # Proses Penggabungan
    while i < len(left_sub) and j < len(right_sub):
        
        # Catat state saat Perbandingan
        HISTORY.append({
            'array': arr[:],
            'highlight': (start, end, start + i, mid + 1 + j, 'Bandingkan'), 
            'action': f'Membandingkan: Sub-array Kiri[{start+i}] ({left_sub[i]}) dan Kanan[{mid+1+j}] ({right_sub[j]})'
        })
        
        if left_sub[i] <= right_sub[j]:
            arr[k] = left_sub[i]
            i += 1
        else:
            arr[k] = right_sub[j]
            j += 1
        
        k += 1

    # Tambahkan sisa elemen
    while i < len(left_sub):
        arr[k] = left_sub[i]
        k += 1
        i += 1
    while j < len(right_sub):
        arr[k] = right_sub[j]
        k += 1
        j += 1
        
    # Catat state setelah Merge Selesai
    HISTORY.append({
        'array': arr[:],
        # Konsisten: 5 elemen
        'highlight': (start, end, -1, -1, 'Gabung Selesai'), 
        'action': f'MERGE SELESAI: Rentang Indeks [{start} hingga {end}] kini terurut.'
    })
    
    return arr
