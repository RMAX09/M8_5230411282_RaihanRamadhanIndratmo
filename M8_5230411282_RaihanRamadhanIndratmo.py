# Import semua fungsi, modul, dan kelas dari library tkinter (tidak mencakup submodul)
import tkinter as tk
# Merupakan submodul maka harus di import lagi (tidak include dengan *), agar tersedia secara eksplisit dalam kode
from tkinter import messagebox, ttk


class SistemSidapus:
    def __init__(self, root):
        self.root = root
        # Menamai program
        self.root.title("SiDaPus | Sistem Data Perpustakaan")
        self.root.geometry("700x600")   # Ukuran
        self.root.resizable(False, False)   # Tidak dapat dirubah (tetap)

        # Data Penyimpanan Buku
        self.book_data = []  # List untuk simpan data buku

        # Membuat User Interface
        self.create_ui()

    def create_ui(self):
        # Wrapper (frames yang akan saya gunakan 3 frame)
        # Komponen tabel ada di wrapper 1
        self.wrapper1 = tk.LabelFrame(self.root, text="Daftar Buku")
        # Komponen search ada di dalam wrapper 2 (include dengan 2 button)
        self.wrapper2 = tk.LabelFrame(self.root, text="Pencarian")
        # Komponen data buku ada di dalam wrapper 3 (include dengan 3 button)
        self.wrapper3 = tk.LabelFrame(self.root, text="Data Buku")

        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=20)
        self.wrapper2.pack(fill="both", padx=20, pady=20)
        self.wrapper3.pack(fill="both", padx=20, pady=20)

        # Membuat Variabel Penghubung
        self.setup_form_variables()

        # Buat label dan input
        self.create_form_fields()

        # Buat Tabel
        self.create_table()

        # Buat search
        self.create_search_components()

    def setup_form_variables(self):
        # variabel penghubung antara input dan data
        self.v_judul = tk.StringVar()
        self.v_kategori = tk.StringVar()
        self.v_no_rak = tk.StringVar()
        self.v_penulis = tk.StringVar()
        self.v_penerbit = tk.StringVar()
        self.v_tahun_terbit = tk.StringVar()
        self.v_stok = tk.IntVar()
        self.v_stok.set(0)
        self.q = tk.StringVar()

    def create_form_fields(self):
        # kolom 1
        fields = [
            ("Judul", self.v_judul, tk.Entry),
            ("Kategori", self.v_kategori, ttk.Combobox,
             {'values': ('000 - Umum', '100 - Filsafat dan Psikologi',
                         '200 - Agama', '300 - Ilmu - Ilmu Sosial',
                         '400 - Bahasa', '500 - Ilmu Pengetahuan Alam dan Matematika',
                         '600 - Teknologi dan Ilmu - Ilmu Terapan',
                         '700 - Seni, Hiburan, dan Olahraga',
                         '800 - Sastra', '900 - Geografi dan Sejarah')}),
            ("No Rak", self.v_no_rak, ttk.Combobox, {
             'values': ('001', '002', '003', '004', '005')}),
            ("Penulis", self.v_penulis, tk.Entry)
        ]

        # kolom 2
        second_column_fields = [
            ("Penerbit", self.v_penerbit, tk.Entry),
            ("Tahun Terbit", self.v_tahun_terbit, tk.Entry),
            ("Stok", self.v_stok, tk.Entry)
        ]

        
        for i, (label_text, var, field_type, *extra_args) in enumerate(fields):
            label = tk.Label(self.wrapper3, text=label_text)
            label.grid(row=i, column=0, sticky="w", pady=4)

            if extra_args:
                field = field_type(self.wrapper3, width=17,
                                   textvariable=var, **extra_args[0])
            else:
                field = field_type(self.wrapper3, textvariable=var)

            field.grid(row=i, column=1, columnspan=2,
                       sticky="w", pady=4, padx=10)

        
        for i, (label_text, var, field_type, *extra_args) in enumerate(second_column_fields):
            label = tk.Label(self.wrapper3, text=label_text)
            label.grid(row=i, column=3, sticky="w", pady=4, padx=10)

            if extra_args:
                field = field_type(
                    self.wrapper3, textvariable=var, **extra_args[0])
            else:
                field = field_type(self.wrapper3, textvariable=var)

            field.grid(row=i, column=4, columnspan=2, sticky="w", pady=4)

        
        frame_btn = tk.Frame(self.wrapper3)
        frame_btn.grid(row=4, column=0, columnspan=5, sticky="w", pady=10)

   
        add_btn = tk.Button(frame_btn, text="Tambah Baru",
                            command=self.add_new)
        delete_btn = tk.Button(frame_btn, text="Hapus",
                               command=self.delete_book)
        borrow_btn = tk.Button(
            frame_btn, text="Pinjam Buku", command=self.borrow_book)

        add_btn.pack(side=tk.LEFT, padx=5)
        delete_btn.pack(side=tk.LEFT, padx=5)
        borrow_btn.pack(side=tk.LEFT, padx=5)

    def create_table(self):
        # Tabel data buku
        self.trv = ttk.Treeview(self.wrapper1, column=(1, 2, 3, 4, 5, 6, 7),
                                show="headings", height=5)
        self.trv.bind("<<TreeviewSelect>>", self.on_table_select)

        # Headings Tabel
        headings = ["Judul", "Kategori", "No Rak Buku",
                    "Penulis", "Penerbit", "Tahun Terbit", "Stok"]
        for i, heading in enumerate(headings, 1):
            self.trv.heading(i, text=heading)

        
        column_configs = [
            (1, 95, 135, 'center'),
            (2, 95, 135, 'center'),
            (3, 95, 135, 'center'),
            (4, 95, 135, 'center'),
            (5, 95, 135, 'center'),
            (6, 95, 135, 'center'),
            (7, 65, 105, 'center')
        ]

        for col, width, minwidth, anchor in column_configs:
            self.trv.column(col, width=width, minwidth=minwidth,
                            anchor=anchor)

        # Scrollbars
        yscrollbar = tk.Scrollbar(
            self.wrapper1, orient="vertical", command=self.trv.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")

        xscrollbar = tk.Scrollbar(
            self.wrapper1, orient="horizontal", command=self.trv.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")

        self.trv.configure(yscrollcommand=yscrollbar.set,
                           xscrollcommand=xscrollbar.set)
        self.trv.pack(fill=tk.BOTH, expand=True)

    def create_search_components(self):
    
        lbl = tk.Label(self.wrapper2, text="Search")
        lbl.pack(side=tk.LEFT, padx=10, pady=15)

        ent = tk.Entry(self.wrapper2, textvariable=self.q)
        ent.pack(side=tk.LEFT, padx=6, pady=15)

        btn = tk.Button(self.wrapper2, text="Search", command=self.search)
        btn.pack(side=tk.LEFT, padx=6, pady=15)

        cbtn = tk.Button(self.wrapper2, text="Clear", command=self.clear)
        cbtn.pack(side=tk.LEFT, padx=6, pady=15)

    def add_new(self):
        # Validasi data harus diisi semua
        if not (self.v_judul.get() and self.v_kategori.get() and
                self.v_no_rak.get() and self.v_penulis.get() and
                self.v_penerbit.get() and self.v_tahun_terbit.get() and
                self.v_stok.get()):
            messagebox.showwarning("Peringatan", "Semua data harus diisi!")
            return

        # Validasi tahun hanya angka
        if not self.v_tahun_terbit.get().isdigit():
            messagebox.showerror("Error", "Tahun terbit harus berupa angka!")
            return

        # Validasi stok harus berupa angka
        try:
            stok = int(self.v_stok.get())
            if stok < 0:
                messagebox.showerror("Error", "Stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka!")
            return

        # Jika validasi lolos, data disimpan
        new_book = {
            "judul": self.v_judul.get(),
            "kategori": self.v_kategori.get(),
            "no_rak": self.v_no_rak.get(),
            "penulis": self.v_penulis.get(),
            "penerbit": self.v_penerbit.get(),
            "tahun_terbit": self.v_tahun_terbit.get(),
            "stok": stok
        }
        self.book_data.append(new_book)
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Sukses", "Buku berhasil ditambahkan.")

    def delete_book(self):
        selected_item = self.trv.selection()
        if not selected_item:
            messagebox.showwarning(
                "Peringatan", "Pilih buku yang ingin dihapus!")
            return
        item_index = self.trv.index(selected_item[0])
        del self.book_data[item_index]
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Sukses", "Buku berhasil dihapus.")

    def search(self):
        query = self.q.get().lower()
        filtered_books = [
            book for book in self.book_data if query in book["judul"].lower()
        ]
        self.refresh_table(filtered_books)

    def clear(self):
        self.q.set("")
        self.refresh_table()

    def borrow_book(self):
        selected_item = self.trv.selection()
        if not selected_item:
            messagebox.showwarning(
                "Peringatan", "Pilih buku yang ingin dipinjam!")
            return

        try:
            jumlah_pinjam = int(self.v_stok.get())
            if jumlah_pinjam <= 0:
                messagebox.showerror(
                    "Error", "Jumlah pinjam harus lebih dari nol!")
                return

            item_index = self.trv.index(selected_item[0])
            if self.book_data[item_index]["stok"] >= jumlah_pinjam:
                self.book_data[item_index]["stok"] -= jumlah_pinjam
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Sukses", "Buku berhasil dipinjam.")
            else:
                messagebox.showerror("Error", "Stok buku tidak mencukupi.")
        except ValueError:
            messagebox.showerror(
                "Error", "Masukkan jumlah pinjam sebagai angka!")

    def refresh_table(self, data=None):
        self.trv.delete(*self.trv.get_children())
        books_to_display = data if data is not None else self.book_data
        for index, book in enumerate(books_to_display):
            self.trv.insert("", "end", values=(
                book["judul"], book["kategori"], book["no_rak"],
                book["penulis"], book["penerbit"], book["tahun_terbit"], book["stok"]
            ))

    def on_table_select(self, event):
        selected_item = self.trv.selection()
        if not selected_item:
            return
        item_index = self.trv.index(selected_item[0])
        selected_book = self.book_data[item_index]
        # Mengisi form dengan data buku yang dipilih
        self.v_judul.set(selected_book["judul"])
        self.v_kategori.set(selected_book["kategori"])
        self.v_no_rak.set(selected_book["no_rak"])
        self.v_penulis.set(selected_book["penulis"])
        self.v_penerbit.set(selected_book["penerbit"])
        self.v_tahun_terbit.set(selected_book["tahun_terbit"])
        self.v_stok.set(selected_book["stok"])

    def clear_form(self):
        self.v_judul.set("")
        self.v_kategori.set("")
        self.v_no_rak.set("")
        self.v_penulis.set("")
        self.v_penerbit.set("")
        self.v_tahun_terbit.set("")
        self.v_stok.set(0)


def main():
    root = tk.Tk()
    app = SistemSidapus(root)
    root.mainloop()


if __name__ == "__main__":
    main()
