import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import os


class Transakcija:
    def __init__(self, datum, opis, iznos):
        self.datum = datum
        self.opis = opis
        self.iznos = iznos

    def to_xml(self, parent):
        raise NotImplementedError


class Prihod(Transakcija):
    def __init__(self, datum, opis, iznos, izvor):
        super().__init__(datum, opis, iznos)
        self.izvor = izvor

    def __str__(self):
        return f"[+] {self.datum} | {self.opis} | {self.iznos:.2f} € | Izvor: {self.izvor}"

    def to_xml(self, parent):
        el = ET.SubElement(parent, "Prihod")
        ET.SubElement(el, "Datum").text = self.datum
        ET.SubElement(el, "Opis").text = self.opis
        ET.SubElement(el, "Iznos").text = str(self.iznos)
        ET.SubElement(el, "Izvor").text = self.izvor


class Rashod(Transakcija):
    def __init__(self, datum, opis, iznos, kategorija):
        super().__init__(datum, opis, iznos)
        self.kategorija = kategorija

    def __str__(self):
        return f"[-] {self.datum} | {self.opis} | {self.iznos:.2f} € | Kategorija: {self.kategorija}"

    def to_xml(self, parent):
        el = ET.SubElement(parent, "Rashod")
        ET.SubElement(el, "Datum").text = self.datum
        ET.SubElement(el, "Opis").text = self.opis
        ET.SubElement(el, "Iznos").text = str(self.iznos)
        ET.SubElement(el, "Kategorija").text = self.kategorija



class FinTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 FinTrack – Kućni budžet 1.0")
        self.root.geometry("750x600")
        self.root.configure(bg="#f2f6f9")

        self.transakcije = []

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#007acc", foreground="white", padding=6, font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#005f99")])
        style.configure("TLabel", background="#f2f6f9", font=("Segoe UI", 10))
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

        
        logo_text = """
███████╗██╗███╗   ██╗████████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║  ██║
█████╗  ██║██╔██╗ ██║   ██║   ██████╔╝███████║██║     ███████║
██╔══╝  ██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║     ██╔══██║
██║     ██║██║ ╚████║   ██║   ██║  ██║██║  ██║╚██████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
        logo = tk.Label(root, text=logo_text, fg="#007acc", bg="#f2f6f9", font=("Consolas", 8, "bold"))
        logo.pack(pady=(10, 0))

        naslov = tk.Label(root, text="Kućni budžet 1.0", font=("Segoe UI", 14, "bold"), bg="#f2f6f9", fg="#00334d")
        naslov.pack()

       
        menubar = tk.Menu(root)
        app_menu = tk.Menu(menubar, tearoff=0)
        app_menu.add_command(label="O aplikaciji", command=self.o_aplikaciji)
        app_menu.add_separator()
        app_menu.add_command(label="Izlaz", command=root.quit)
        menubar.add_cascade(label="Aplikacija", menu=app_menu)
        root.config(menu=menubar)

        
        okvir = ttk.LabelFrame(root, text="Unos transakcije")
        okvir.pack(fill="x", padx=15, pady=10)

        ttk.Label(okvir, text="Datum:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Opis:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Iznos (€):").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Dodatno:").grid(row=3, column=0, padx=5, pady=2, sticky="e")

        self.datum = ttk.Entry(okvir)
        self.opis = ttk.Entry(okvir)
        self.iznos = ttk.Entry(okvir)
        self.dodatno = ttk.Entry(okvir)
        self.datum.grid(row=0, column=1, pady=2)
        self.opis.grid(row=1, column=1, pady=2)
        self.iznos.grid(row=2, column=1, pady=2)
        self.dodatno.grid(row=3, column=1, pady=2)

        self.tip = tk.StringVar(value="prihod")
        ttk.Radiobutton(okvir, text="Prihod", variable=self.tip, value="prihod").grid(row=0, column=2, padx=5)
        ttk.Radiobutton(okvir, text="Rashod", variable=self.tip, value="rashod").grid(row=1, column=2, padx=5)

        ttk.Button(okvir, text="➕ Dodaj transakciju", command=self.dodaj_transakciju).grid(
            row=4, column=0, columnspan=3, pady=8
        )

        
        ttk.Label(root, text="📋 Pregled transakcija:").pack(pady=(5, 0))
        self.lista = tk.Listbox(root, height=10, width=85, font=("Consolas", 9))
        self.lista.pack(padx=15, pady=5)

        
        filtar_frame = ttk.Frame(root)
        filtar_frame.pack(pady=5)
        ttk.Label(filtar_frame, text="Filtriraj po tipu:").pack(side="left", padx=5)
        self.filtar = ttk.Combobox(filtar_frame, values=["Sve", "Prihodi", "Rashodi"], width=15)
        self.filtar.current(0)
        self.filtar.pack(side="left")
        ttk.Button(filtar_frame, text="🔍 Primijeni", command=self.osvjezi_prikaz).pack(side="left", padx=5)

        
        self.saldo_label = ttk.Label(root, text="Saldo: 0.00 €", font=("Segoe UI", 13, "bold"), foreground="#004d40")
        self.saldo_label.pack(pady=10)

        
        gumbo_frame = ttk.Frame(root)
        gumbo_frame.pack(pady=5)
        ttk.Button(gumbo_frame, text="💾 Spremi u XML", command=self.spremi_xml).pack(side="left", padx=8)
        ttk.Button(gumbo_frame, text="📂 Učitaj XML", command=self.ucitaj_xml).pack(side="left", padx=8)

        
        self.status = ttk.Label(root, text="Spreman", relief="sunken", anchor="w", padding=3)
        self.status.pack(side="bottom", fill="x")

   
    def dodaj_transakciju(self):
        try:
            datum = self.datum.get()
            opis = self.opis.get()
            iznos = float(self.iznos.get())
            dodatno = self.dodatno.get()

            if not datum or not opis:
                messagebox.showwarning("Upozorenje", "Molimo unesite datum i opis.")
                return

            if self.tip.get() == "prihod":
                t = Prihod(datum, opis, iznos, dodatno)
            else:
                t = Rashod(datum, opis, iznos, dodatno)

            self.transakcije.append(t)
            self.osvjezi_prikaz()
            self.ocisti_unos()
            self.status.config(text="Transakcija dodana.")
        except ValueError:
            messagebox.showerror("Greška", "Iznos mora biti broj!")

    def osvjezi_prikaz(self):
        self.lista.delete(0, tk.END)
        tip = self.filtar.get()
        saldo = 0

        for t in self.transakcije:
            if isinstance(t, Prihod):
                saldo += t.iznos
            else:
                saldo -= t.iznos

            if tip == "Sve" or (tip == "Prihodi" and isinstance(t, Prihod)) or (tip == "Rashodi" and isinstance(t, Rashod)):
                self.lista.insert(tk.END, str(t))

        self.saldo_label.config(text=f"Saldo: {saldo:.2f} €")

    def ocisti_unos(self):
        self.datum.delete(0, tk.END)
        self.opis.delete(0, tk.END)
        self.iznos.delete(0, tk.END)
        self.dodatno.delete(0, tk.END)

    def spremi_xml(self):
        dat = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML datoteka", "*.xml")])
        if not dat:
            return
        root = ET.Element("Transakcije")
        for t in self.transakcije:
            t.to_xml(root)
        ET.ElementTree(root).write(dat, encoding="utf-8", xml_declaration=True)
        self.status.config(text=f"Podaci spremljeni u {dat}")

    def ucitaj_xml(self):
        dat = filedialog.askopenfilename(filetypes=[("XML datoteka", "*.xml")])
        if not dat or not os.path.exists(dat):
            return
        try:
            tree = ET.parse(dat)
            root = tree.getroot()
            self.transakcije.clear()
            for el in root:
                if el.tag == "Prihod":
                    self.transakcije.append(Prihod(
                        el.find("Datum").text,
                        el.find("Opis").text,
                        float(el.find("Iznos").text),
                        el.find("Izvor").text
                    ))
                elif el.tag == "Rashod":
                    self.transakcije.append(Rashod(
                        el.find("Datum").text,
                        el.find("Opis").text,
                        float(el.find("Iznos").text),
                        el.find("Kategorija").text
                    ))
            self.osvjezi_prikaz()
            self.status.config(text=f"Učitano iz {dat}")
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati datoteku: {e}")

    def o_aplikaciji(self):
        messagebox.showinfo(
            "O aplikaciji",
            "💰 FinTrack – Kućni budžet\n"
            "Verzija: 1.0\n"
            "Autor: Vaše ime\n"
            "Godina: 2025\n\n"
            "Aplikacija za praćenje osobnih financija.\n"
            "Omogućuje unos prihoda i rashoda, filtriranje,\n"
            "izračun salda i spremanje podataka u XML formatu."
        )



if __name__ == "__main__":
    root = tk.Tk()
    app = FinTrackApp(root)
    root.mainloop()
