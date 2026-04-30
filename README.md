# 🤖 Antigravity Memory Protocol

**Antigravity Memory Protocol** adalah sistem manajemen pengetahuan otomatis yang dirancang untuk AI Coding Agent (seperti Google Deepmind Antigravity). Sistem ini memungkinkan AI untuk memiliki "ingatan jangka panjang" terhadap keputusan arsitektur, perubahan kode, dan perkembangan proyek Anda.

## 🌟 Fitur Utama
- **Automated Harvesting**: Secara otomatis mencatat perubahan fungsi dan logika setiap kali Anda melakukan commit.
- **Universal Language Support**: Mendukung berbagai bahasa pemrograman (Python, JS/TS, Go, Rust, PHP, dll).
- **Initial Discovery Scan**: Mampu "menyedot" data dari proyek yang sudah berjalan (existing projects) untuk membangun basis pengetahuan instan.
- **Graphify Integration**: Membangun *Knowledge Graph* untuk menghubungkan relasi antar file dan keputusan arsitektur (ADR).
- **Self-Healing Documentation**: Menjaga `KNOWLEDGE_MAP.md` dan `STATE_OF_THE_UNION.md` tetap up-to-date secara otomatis.

## 🚀 Cara Instalasi (Quick Start)

1. **Copy Folder**: Salin seluruh isi paket ini ke direktori root project Anda.
2. **Jalankan Installer**: Buka terminal di root project dan jalankan:
   ```bash
   python setup.py
   ```
3. **Ikuti Instruksi**: 
   - Installer akan menginstal dependensi `graphify`.
   - Installer akan mendeteksi apakah project Anda baru atau sudah berjalan.
   - Pilih **"Y"** jika ingin melakukan *Initial Scan* pada project yang sudah ada.

## 📁 Struktur Folder
```plaintext
your-project/
├── .agent/
│   ├── rules/
│   │   └── GEMINI.md          # Aturan protokol untuk AI Agent
│   └── scripts/
│       └── antigravity_mem/   # Mesin penggerak (Harvester, Backfill, dll)
├── scripts/
│   └── sync_knowledge.py      # Orchestrator utama
└── setup.py                   # Auto-installer
```

## 🛠️ Cara Penggunaan Harian

### 1. Aktivasi Agent
Saat pertama kali memulai sesi dengan AI Agent, berikan perintah:
> "Aktifkan **Automated Memory Protocol** sesuai dengan `.agent/rules/GEMINI.md`."

### 2. Sinkronisasi Otomatis
Sistem ini dirancang untuk berjalan setiap kali Anda melakukan commit. Anda bisa meminta AI:
> "Commit dan push perubahan ini, lalu jalankan sinkronisasi memori."

Atau jalankan secara manual:
```bash
python scripts/sync_knowledge.py
```

## 📝 Catatan Penting
- **Graphify**: Membutuhkan koneksi internet saat instalasi pertama untuk menarik package dari GitHub.
- **SQLite3**: Semua data disimpan secara lokal di `.agent/memory.db`. Data Anda tetap milik Anda.

---
*Created with ❤️ by Antigravity AI for the Developer Community.*
