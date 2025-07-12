import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

FILE = "data.csv"

# --- Fungsi CSV ---
def read_data():
    if not os.path.exists(FILE):
        with open(FILE, mode="w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
    with open(FILE, mode="r") as f:
        return list(csv.DictReader(f))

def write_all_data(data_list):
    with open(FILE, mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
        for d in data_list:
            writer.writerow([
                d["id"], d["tanggal"], d["jenis"],
                d["kategori"], d["jumlah"], d["deskripsi"]
            ])

def append_data(transaksi):
    with open(FILE, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(transaksi)

# --- CRUD Functions ---
def tambah_transaksi():
    try:
        jumlah = int(entry_jumlah.get())
        data = read_data()
        id_baru = int(data[-1]["id"]) + 1 if data else 1
        tanggal = datetime.now().strftime("%Y-%m-%d")
        transaksi = [
            id_baru,
            tanggal,
            jenis_var.get(),
            entry_kategori.get(),
            jumlah,
            entry_deskripsi.get()
        ]
        append_data(transaksi)
        messagebox.showinfo("Berhasil", "Transaksi ditambahkan.")
        bersihkan_form()
        tampilkan_data()
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka!")

def bersihkan_form():
    entry_kategori.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
    entry_deskripsi.delete(0, tk.END)

def tampilkan_data():
    for i in tree.get_children():
        tree.delete(i)
    for row in read_data():
        tree.insert("", tk.END, values=[
            row["id"], row["tanggal"], row["jenis"],
            row["kategori"], row["jumlah"], row["deskripsi"]
        ])

def pilih_data(event):
    item = tree.selection()
    if item:
        values = tree.item(item)["values"]
        all_data = read_data()
        selected = next((d for d in all_data if d["id"] == str(values[0])), None)
        if selected:
            jenis_var.set(selected["jenis"])
            entry_kategori.delete(0, tk.END)
            entry_kategori.insert(0, selected["kategori"])
            entry_jumlah.delete(0, tk.END)
            entry_jumlah.insert(0, selected["jumlah"])
            entry_deskripsi.delete(0, tk.END)
            entry_deskripsi.insert(0, selected["deskripsi"])
            btn_edit["state"] = "normal"
            btn_hapus["state"] = "normal"

def edit_transaksi():
    item = tree.selection()
    if not item:
        return
    selected = tree.item(item)["values"]
    id_edit = selected[0]
    data = read_data()
    for d in data:
        if d["id"] == str(id_edit):
            d["jenis"] = jenis_var.get()
            d["kategori"] = entry_kategori.get()
            d["jumlah"] = entry_jumlah.get()
            d["deskripsi"] = entry_deskripsi.get()
            break
    write_all_data(data)
    messagebox.showinfo("Berhasil", "Data berhasil diubah.")
    bersihkan_form()
    tampilkan_data()
    btn_edit["state"] = "disabled"
    btn_hapus["state"] = "disabled"

def hapus_transaksi():
    item = tree.selection()
    if not item:
        return
    selected = tree.item(item)["values"]
    id_hapus = selected[0]
    data = read_data()
    data = [d for d in data if d["id"] != str(id_hapus)]
    write_all_data(data)
    messagebox.showinfo("Berhasil", "Data berhasil dihapus.")
    tampilkan_data()
    bersihkan_form()
    btn_edit["state"] = "disabled"
    btn_hapus["state"] = "disabled"

# --- Laporan ---
def tampilkan_laporan():
    for i in tree_laporan.get_children():
        tree_laporan.delete(i)

    data = read_data()
    total_masuk = sum(int(d["jumlah"]) for d in data if d["jenis"] == "pemasukan")
    total_keluar = sum(int(d["jumlah"]) for d in data if d["jenis"] == "pengeluaran")
    saldo = total_masuk - total_keluar

    tree_laporan.insert("", "end", values=("Total Pemasukan", f"Rp {total_masuk:,}"))
    tree_laporan.insert("", "end", values=("Total Pengeluaran", f"Rp {total_keluar:,}"))
    tree_laporan.insert("", "end", values=("Saldo Saat Ini", f"Rp {saldo:,}"))

# === GUI ===
root = tk.Tk()
root.title("Aplikasi Manajemen Keuangan")
root.geometry("1000x600")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#007acc", foreground="white")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# === TAB TRANSAKSI ===
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Kelola Transaksi")

judul = tk.Label(tab1, text="Manajemen Keuangan", font=("Segoe UI", 16, "bold"))
judul.pack(pady=10)

frame_form = ttk.LabelFrame(tab1, text="Tambah / Edit Transaksi", padding=15)
frame_form.pack(padx=15, pady=10, fill="x")

jenis_var = tk.StringVar(value="pemasukan")
ttk.Label(frame_form, text="Jenis").grid(row=0, column=0, sticky="w", padx=5, pady=5)
ttk.Combobox(frame_form, textvariable=jenis_var, values=["pemasukan", "pengeluaran"], state="readonly", width=25).grid(row=0, column=1, padx=5)

ttk.Label(frame_form, text="Kategori").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_kategori = ttk.Entry(frame_form, width=27)
entry_kategori.grid(row=1, column=1, padx=5)

ttk.Label(frame_form, text="Jumlah (Rp)").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_jumlah = ttk.Entry(frame_form, width=27)
entry_jumlah.grid(row=2, column=1, padx=5)

ttk.Label(frame_form, text="Deskripsi").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_deskripsi = ttk.Entry(frame_form, width=27)
entry_deskripsi.grid(row=3, column=1, padx=5)

ttk.Button(frame_form, text="Tambah Transaksi", command=tambah_transaksi).grid(row=4, column=0, padx=5, pady=10)
btn_edit = ttk.Button(frame_form, text="Edit Transaksi", command=edit_transaksi, state="disabled")
btn_edit.grid(row=4, column=1, padx=5, pady=10)
btn_hapus = ttk.Button(frame_form, text="Hapus Transaksi", command=hapus_transaksi, state="disabled")
btn_hapus.grid(row=5, column=0, columnspan=2, pady=5)

# === TABEL ===
frame_tabel = ttk.Frame(tab1)
frame_tabel.pack(fill="both", expand=True, padx=15)

scroll_y = ttk.Scrollbar(frame_tabel, orient="vertical")
tree = ttk.Treeview(frame_tabel, yscrollcommand=scroll_y.set,
    columns=("id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"),
    show="headings", height=10)
scroll_y.config(command=tree.yview)
scroll_y.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

for col in ("id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"):
    tree.heading(col, text=col.title())
    tree.column(col, anchor="center", width=140)

tree.bind("<<TreeviewSelect>>", pilih_data)

# === TAB LAPORAN ===
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Laporan Keuangan")

label_laporan = tk.Label(tab2, text="Laporan Ringkasan Keuangan", font=("Segoe UI", 16, "bold"))
label_laporan.pack(pady=10)

tree_laporan = ttk.Treeview(tab2, columns=("Keterangan", "Nilai"), show="headings", height=5)
tree_laporan.heading("Keterangan", text="Keterangan")
tree_laporan.heading("Nilai", text="Nilai")
tree_laporan.column("Keterangan", anchor="center", width=200)
tree_laporan.column("Nilai", anchor="center", width=200)
tree_laporan.pack(pady=20)

ttk.Button(tab2, text="Tampilkan Laporan", command=tampilkan_laporan).pack()

# Jalankan awal
tampilkan_data()
root.mainloop()
