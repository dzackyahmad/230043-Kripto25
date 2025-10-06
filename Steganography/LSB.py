# Nama : Dzacky Ahmad
# NPM : 140810230043
# Deskripsi Progeam : Steganografi LSB pada gambar RGB

import os                      # Import modul os untuk operasi file/path
from typing import List, Tuple # Import typing untuk anotasi tipe data
from PIL import Image          # Import Pillow untuk manipulasi gambar

def bytes_to_bits(data: bytes) -> List[int]:
    """Ubah bytes -> list bit (MSB ke LSB per byte)."""
    bits = []                                  # Inisialisasi list penampung bit
    for b in data:                             # Iterasi setiap byte dalam data
        for i in range(7, -1, -1):             # Iterasi dari bit ke-7 sampai ke-0
            bits.append((b >> i) & 1)          # Ambil bit ke-i dan tambahkan ke list
    return bits                                # Kembalikan list bit

def bits_to_bytes(bits: List[int]) -> bytes:
    """Ubah list bit (kelipatan 8) -> bytes."""
    if len(bits) % 8 != 0:                     # Validasi panjang bit harus kelipatan 8
        raise ValueError("Panjang bit tidak kelipatan 8.")  # Raise error jika tidak
    out = bytearray()                          # Inisialisasi buffer hasil bytes
    for i in range(0, len(bits), 8):           # Proses setiap 8 bit
        v = 0                                  # Inisialisasi nilai byte
        for bit in bits[i:i+8]:                # Loop 8 bit
            v = (v << 1) | (bit & 1)           # Geser dan gabung bit
        out.append(v)                          # Tambahkan byte ke buffer
    return bytes(out)                          # Kembalikan hasil sebagai bytes

def int_to_32bit(n: int) -> List[int]:
    """Ubah int (0..2^32-1) -> 32 bit big-endian."""
    if not (0 <= n < (1 << 32)):               # Validasi rentang integer
        raise ValueError("Header di luar rentang 32-bit.")   # Raise error jika tidak
    return bytes_to_bits(n.to_bytes(4, "big")) # Konversi int ke 4 byte, lalu ke bit

def bits32_to_int(bits: List[int]) -> int:
    """Ubah 32 bit big-endian -> int."""
    if len(bits) != 32:                        # Validasi panjang bit harus 32
        raise ValueError("Header bukan 32 bit.")             # Raise error jika tidak
    return int.from_bytes(bits_to_bytes(bits), "big")        # Konversi bit ke int

# -----------------------------
# Utilitas gambar & kapasitas
# -----------------------------

def load_image_rgb(path: str) -> Image.Image:
    """Muat gambar & pastikan mode RGB (lossless disarankan)."""
    img = Image.open(path)                     # Buka file gambar
    if img.mode != "RGB":                      # Jika mode bukan RGB
        img = img.convert("RGB")               # Konversi ke RGB
    return img                                 # Kembalikan objek Image

def get_capacity_bits(img: Image.Image) -> int:
    """Kapasitas bit = jumlah piksel × 3 channel."""
    w, h = img.size                            # Ambil ukuran gambar
    return w * h * 3                           # Hitung kapasitas bit (R,G,B)

def flatten_rgb(img: Image.Image) -> List[int]:
    """Flatten RGB -> list channel [R0,G0,B0, R1,G1,B1, ...]."""
    flat = []                                  # Inisialisasi list channel
    for r, g, b in img.getdata():              # Iterasi setiap piksel
        flat.extend([r, g, b])                 # Tambahkan nilai R,G,B ke list
    return flat                                # Kembalikan list channel

def unflatten_rgb(flat: List[int], size: Tuple[int, int]) -> Image.Image:
    """Bangun Image RGB dari list channel & ukuran."""
    if len(flat) % 3 != 0:                     # Validasi data channel kelipatan 3
        raise ValueError("Data channel tidak kelipatan 3.")  # Raise error jika tidak
    pixels = []                                # Inisialisasi list piksel
    for i in range(0, len(flat), 3):           # Iterasi setiap 3 channel
        pixels.append((flat[i], flat[i+1], flat[i+2]))       # Gabung jadi tuple RGB
    img = Image.new("RGB", size)               # Buat canvas gambar baru
    img.putdata(pixels)                        # Set data piksel ke gambar
    return img                                 # Kembalikan objek Image

# -----------------------------
# Inti: LSB Encode / Decode
# -----------------------------

