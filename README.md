### Nama: Revaldi Enzha Agviandry P
### NIM: H1D024094
### Shift KRS: C
### Shift Baru: C

# Sistem Fuzzy Penilaian Kelayakan Spesifikasi PC untuk Game Berat

Program Python berbasis GUI (Tkinter) yang menggunakan **logika fuzzy** untuk menilai apakah spesifikasi sebuah PC atau laptop cukup layak untuk menjalankan game-game berat modern. Pengguna memasukkan nilai spesifikasi perangkatnya, lalu sistem akan menghitung skor kelayakan dan memberikan label hasil secara otomatis.

---

## Struktur Program
### 1. Definisi Variabel Fuzzy

```python
ram=ctrl.Antecedent(np.arange(4, 33, 1),'ram')
vram=ctrl.Antecedent(np.arange(2, 13, 1),'vram')
cpu=ctrl.Antecedent(np.arange(2.0, 5.1, 0.1),'cpu')
storage=ctrl.Antecedent(np.arange(50, 501, 1),'storage')
kelayakan=ctrl.Consequent(np.arange(0, 101, 1),'kelayakan')
```

Bagian ini mendefinisikan semua variabel fuzzy menggunakan `ctrl.Antecedent` untuk input dan `ctrl.Consequent` untuk output. `np.arange` menentukan *universe of discourse* — rentang nilai yang valid untuk setiap variabel. Misalnya RAM memiliki rentang 4 hingga 32 GB, yang mencakup dari laptop entry-level hingga workstation kelas atas.

---

### 2. Fungsi Keanggotaan

```python
ram['rendah'] = fuzz.trapmf(ram.universe, [4,  4,  6,  10])
ram['sedang'] = fuzz.trimf(ram.universe,  [8,  12, 16])
ram['tinggi'] = fuzz.trapmf(ram.universe, [14, 20, 32, 32])
```

Setiap variabel input dibagi menjadi tiga kategori linguistik: **rendah**, **sedang**, dan **tinggi** (untuk storage: **kecil**, **cukup**, **besar**). Program menggunakan dua jenis membership function:

- `trapmf` (trapezoid) — dipakai untuk kategori di ujung rentang (rendah dan tinggi), karena nilainya "pasti rendah" atau "pasti tinggi" di tepi-tepi ekstrem.
- `trimf` (segitiga) — dipakai untuk kategori tengah (sedang), karena nilainya hanya "paling sedang" di satu titik puncak dan menurun ke dua sisi.

Output `kelayakan` dibagi menjadi empat kategori: **tidak_layak** (0–30), **kurang_layak** (20–50), **cukup_layak** (40–72), dan **layak** (65–100).

---

### 3. Aturan Fuzzy

```python
aturan1  = ctrl.Rule(ram['tinggi'] & vram['tinggi'] & cpu['tinggi'], kelayakan['layak'])
aturan5  = ctrl.Rule(ram['sedang'] & vram['sedang'] & cpu['sedang'], kelayakan['cukup_layak'])
aturan12 = ctrl.Rule(ram['rendah'] & vram['rendah'], kelayakan['tidak_layak'])
```

Program mendefinisikan **18 aturan fuzzy** yang menghubungkan kombinasi kondisi input dengan output kelayakan. Aturan-aturan ini menggunakan operator `&` (AND) untuk menggabungkan beberapa kondisi. Semakin tinggi spesifikasi yang terpenuhi, semakin tinggi output kelayakan yang dihasilkan. Aturan juga mencakup variabel storage sebagai faktor tambahan — storage yang kecil dapat menurunkan kelayakan meskipun RAM dan GPU sudah memadai.

---

### 4. Control System dan Simulasi

```python
engine = ctrl.ControlSystem([aturan1, aturan2, ..., aturan18])
sistem = ctrl.ControlSystemSimulation(engine)
```

Semua aturan dikumpulkan ke dalam `ctrl.ControlSystem` yang menjadi mesin inferensi fuzzy. `ControlSystemSimulation` adalah objek yang digunakan untuk menjalankan simulasi dengan nilai input tertentu. Objek `sistem` ini dibuat sekali di awal program dan digunakan ulang setiap kali tombol hitung ditekan.

---

### 5. Fungsi Hitung — `hitung_kelayakan()`

```python
def hitung_kelayakan(ram_val, vram_val, cpu_val, storage_val):
    sistem.input['ram']     = np.clip(ram_val, 4, 32)
    sistem.input['vram']    = np.clip(vram_val, 2, 12)
    sistem.input['cpu']     = np.clip(cpu_val, 2.0, 5.0)
    sistem.input['storage'] = np.clip(storage_val, 50, 500)
    sistem.compute()
    skor = sistem.output['kelayakan']
    ...
```

Fungsi ini menerima nilai input mentah dari pengguna, lalu memasukkkannya ke dalam simulasi fuzzy. `np.clip` digunakan untuk memastikan nilai input tidak keluar dari universe of discourse yang sudah didefinisikan — misalnya jika pengguna memasukkan RAM 64 GB, nilai akan di-clip ke 32 GB. Setelah `sistem.compute()` dipanggil, hasil defuzzifikasi tersedia di `sistem.output['kelayakan']` sebagai angka tunggal antara 0–100.

---

### 6. Kelas GUI — `AplikasiFuzzy`

```python
class AplikasiFuzzy:
    def __init__(self, root):
        ...
    def hitung(self):
        ...
```

Kelas ini mengelola seluruh antarmuka grafis.

---

## Contoh Hasil Penilaian

| Skenario | RAM | VRAM | CPU | Storage | Skor | Label |
|----------|-----|------|-----|---------|------|-------|
| Spek tinggi | 32 GB | 10 GB | 5.0 GHz | 500 GB | 85.9 | Layak |
| Recommended RDR2 | 12 GB | 6 GB | 3.5 GHz | 200 GB | 56.3 | Cukup Layak |
| Minimum RDR2 | 8 GB | 2 GB | 3.0 GHz | 150 GB | 13.2 | Tidak Layak |
| Spek sangat lemah | 4 GB | 2 GB | 2.0 GHz | 60 GB | 11.7 | Tidak Layak |

---

## Cara Menjalankan

Install dependency terlebih dahulu:

```bash
pip install scikit-fuzzy numpy
```

Lalu jalankan program:

```bash
python sistem_fuzzy_game.py
```

Masukkan nilai spesifikasi PC/laptop kamu pada masing-masing field, lalu klik **Hitung Kelayakan**.

---

## Requirement

- Python 3.x
- numpy
- scikit-fuzzy
- Tkinter (sudah termasuk bawaan Python)
