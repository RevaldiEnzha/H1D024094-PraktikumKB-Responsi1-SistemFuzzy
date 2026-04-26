import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ── VARIABEL FUZZY ────────────────────────────────────────────────────────────

ram       = ctrl.Antecedent(np.arange(4, 33, 1),   'ram')
vram      = ctrl.Antecedent(np.arange(2, 13, 1),   'vram')
cpu       = ctrl.Antecedent(np.arange(2.0, 5.1, 0.1), 'cpu')
storage   = ctrl.Antecedent(np.arange(50, 501, 1), 'storage')
kelayakan = ctrl.Consequent(np.arange(0, 101, 1),  'kelayakan')

# ── MEMBERSHIP FUNCTION ───────────────────────────────────────────────────────

# RAM (GB): 4 - 32
ram['rendah'] = fuzz.trapmf(ram.universe, [4,  4,  6,  10])
ram['sedang'] = fuzz.trimf(ram.universe,  [8,  12, 16])
ram['tinggi'] = fuzz.trapmf(ram.universe, [14, 20, 32, 32])

# VRAM (GB): 2 - 12
vram['rendah'] = fuzz.trapmf(vram.universe, [2, 2, 3, 5])
vram['sedang'] = fuzz.trimf(vram.universe,  [4, 6, 8])
vram['tinggi'] = fuzz.trapmf(vram.universe, [6, 8, 12, 12])

# CPU Speed (GHz): 2.0 - 5.0
cpu['rendah'] = fuzz.trapmf(cpu.universe, [2.0, 2.0, 2.5, 3.2])
cpu['sedang'] = fuzz.trimf(cpu.universe,  [3.0, 3.5, 4.0])
cpu['tinggi'] = fuzz.trapmf(cpu.universe, [3.8, 4.2, 5.0, 5.0])

# Storage kosong (GB): 50 - 500
storage['kecil'] = fuzz.trapmf(storage.universe, [50,  50,  80,  120])
storage['cukup'] = fuzz.trimf(storage.universe,  [100, 175, 250])
storage['besar'] = fuzz.trapmf(storage.universe, [200, 300, 500, 500])

# Output kelayakan: 0 - 100
kelayakan['tidak_layak']  = fuzz.trapmf(kelayakan.universe, [0,  0,  15, 30])
kelayakan['kurang_layak'] = fuzz.trimf(kelayakan.universe,  [20, 35, 50])
kelayakan['cukup_layak']  = fuzz.trimf(kelayakan.universe,  [40, 57, 72])
kelayakan['layak']        = fuzz.trapmf(kelayakan.universe, [65, 80, 100, 100])

# ── ATURAN FUZZY ──────────────────────────────────────────────────────────────

aturan1  = ctrl.Rule(ram['tinggi'] & vram['tinggi'] & cpu['tinggi'],            kelayakan['layak'])
aturan2  = ctrl.Rule(ram['tinggi'] & vram['tinggi'] & cpu['sedang'],            kelayakan['layak'])
aturan3  = ctrl.Rule(ram['tinggi'] & vram['sedang'] & cpu['tinggi'],            kelayakan['layak'])
aturan4  = ctrl.Rule(ram['sedang'] & vram['tinggi'] & cpu['tinggi'],            kelayakan['layak'])
aturan5  = ctrl.Rule(ram['sedang'] & vram['sedang'] & cpu['sedang'],            kelayakan['cukup_layak'])
aturan6  = ctrl.Rule(ram['sedang'] & vram['sedang'] & cpu['tinggi'],            kelayakan['cukup_layak'])
aturan7  = ctrl.Rule(ram['tinggi'] & vram['sedang'] & cpu['sedang'],            kelayakan['cukup_layak'])
aturan8  = ctrl.Rule(ram['sedang'] & vram['tinggi'] & cpu['sedang'],            kelayakan['cukup_layak'])
aturan9  = ctrl.Rule(ram['sedang'] & vram['sedang'] & cpu['rendah'],            kelayakan['kurang_layak'])
aturan10 = ctrl.Rule(ram['rendah'] & vram['sedang'] & cpu['sedang'],            kelayakan['kurang_layak'])
aturan11 = ctrl.Rule(ram['sedang'] & vram['rendah'] & cpu['sedang'],            kelayakan['kurang_layak'])
aturan12 = ctrl.Rule(ram['rendah'] & vram['rendah'],                            kelayakan['tidak_layak'])
aturan13 = ctrl.Rule(ram['rendah'] & vram['sedang'] & cpu['rendah'],            kelayakan['tidak_layak'])
aturan14 = ctrl.Rule(ram['rendah'] & cpu['rendah'],                             kelayakan['tidak_layak'])
aturan15 = ctrl.Rule(storage['kecil'] & ram['rendah'],                          kelayakan['tidak_layak'])
aturan16 = ctrl.Rule(storage['besar'] & ram['tinggi'] & vram['tinggi'],         kelayakan['layak'])
aturan17 = ctrl.Rule(storage['cukup'] & ram['sedang'] & vram['sedang'],         kelayakan['cukup_layak'])
aturan18 = ctrl.Rule(storage['kecil'] & ram['sedang'] & vram['sedang'],         kelayakan['kurang_layak'])

