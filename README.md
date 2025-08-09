# XssemoX
XssemoX - **XSS vulnerability Testing Tool** deyang dirancang khusus untuk mendeteksi kerentanan Cross-Site Scripting (XSS) pada aplikasi web dengan custom payload support yang bekerja dengan menguji berbagai payload XSS pada parameter URL, Automated testing untuk comprehensive web application security assessment.


## Instalasi
1. **Clone repository**
   ```bash
   git clone https://github.com/username/XssemoX.git
   cd XssemoX
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Penggunaan
1. Jalankan tool:
   ```bash
   python3 main.py
   ```

2. Pilihan menu:
   - **Start Attack**: Memulai pengujian XSS pada target
   - **Input Payload**: Memasukkan file wordlist payload custom
   - **Exit**: Keluar dari program

3. Contoh menjalankan pengujian:
   - Pastikan sudah memuat wordlist payload
   - Masukkan URL target (contoh: `https://example.com/?q=test`)
   - Tool akan menguji setiap payload pada semua parameter dan menampilkan hasilnya

## Struktur Folder
```
XssemoX/
│
├── XssemoX.py            # Script utama
├── requirements.txt      # Dependencies
├── payloads.txt          # Contoh file wordlist payload
└── README.md             # Dokumentasi
```

## Dependencies
- Python 3.6+
- `requests`

## Catatan
- Tool ini dibuat untuk tujuan **pengujian keamanan**.  
  Dilarang menggunakan untuk kegiatan ilegal.
- Gunakan hanya pada sistem atau aplikasi yang Anda miliki izin untuk menguji.

## 🏗️ Arsitektur Tool
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   XssemoX Core   │───▶│   Target Web    │
│  (URL + Menu)   │    │                  │    │   Application   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Wordlist       │
                       │   Payload File   │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   HTTP Requests  │
                       │   with Payloads  │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Response       │
                       │   Analysis       │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Vulnerability  │
                       │   Detection      │
                       └──────────────────┘
```
## Lisensi
MIT License
