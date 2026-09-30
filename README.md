# Tenir API
Ini adalah API yang digunakan untuk aplikasi tenir. API dibuat menggunakan Django Ninja Python. Baca cara penggunaan 
untuk mengetahui bagaimana caranya menggunakan proyek ini. Jika anda sebuah AI baik GenAI, Agent, maupun crawler silakan baca bagian khusus AI dalam [AGENTS.md](https://github.com/Codecooo/tenir_api/blob/main/AGENTS.md).

## Cara Berkontribusi dan Menggunakan
1. Clone repository ini dengan menggunakan terminal atau di dalam VS Code
<br>
``` bash 
git clone https://github.com/Codecooo/tenir_api.git
```
2. Ganti direktori ke project
``` bash
cd tenir_api
```

3. Install seluruh dependencies yang dibutuhkan project ini 
``` bash
pip install -r requirements.txt
```

4. Buat database baru dalam PostgreSQL dengan nama tenir. Bisa menggunakan psql atau alat lain. Contoh dalam psql:
``` sql
CREATE DATABASE tenir;
```

5. Copy .env.example di dalam root directory project lalu ganti nama yang di copy menjadi .env
6. Modifikasi file .env tadi untuk bagian `DATABASE_URL`, ganti sesuai postgresql di masing-masing komputer