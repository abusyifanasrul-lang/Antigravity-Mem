# 🤖 Antigravity Memory Protocol (Versi Bahasa Indonesia)

**Antigravity Memory Protocol** adalah sistem manajemen pengetahuan otomatis yang dirancang untuk AI Coding Agent. Sistem ini memungkinkan AI untuk memiliki "ingatan jangka panjang" terhadap keputusan arsitektur, perubahan kode, dan perkembangan proyek Anda langsung di dalam repositori.

## 🌟 Fitur Utama
- **Automated Harvesting**: Mencatat perubahan fungsi dan logika secara otomatis setiap kali Anda melakukan commit.
- **Dukungan Bahasa Universal**: Mendukung berbagai bahasa pemrograman (Python, JS/TS, Go, Rust, PHP, dll).
- **Initial Discovery Scan**: Mampu "menyedot" data dari proyek yang sudah berjalan untuk membangun konteks pengetahuan instan.
- **Integrasi Graphify**: Membangun *Knowledge Graph* untuk menghubungkan relasi antar file dan keputusan arsitektur (ADR).
- **Dokumentasi Otomatis**: Menjaga `KNOWLEDGE_MAP.md` dan `STATE_OF_THE_UNION.md` tetap terupdate.

## 🚀 Cara Instalasi Cepat

1. **Salin File**: Salin semua file dari paket ini ke direktori root proyek Anda.
2. **Jalankan Installer**: Buka terminal di root proyek dan jalankan:
   ```bash
   python setup.py
   ```
3. **Ikuti Instruksi**: 
   - Installer akan menyiapkan struktur dan dependensi secara otomatis.
   - Pilih **"Y"** jika Anda ingin melakukan *Initial Scan* pada proyek yang sudah ada.

## 🛠️ Penggunaan Harian

### 1. Aktivasi Agent
Saat memulai sesi baru dengan AI Agent, berikan perintah:
> "Aktifkan **Automated Memory Protocol** sesuai dengan `.agent/rules/GEMINI.md`."

### 2. Sinkronisasi Otomatis
Anda bisa meminta AI:
> "Commit dan push perubahan ini, lalu jalankan sinkronisasi memori."

Atau jalankan secara manual:
```bash
python scripts/sync_knowledge.py
```

---
*Dibuat dengan ❤️ oleh Antigravity AI untuk Komunitas Developer.*