def encode_message_to_image(cover_path: str, out_path: str, message: str) -> int:
    """Sisipkan 'message' ke dalam cover & simpan PNG; return jumlah byte."""
    img = load_image_rgb(cover_path)           # Muat gambar cover
    w, h = img.size                            # Simpan ukuran gambar
    flat = flatten_rgb(img)                    # Flatten channel gambar

    data = message.encode("utf-8")             # Encode pesan ke bytes
    header_bits = int_to_32bit(len(data))      # Buat header 32-bit (panjang pesan)
    payload_bits = bytes_to_bits(data)         # Konversi payload ke bit
    all_bits = header_bits + payload_bits      # Gabungkan header dan payload

    if len(all_bits) > len(flat):              # Validasi kapasitas gambar
        max_bytes = max((len(flat) - 32) // 8, 0)            # Hitung maksimal byte
        raise ValueError(f"Pesan terlalu besar. Maks ≈ {max_bytes} byte.")  # Raise error jika pesan terlalu besar

    stego_flat = flat[:]                       # Salin channel gambar
    for i, bit in enumerate(all_bits):         # Iterasi setiap bit yang akan disisipkan
        stego_flat[i] = (stego_flat[i] & 0xFE) | bit         # Sisipkan bit ke LSB channel

    stego_img = unflatten_rgb(stego_flat, (w, h))            # Rekonstruksi gambar stego
    root, _ = os.path.splitext(out_path)       # Pisahkan nama dan ekstensi file output
    safe_out = root + ".png"                   # Paksa output ke PNG (lossless)
    stego_img.save(safe_out, "PNG")            # Simpan gambar stego
    return len(data)                           # Kembalikan jumlah byte pesan yang disisipkan

def decode_message_from_image(stego_path: str) -> str:
    """Ekstrak pesan teks dari gambar stego (UTF-8 / fallback hex)."""
    img = load_image_rgb(stego_path)           # Muat gambar stego
    flat = flatten_rgb(img)                    # Flatten channel gambar

    header_bits = [(flat[i] & 1) for i in range(32)]         # Ambil 32 bit pertama sebagai header
    nbytes = bits32_to_int(header_bits)        # Konversi header ke panjang payload (byte)

    need = 32 + nbytes * 8                     # Hitung total bit yang diperlukan
    if need > len(flat):                       # Validasi kapasitas gambar
        raise ValueError("Payload tidak lengkap / bukan stego valid.")     # Raise error jika payload tidak lengkap

    payload_bits = [(flat[32+i] & 1) for i in range(nbytes * 8)]           # Ambil bit payload
    payload = bits_to_bytes(payload_bits)      # Konversi bit payload ke bytes
    try:
        return payload.decode("utf-8")         # Decode payload ke string UTF-8
    except UnicodeDecodeError:
        return payload.hex()                   # Jika gagal, kembalikan payload dalam bentuk hex

# -----------------------------
# CLI: Menu interaktif
# -----------------------------

def menu_loop() -> None:
    """Loop menu 1) Encode 2) Decode 3) Keluar."""
    while True:                                                # Loop utama menu
        print("\n=== Steganografi LSB (CLI) ===")              # Tampilkan judul menu
        print("1. Encode")                                     # Tampilkan opsi Encode
        print("2. Decode")                                     # Tampilkan opsi Decode
        print("3. Keluar")                                     # Tampilkan opsi Keluar
        choice = input("Pilih menu [1/2/3]: ").strip()         # Baca input pilihan menu

        if choice == "1":                                      # Jika pilih Encode
            cover = input("Masukkan Nama File Cover Object (contoh: gambar.png): ").strip()
            cover_path = os.path.join("Cover Object", cover)   # Gabungkan path folder dan nama file

            if not os.path.isfile(cover_path):                 # Validasi file cover ada
                print("! File cover tidak ditemukan di folder Cover Object.")
                continue

            pesan = input("Masukkan Pesan: ").rstrip("\n")     # Baca pesan dari user
            if not pesan:                                      # Validasi pesan tidak kosong
                print("! Pesan tidak boleh kosong.")
                continue

            os.makedirs("Stego Object", exist_ok=True)         # Pastikan folder output ada
            base, _ = os.path.splitext(cover)                  # Ambil nama file tanpa ekstensi
            out_path = os.path.join("Stego Object", f"{base}_stego.png")  # Buat path output

            try:
                n = encode_message_to_image(cover_path, out_path, pesan)  # Encode pesan ke gambar
                print(f"✓ Berhasil. {n} byte tersisip → {out_path}")      # Tampilkan pesan sukses
            except Exception as e:
                print(f"! Gagal encode: {e}")                              # Tampilkan pesan error

        elif choice == "2":                                    # Jika pilih Decode
            stego = input("Masukkan Nama File Stego Object (contoh: gambar_stego.png): ").strip()
            stego_path = os.path.join("Stego Object", stego)   # Gabungkan path folder dan nama file

            if not os.path.isfile(stego_path):                 # Validasi file stego ada
                print("! File stego tidak ditemukan di folder Stego Object.")
                continue

            try:
                msg = decode_message_from_image(stego_path)    # Decode pesan dari gambar stego
                print("✓ Pesan Terbaca:")                      # Tampilkan pesan sukses
                print(msg)                                     # Tampilkan pesan yang terbaca
            except Exception as e:
                print(f"! Gagal decode: {e}")                  # Tampilkan pesan error

        elif choice == "3":                                    # Jika pilih Keluar
            print("Terimakasih!.")                             # Tampilkan pesan keluar
            break                                              # Keluar dari loop menu

        else:                                                  # Jika pilihan tidak valid
            print("! Pilihan tidak valid. Masukkan 1/2/3.")    # Tampilkan pesan error

# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":      # Jika file dijalankan langsung
    menu_loop()                 # Jalankan menu interaktif CLI

