# i.	Implementasi Algoritma Greedy
# Algoritma Greedy yang diimplementasikan dalam kode ini adalah strategi untuk memainkan permainan Diamonds. Strategi ini memprioritaskan pengumpulan berlian, pengamanan skor, dan interaksi strategis dengan elemen papan seperti musuh, Red Button, dan teleporter. Algoritma ini menggunakan beberapa fungsi untuk menentukan langkah terbaik, seperti:
# •	_find_best_diamond:Mencari berlian terbaik berdasarkan jarak dan jenis berlian. Fungsi ini memprioritaskan berlian merah yang berada dalam radius 5 langkah dari bot.
# •	_find_enemy: Mencari musuh yang berada di sekitar bot. Fungsi ini memeriksa apakah ada musuh yang berada dalam jarak 1 langkah dari bot.
# •	_can_use_red_button: Menentukan apakah Red Button dapat digunakan. Fungsi ini memeriksa apakah Red Button berada dalam jarak 2 langkah dari bot dan apakah jumlah berlian di papan kurang dari 5.
# •	_find_better_teleporter: Mencari teleporter yang dapat mempersingkat jalur ke tujuan. Fungsi ini memeriksa apakah ada teleporter yang dapat mempersingkat jalur ke tujuan dan memilih teleporter yang paling efisien.
# Algoritma ini juga menggunakan beberapa variabel untuk menyimpan informasi tentang keadaan permainan, seperti:
# •	goal_position: Menyimpan posisi tujuan bot saat ini.
# •	tackle_cooldown: Menyimpan waktu cooldown untuk tackle musuh.
# •	bot_id: Menyimpan ID bot.

# ii.	Requirement Program
# •	Python 3.x: Bahasa pemrograman yang digunakan untuk mengembangkan bot.
# •	Game Engine Diamonds: Engine permainan yang digunakan untuk menjalankan permainan Diamonds.
# •	Bot Starter Pack: Paket yang berisi kode dasar untuk bot dan API untuk berinteraksi dengan Game Engine.

# iii.	Langkah-langkah Meng-compile atau Build Program
# •	Pastikan Python 3.x telah terinstal di sistem Anda.
# •	Unduh dan instal Game Engine Diamonds dan Bot Starter Pack.
# •	Buat file Bowtie.py dan salin kode program ke dalamnya.
# •	Letakkan file Bowtie.py di direktori yang sesuai di dalam Bot Starter Pack.
# •	Jalankan perintah python main.py di terminal atau command prompt untuk menjalankan Game Engine.
# •	Bot "Bowtie" akan berjalan secara otomatis dan memainkan permainan Diamonds menggunakan algoritma Greedy.

# iv.	Author
# Kelompok 3psilon
# •	Mekar Cendra Narwastu (123140074)
# •	Mei Disti Ayuningtias (123140076)
# •	Afrilia Dwi Amnesti (123140079)
