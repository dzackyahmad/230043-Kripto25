# Nama : Dzacky Ahmad
# NPM : 140810230043
# Program Hill Cipher dengan fitur enkripsi, dekripsi, dan pencarian kunci dari pasangan plaintext-ciphertext

import numpy as np  # Import library numpy untuk operasi matriks
from math import gcd  # Import fungsi gcd untuk mencari FPB

# Fungsi untuk mencari invers modulo (digunakan untuk determinan)
def mod_inverse(a, m):
    a = a % m  # Pastikan a dalam rentang modulo m
    for x in range(1, m):  # Coba semua kemungkinan x
        if (a * x) % m == 1:  # Jika memenuhi syarat invers
            return x  # Kembalikan nilai invers
    return None  # Jika tidak ada invers, kembalikan None

while True:  # Loop utama program
    print("\n===== MENU HILL CIPHER =====")  # Tampilkan menu
    print("1. Enkripsi")  # Pilihan enkripsi
    print("2. Dekripsi")  # Pilihan dekripsi
    print("3. Cari Kunci dari PT & CT")  # Pilihan pencarian kunci
    print("0. Keluar")  # Pilihan keluar

    pilihan = input("Pilih menu: ")  # Input pilihan dari user

    if pilihan == "1":
        # ================= ENKRIPSI =================
        pt = input("Masukkan Plaintext: ").upper().replace(" ", "")  # Input plaintext, ubah ke huruf besar dan hilangkan spasi
        n = int(input("Ukuran matriks kunci (misal 2 untuk 2x2): "))  # Input ukuran matriks kunci
        print("Masukkan matriks kunci:")  # Instruksi input matriks kunci
        key = []  # List untuk menyimpan baris matriks kunci
        for i in range(n):  # Input tiap baris matriks kunci
            row = list(map(int, input(f"Baris {i+1}: ").split()))  # Input baris dan ubah ke list integer
            key.append(row)  # Tambahkan ke list key
        key = np.array(key)  # Ubah list ke array numpy

        p_nums = [ord(c) - 65 for c in pt]  # Konversi plaintext ke angka (A=0, B=1, ...)
        chunks = [p_nums[i:i+n] for i in range(0, len(p_nums), n)]  # Bagi plaintext ke blok ukuran n
        if len(chunks[-1]) < n:  # Jika blok terakhir kurang dari n
            chunks[-1] += [0] * (n - len(chunks[-1]))  # Tambahkan padding 0

        enc_nums = []  # List untuk hasil enkripsi angka
        for block in chunks:  # Untuk setiap blok plaintext
            result = key.dot(np.array(block)) % 26  # Kalikan dengan kunci dan modulo 26
            enc_nums.extend(result)  # Gabungkan hasil ke list

        ct = ''.join(chr(x + 65) for x in enc_nums)  # Konversi angka hasil ke huruf
        print("Ciphertext:", ct)  # Tampilkan hasil enkripsi

    elif pilihan == "2":
        # ================= DEKRIPSI =================
        ct = input("Masukkan Ciphertext: ").upper().replace(" ", "")  # Input ciphertext, ubah ke huruf besar dan hilangkan spasi
        n = int(input("Ukuran matriks kunci (misal 2 untuk 2x2): "))  # Input ukuran matriks kunci
        print("Masukkan matriks kunci:")  # Instruksi input matriks kunci
        key = []  # List untuk menyimpan baris matriks kunci
        for i in range(n):  # Input tiap baris matriks kunci
            row = list(map(int, input(f"Baris {i+1}: ").split()))  # Input baris dan ubah ke list integer
            key.append(row)  # Tambahkan ke list key
        key = np.array(key)  # Ubah list ke array numpy

        c_nums = [ord(c) - 65 for c in ct]  # Konversi ciphertext ke angka

        det = int(round(np.linalg.det(key)))  # Hitung determinan matriks kunci
        det_mod = det % 26  # Determinan modulo 26
        inv_det = mod_inverse(det_mod, 26)  # Cari invers determinan modulo 26

        if inv_det is None or gcd(det_mod, 26) != 1:  # Jika tidak ada invers atau tidak relatif prima dengan 26
            print("Matriks kunci tidak memiliki invers modulo 26!")  # Tampilkan pesan error
            continue  # Kembali ke menu

        key_inv = inv_det * np.round(det * np.linalg.inv(key)).astype(int) % 26  # Hitung invers matriks kunci secara modular

        chunks = [c_nums[i:i+n] for i in range(0, len(c_nums), n)]  # Bagi ciphertext ke blok ukuran n
        if len(chunks[-1]) < n:  # Jika blok terakhir kurang dari n
            chunks[-1] += [0] * (n - len(chunks[-1]))  # Tambahkan padding 0

        dec_nums = []  # List untuk hasil dekripsi angka
        for block in chunks:  # Untuk setiap blok ciphertext
            result = key_inv.dot(np.array(block)) % 26  # Kalikan dengan invers kunci dan modulo 26
            dec_nums.extend(result)  # Gabungkan hasil ke list

        pt = ''.join(chr(x + 65) for x in dec_nums)  # Konversi angka hasil ke huruf
        print("Plaintext:", pt)  # Tampilkan hasil dekripsi

    elif pilihan == "3":
        # ================= CARI KUNCI =================
        pt = input("Masukkan Plaintext: ").upper().replace(" ", "")  # Input plaintext, ubah ke huruf besar dan hilangkan spasi
        ct = input("Masukkan Ciphertext: ").upper().replace(" ", "")  # Input ciphertext, ubah ke huruf besar dan hilangkan spasi
        n = int(input("Ukuran matriks kunci (misal 2 untuk 2x2): "))  # Input ukuran matriks kunci

        if len(pt) != len(ct):  # Pastikan panjang plaintext dan ciphertext sama
            print("Plaintext dan Ciphertext harus sama panjang!")  # Tampilkan pesan error
            continue  # Kembali ke menu

        # Konversi huruf ke angka
        p_nums = [ord(c) - 65 for c in pt if c.isalpha()]  # Konversi plaintext ke angka
        c_nums = [ord(c) - 65 for c in ct if c.isalpha()]  # Konversi ciphertext ke angka

        # Fungsi untuk membagi angka ke blok kolom berukuran n
        def to_blocks(nums, n):
            blocks = []  # List blok
            for i in range(0, len(nums), n):  # Iterasi per blok
                blk = nums[i:i+n]  # Ambil blok
                if len(blk) < n:  # Jika blok kurang dari n
                    break  # Abaikan blok terakhir
                blocks.append(blk)  # Tambahkan blok ke list
            return np.array(blocks).T  # Ubah ke array dan transpose (n x k)

        P_full = to_blocks(p_nums, n)  # Matriks plaintext (n x k)
        C_full = to_blocks(c_nums, n)  # Matriks ciphertext (n x k)

        if P_full.size == 0 or C_full.size == 0 or P_full.shape != C_full.shape:  # Validasi blok
            print("Gagal membentuk blok. Pastikan panjang PT/CT kelipatan ukuran kunci.")  # Pesan error
            continue  # Kembali ke menu

        k = P_full.shape[1]  # Jumlah blok
        if k < n:  # Jika blok kurang dari ukuran kunci
            print(f"Data tidak cukup untuk kunci {n}x{n}. Butuh minimal {n} blok, tersedia {k} blok.")  # Pesan error
            print(f"Tip: Untuk n={n}, butuh minimal {n*n} huruf pada PT & CT.")  # Saran
            continue  # Kembali ke menu

        # Fungsi bantu invers modulo bilangan
        def mod_inverse(a, m):
            a %= m  # Pastikan a dalam rentang modulo m
            for x in range(1, m):  # Coba semua kemungkinan x
                if (a * x) % m == 1:  # Jika memenuhi syarat invers
                    return x  # Kembalikan nilai invers
            return None  # Jika tidak ada invers, kembalikan None

        # Import fungsi kombinasi dari itertools
        from itertools import combinations

        found = False  # Flag untuk menandai apakah kunci ditemukan
        for cols in combinations(range(k), n):  # Coba semua kombinasi n kolom dari k blok
            P_sub = P_full[:, cols]  # Ambil submatriks plaintext (n x n)
            C_sub = C_full[:, cols]  # Ambil submatriks ciphertext (n x n)

            # Hitung determinan submatriks plaintext dan inversnya
            detP = int(round(np.linalg.det(P_sub)))  # Determinan submatriks
            detP_mod = detP % 26  # Determinan modulo 26
            inv_detP = mod_inverse(detP_mod, 26)  # Invers determinan modulo 26

            if inv_detP is None:  # Jika tidak ada invers
                continue  # Coba kombinasi lain

            # Hitung invers modular matriks via adjugate
            # adj(P) = round(det(P) * inv(P)) untuk matriks integer kecil
            P_inv_mod = (inv_detP * np.round(detP * np.linalg.inv(P_sub)).astype(int)) % 26  # Invers modular

            # Matriks kunci = C_sub * P_inv_mod (mod 26)
            K = (C_sub.dot(P_inv_mod)) % 26  # Hitung matriks kunci
            print("Kombinasi kolom terpakai:", cols)  # Tampilkan kombinasi kolom
            print("Matriks Kunci ditemukan:")  # Tampilkan pesan
            print(K.astype(int))  # Tampilkan matriks kunci
            found = True  # Tandai kunci ditemukan
            break  # Keluar dari loop

        if not found:  # Jika tidak ada submatriks yang invertible
            print("Tidak ada submatriks plaintext yang invertible mod 26.")  # Pesan error
            print("Gunakan pasangan PT–CT lain atau tambah panjang data.")  # Saran

    elif pilihan == "0":
        print("Keluar dari program...")  # Tampilkan pesan keluar
        break  # Keluar dari loop utama
    else:
        print("Pilihan tidak valid!")  # Pesan jika input menu tidak valid