engine = ctrl.ControlSystem([
    aturan1, aturan2, aturan3, aturan4, aturan5, aturan6,
    aturan7, aturan8, aturan9, aturan10, aturan11, aturan12,
    aturan13, aturan14, aturan15, aturan16, aturan17, aturan18
])
sistem = ctrl.ControlSystemSimulation(engine)

# ── FUNGSI HITUNG ─────────────────────────────────────────────────────────────

def hitung_kelayakan(ram_val, vram_val, cpu_val, storage_val):
    sistem.input['ram']     = np.clip(ram_val,     4,   32)
    sistem.input['vram']    = np.clip(vram_val,    2,   12)
    sistem.input['cpu']     = np.clip(cpu_val,     2.0, 5.0)
    sistem.input['storage'] = np.clip(storage_val, 50,  500)
    sistem.compute()
    skor = sistem.output['kelayakan']

    if skor >= 65:
        label = "Layak"
    elif skor >= 40:
        label = "Cukup Layak"
    elif skor >= 20:
        label = "Kurang Layak"
    else:
        label = "Tidak Layak"

    return round(skor, 1), label

# ── GUI ───────────────────────────────────────────────────────────────────────

class AplikasiFuzzy:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Fuzzy Kelayakan Spesifikasi PC untuk Game Berat")
        self.root.geometry("420x320")
        self.root.resizable(False, False)

        tk.Label(root, text="Sistem Fuzzy: Kelayakan Spesifikasi PC untuk Game Berat",
                 font=("Arial", 11, "bold"), wraplength=380, justify="center").pack(pady=12)

        frame = tk.Frame(root)
        frame.pack(padx=30, fill="x")

        tk.Label(frame, text="RAM (GB)  [4–32]:",        font=("Arial", 10), anchor="w").grid(row=0, column=0, sticky="w", pady=4)
        tk.Label(frame, text="VRAM GPU (GB)  [2–12]:",   font=("Arial", 10), anchor="w").grid(row=1, column=0, sticky="w", pady=4)
        tk.Label(frame, text="Kecepatan CPU (GHz)  [2.0–5.0]:", font=("Arial", 10), anchor="w").grid(row=2, column=0, sticky="w", pady=4)
        tk.Label(frame, text="Storage Kosong (GB)  [50–500]:", font=("Arial", 10), anchor="w").grid(row=3, column=0, sticky="w", pady=4)

        self.entry_ram     = tk.Entry(frame, font=("Arial", 10), width=10)
        self.entry_vram    = tk.Entry(frame, font=("Arial", 10), width=10)
        self.entry_cpu     = tk.Entry(frame, font=("Arial", 10), width=10)
        self.entry_storage = tk.Entry(frame, font=("Arial", 10), width=10)

        self.entry_ram.grid(row=0, column=1, padx=10)
        self.entry_vram.grid(row=1, column=1, padx=10)
        self.entry_cpu.grid(row=2, column=1, padx=10)
        self.entry_storage.grid(row=3, column=1, padx=10)

        tk.Button(root, text="Hitung Kelayakan", font=("Arial", 11),
                  command=self.hitung).pack(pady=12)

        self.label_hasil = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.label_hasil.pack()

        self.label_skor = tk.Label(root, text="", font=("Arial", 10), fg="gray")
        self.label_skor.pack()

    def hitung(self):
        try:
            ram_val     = float(self.entry_ram.get())
            vram_val    = float(self.entry_vram.get())
            cpu_val     = float(self.entry_cpu.get())
            storage_val = float(self.entry_storage.get())

            skor, label = hitung_kelayakan(ram_val, vram_val, cpu_val, storage_val)

            self.label_hasil.config(text=f"Hasil: {label}")
            self.label_skor.config(text=f"Skor kelayakan: {skor} / 100")

        except ValueError:
            messagebox.showerror("Input Tidak Valid", "Pastikan semua field diisi dengan angka.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    AplikasiFuzzy(root)
    root.mainloop()