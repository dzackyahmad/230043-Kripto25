# Nama : Dzacky Ahmad
# NPM  : 140810230043
# Deskripsi : Program Vigenere Cipher 

# ---------- Utilitas ----------
def a2n(ch):  # A=0..Z=25 (non-huruf -> None)
    return ord(ch.upper()) - ord('A') if ch.isalpha() else None

def n2a(n, template='A'):
    ch = chr((n % 26) + ord('A'))
    return ch if template.isupper() else ch.lower()

def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    for i in range(len(text) - len(key)):
        key.append(key[i % len(key)])
    return "".join(key)

def vigenere_encrypt(plaintext, key):
    out = []
    for p, k in zip(plaintext, key):
        if p.isalpha():
            pv, kv = a2n(p), a2n(k)
            cv = (pv + kv) % 26
            out.append(n2a(cv, p))
        else:
            out.append(p)
    return "".join(out)

def vigenere_decrypt(ciphertext, key):
    out = []
    for c, k in zip(ciphertext, key):
        if c.isalpha():
            cv, kv = a2n(c), a2n(k)
            pv = (cv - kv) % 26
            out.append(n2a(pv, c))
        else:
            out.append(c)
    return "".join(out)

# ====== CETAK TABEL  ======
W_LABEL = 16   # lebar kolom label (kolom pertama)
W_CELL  = 4    # lebar setiap sel huruf/angka

def _fmt_cells(cells, align="center"):
    out = []
    for i, x in enumerate(cells):
        w = W_LABEL if i == 0 else W_CELL
        s = str(x)
        if align == "right":
            out.append(f"{s:>{w}}")
        elif align == "left":
            out.append(f"{s:<{w}}")
        else:
            out.append(f"{s:^{w}}")
    return "".join(out)

def print_enc_table(plaintext, key, ciphertext):
    # Baris 1: PT (huruf)
    print(_fmt_cells(["PT"] + list(plaintext), align="center"))

    # Baris 2: n(PT)
    npt = ["n(PT)"] + [a2n(ch) if ch.isalpha() else "-" for ch in plaintext]
    print(_fmt_cells(npt, align="right"))

    # Baris 3: n(K)
    nk = ["n(K)"] + [a2n(k) if k.isalpha() else "-" for k in key]
    print(_fmt_cells(nk, align="right"))

    # Baris 4–5: (n(PT)+n(K)) mod 26
    print(_fmt_cells(["(n(PT)+n(K))"] + [""]*len(plaintext), align="left"))
    sum_vals = []
    for p, k in zip(plaintext, key):
        if p.isalpha():
            sum_vals.append((a2n(p) + a2n(k)) % 26)
        else:
            sum_vals.append("-")
    print(_fmt_cells(["mod 26"] + sum_vals, align="right"))

    # Baris 6: CT
    print(_fmt_cells(["CT"] + list(ciphertext), align="center"))

    # Baris 7: n(CT)
    nct = ["n(CT)"] + [a2n(c) if c.isalpha() else "-" for c in ciphertext]
    print(_fmt_cells(nct, align="right"))

def print_dec_table(ciphertext, key, plaintext):
    # n(CT)
    nct = ["n(CT)"] + [a2n(c) if c.isalpha() else "-" for c in ciphertext]
    print(_fmt_cells(nct, align="right"))

    # n(K)
    nk = ["n(K)"] + [a2n(k) if k.isalpha() else "-" for k in key]
    print(_fmt_cells(nk, align="right"))

    # (n(CT)-n(K)) mod 26
    print(_fmt_cells(["(n(CT)-n(K))"] + [""]*len(ciphertext), align="left"))
    diff_vals = []
    for c, k in zip(ciphertext, key):
        if c.isalpha():
            diff_vals.append((a2n(c) - a2n(k)) % 26)
        else:
            diff_vals.append("-")
    print(_fmt_cells(["mod 26"] + diff_vals, align="right"))

    # PT
    print(_fmt_cells(["PT"] + list(plaintext), align="center"))


# ---------- Menu ----------
def main():
    print("===== PROGRAM VIGENERE CIPHER =====")
    print("1. Enkripsi (dengan tabel)")
    print("2. Dekripsi (dengan tabel)")
    print("3. Keluar")
    while True:
        ch = input("\nPilih menu (1/2/3): ").strip()
        if ch == "1":
            pt  = input("Masukkan plaintext : ").upper()
            key = input("Masukkan key       : ").upper()
            gk  = generate_key(pt, key)
            ct  = vigenere_encrypt(pt, gk)
            print("\n\t\t\t=== TABEL ENKRIPSI ===")
            print_enc_table(pt, gk, ct)
            print("\nCiphertext:", ct)
        elif ch == "2":
            ct  = input("Masukkan ciphertext: ").upper()
            key = input("Masukkan key       : ").upper()
            gk  = generate_key(ct, key)
            pt  = vigenere_decrypt(ct, gk)
            print("\n=== TABEL DEKRIPSI ===")
            print_dec_table(ct, gk, pt)
            print("\nPlaintext:", pt)
        elif ch == "3":
            print("Keluar dari Program. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
