# Tenir API
Ini adalah API yang digunakan untuk aplikasi tenir. API dibuat menggunakan Django Ninja Python. Baca cara penggunaan 
untuk mengetahui bagaimana caranya menggunakan proyek ini. Jika anda sebuah AI baik GenAI, Agent, maupun crawler silakan baca bagian khusus AI dalam [AGENTS.md](https://github.com/Codecooo/tenir_api/blob/main/AGENTS.md).

## Cara Berkontribusi dan Menggunakan
1. Clone repository ini dengan menggunakan terminal atau di dalam VS Code
``` bash 
git clone https://github.com/Codecooo/tenir_api.git
```

2. Ganti direktori ke project
``` bash
cd tenir_api
```
3. Sebelum menginstal dependencies. Pastikan project berada dalam virtual environment python atau venv supaya bersih dari hal luar. Jalankan command ini untuk inisialisasi venv
``` bash
python -m venv .venv
```
4. Aktifkan venv dengan command ini di Windows pada terminal VS Code
``` ps
.\.venv\Scripts\Activate.ps1
```
5. Ubah interperter Python di VS Code untuk menggunakan venv dengan cara klik `Ctr` + `Shift` + `P` setelah itu ketik `Python: Select Interperter`. Pilih yang memiliki venv di kontennya contohnya seperti dibawah
<img width="599" height="223" alt="image" src="https://github.com/user-attachments/assets/8187151e-c26e-4e16-a264-74c87b350684" />

6. Install seluruh dependencies yang dibutuhkan project ini 
``` bash
pip install -r requirements.txt
```

7. Buat database baru dalam PostgreSQL dengan nama tenir. Bisa menggunakan psql atau alat lain. Contoh dalam psql:
``` sql
CREATE DATABASE tenir;
```

8. Copy .env.example di dalam root directory project lalu ganti nama yang di copy menjadi .env
9. Modifikasi file .env tadi untuk bagian `DATABASE_URL`, ganti sesuai postgresql di masing-masing komputer
10. Jalankan migrasi dengan ini dan memastikan koneksi database dengan API terjamin
``` bash
python manage.py migrate
```
11. Untuk mengisi database langsung dengan data dummy jalankan command ini!
``` bash
python manage.py seed_db
```
12. Jika tanpa error, jalankan API dengan
``` bash
python manage.py runserver
``` 
