# Nama : Dzacky Ahmad
# NPM  : 140810230043
# Deskripsi : Program ElGamal dengan output tabel & pasangan


from typing import List, Tuple

# ---------- Utilitas ----------

def egcd(a: int, b: int) -> Tuple[int, int, int]:
    # Extended Euclidean Algorithm untuk mencari gcd dan koefisien x, y
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int:
    # Mencari invers modular dari a mod m
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"Tidak ada invers modular untuk {a} mod {m}")
    return x % m

def powmod(base: int, exp: int, mod: int) -> int:
    # Perpangkatan modular (base^exp mod mod)
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

# ---------- Mapping teks <-> angka ----------

def char_to_num(ch: str) -> int:
    # Konversi karakter alfabet ke angka (A=0, ..., Z=25)
    if ch.isalpha():
        return ord(ch.upper()) - ord('A')
    return -1  # Untuk karakter non-alfabet

def num_to_char(n: int, template: str = 'A') -> str:
    # Konversi angka ke karakter, mengikuti case dari template
    ch = chr((n % 26) + ord('A'))
    return ch if template.isupper() else ch.lower()

# ---------- Kunci publik/pribadi ----------

def public_key(g: int, p: int, x: int) -> int:
    # Hitung kunci publik y = g^x mod p
    return powmod(g, x, p)

# ---------- Enkripsi & Dekripsi ----------

def elgamal_encrypt(plaintext: str, p: int, g: int, x: int, k: int) -> Tuple[int, List[int]]:
    # Proses enkripsi ElGamal
    y  = public_key(g, p, x)           # Hitung kunci publik
    c1 = powmod(g, k, p)               # Hitung c1 = g^k mod p
    s  = powmod(y, k, p)               # Hitung shared secret s = y^k mod p

    print("\n=== Tabel Enkripsi ===")
    print(f"{'i':>2} {'ch':^3} {'m_i':>4} {'c2_i':>6}")
    c2_list: List[int] = []
    for i, ch in enumerate(plaintext):
        m = char_to_num(ch)            # Konversi karakter ke angka
        if m == -1:
            c2_list.append(-1)         # Simpan -1 untuk karakter non-alfabet
            print(f"{i:>2} {ch:^3} {'-':>4} {'-':>6}")
        else:
            c2 = (m * s) % p           # Hitung c2_i = m_i * s mod p
            c2_list.append(c2)
            print(f"{i:>2} {ch:^3} {m:>4} {c2:>6}")

    print("\nCiphertext (pasangan c1,c2_i):")
    print(" " + ",".join("(_)" if c==-1 else f"({c1},{c})" for c in c2_list))
    return c1, c2_list

def elgamal_decrypt(c1: int, c2_list: List[int], p: int, x: int, original_text_template: str) -> str:
    # Proses dekripsi ElGamal
    s = powmod(c1, x, p)               # Hitung shared secret s = c1^x mod p
    s_inv = modinv(s, p)               # Hitung invers modular dari s

    print("\n=== Tabel Dekripsi ===")
    print(f"{'i':>2} {'tmpl':^5} {'c2_i':>6} {'m_i':>6} {'ch':^3}")
    result_chars: List[str] = []
    for i, (ch, c2) in enumerate(zip(original_text_template, c2_list)):
        if c2 == -1:
            result_chars.append(ch)     # Karakter non-alfabet, langsung ambil dari template
            print(f"{i:>2} {ch:^5} {'-':>6} {'-':>6} {ch:^3}")
        else:
            m = (c2 * s_inv) % p       # Hitung m_i = c2_i * s_inv mod p
            out_ch = num_to_char(m, template=ch)  # Konversi angka ke karakter
            result_chars.append(out_ch)
            print(f"{i:>2} {ch:^5} {c2:>6} {m:>6} {out_ch:^3}")

    plaintext = "".join(result_chars)
    print("\nPlaintext hasil dekripsi:", plaintext)
    return plaintext

# ---------- Parser Ciphertext ----------

def parse_c2_list(s: str) -> List[int]:
    # Parse input ciphertext menjadi list integer c2
    txt = s.strip()
    out: List[int] = []

    if "(" in txt and ")" in txt:  # format (c1,c2)
        i = 0
        while i < len(txt):
            if txt[i] == '(':
                j = txt.find(')', i)
                content = txt[i+1:j]
                parts = content.replace(",", " ").split()
                out.append(int(parts[1]))  # Ambil c2 dari pasangan
                i = j + 1
            else:
                if txt[i:i+3] == "(_)":
                    out.append(-1)         # Simpan -1 untuk karakter non-alfabet
                    i += 3
                else:
                    i += 1
        return out

    raw = txt.replace(",", " ").split()
    for tok in raw:
        if tok in {"(_)", "_", "-"}:
            out.append(-1)
        else:
            out.append(int(tok))
    return out

# ---------- Menu CLI ----------

def menu():
    # Menu utama CLI
    print("===== PROGRAM ELGAMAL (Latihan Z_p) =====")
    print("Output: Tabel per langkah + pasangan (c1,c2_i)\n")

    while True:
        print("Menu:")
        print(" 1. Enkripsi")
        print(" 2. Dekripsi")
        print(" 3. Keluar")
        choice = input("Pilih (1/2/3): ").strip()

        if choice == "1":
            # Input parameter enkripsi
            p = int(input("Masukkan p (prima): ").strip())
            g = int(input("Masukkan g (generator): ").strip())
            x = int(input("Masukkan x (kunci privat): ").strip())
            k = int(input("Masukkan k (nonce acak): ").strip())
            plaintext = input("Masukkan plaintext: ")

            elgamal_encrypt(plaintext, p, g, x, k)

        elif choice == "2":
            # Input parameter dekripsi
            p = int(input("Masukkan p (prima): ").strip())
            x = int(input("Masukkan x (kunci privat): ").strip())
            c1 = int(input("Masukkan c1: ").strip())
            template = input("Masukkan template teks asli: ")
            c2_str = input("Masukkan daftar C2:\n> ")

            c2_list = parse_c2_list(c2_str)
            if len(c2_list) != len(template):
                print("[!] Panjang C2 tidak sama dengan panjang template teks.")
                continue
            elgamal_decrypt(c1, c2_list, p, x, template)

        elif choice == "3":
            print("Selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.\n")

# ---------- Entry point ----------

if __name__ == "__main__":
    # Jalankan menu jika file dieksekusi langsung
    menu()
