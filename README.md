# PAITEN EX KELIPS
Deteksi bentuk dasar geometri berdasarkan *Knowledge Based System* (KBS)

## Cara Kerja Program
1. Program me*load* gambar
2. Program melakukan *feature detection* terhadap gambar
3. Akan dibuat *environment* CLIPS untuk setiap bentuk
4. Hasil *feature detection* akan diubah menjadi fakta dan di*assert* 
5. CLIPS kemudian akan dijalankan dan hasilnya disimpan
6. Hasil fakta akhir akan dicocokkan dengan *input* pengguna
7. Akan ditampilkan informasi-informasi tambahan

## Requirements
- python : ^3.7
- conda : ^4.0
    ```bash
    $ conda env create -f env.yml
    ```

## User Manual
1. Melakukan *run* program `app.py` pada *Command Line Interface* (CLI) dengan perintah berikut :
    ```base
    $ python app.py
    ```
2. Membuka gambar dengan tombol `Open Image`
3. Memilih bentuk dasar geometri dari daftar bentuk
4. Menekan tombol `Run` untuk mencari bentuk dasar geometri pada gambar
5. Dapat melakukan perubahan pada rule dengan tombol `Open Rule Editor`
6. Dapat melihat rule yang ada pada


## Author
  - 13517012 / Johanes
  - 13517039 / Steve Andreas Immanuel
  - 13517063 / Joshua Christo Randiny
  - 13517066 / Willy Santoso