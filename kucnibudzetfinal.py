import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import os
import uuid
from datetime import datetime
from collections import defaultdict



class Transakcija:
    def __init__(self, datum, opis, iznos, valuta="EUR", id=None):
        
        try:
            d = datetime.strptime(datum, "%Y-%m-%d")
            self.datum_obj = d
            self.datum = d.strftime("%Y-%m-%d")
        except:
            raise ValueError("Datum mora biti u formatu YYYY-MM-DD")

        self.opis = opis
        self.iznos = iznos
        self.valuta = valuta

        
        self.id = id if id else str(uuid.uuid4())

    def to_xml(self, parent):
        raise NotImplementedError


class Prihod(Transakcija):
    def __init__(self, datum, opis, iznos, izvor, valuta="EUR", id=None):
        super().__init__(datum, opis, iznos, valuta, id)
        self.izvor = izvor

    def __str__(self):
        return f"[+] {self.datum} | {self.opis} | {self.iznos:.2f} {self.valuta} | Izvor: {self.izvor}"

    def to_xml(self, parent):
        el = ET.SubElement(parent, "Prihod")
        ET.SubElement(el, "ID").text = self.id
        ET.SubElement(el, "Datum").text = self.datum
        ET.SubElement(el, "Opis").text = self.opis
        ET.SubElement(el, "Iznos").text = str(self.iznos)
        ET.SubElement(el, "Valuta").text = self.valuta
        ET.SubElement(el, "Izvor").text = self.izvor


class Rashod(Transakcija):
    def __init__(self, datum, opis, iznos, kategorija, valuta="EUR", id=None):
        super().__init__(datum, opis, iznos, valuta, id)
        self.kategorija = kategorija

    def __str__(self):
        return f"[-] {self.datum} | {self.opis} | {self.iznos:.2f} {self.valuta} | Kategorija: {self.kategorija}"

    def to_xml(self, parent):
        el = ET.SubElement(parent, "Rashod")
        ET.SubElement(el, "ID").text = self.id
        ET.SubElement(el, "Datum").text = self.datum
        ET.SubElement(el, "Opis").text = self.opis
        ET.SubElement(el, "Iznos").text = str(self.iznos)
        ET.SubElement(el, "Valuta").text = self.valuta
        ET.SubElement(el, "Kategorija").text = self.kategorija




class FinTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 FinTrack – Kućni budžet 1.5")
        self.root.geometry("750x650")
        self.root.configure(bg="#f2f6f9")

        )
        self.default_kategorije = ["Hrana", "Režije", "Prijevoz", "Zabava"]
        self.default_izvori = ["Plaća", "Stipendija", "Poklon"]

        
        self.transakcije = []

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#007acc", foreground="white",
                        padding=6, font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#005f99")])

        
        logo_text = """
███████╗██╗███╗   ██╗████████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║  ██║
█████╗  ██║██╔██╗ ██║   ██║   ██████╔╝███████║██║     ███████║
██╔══╝  ██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║     ██╔══██║
██║     ██║██║ ╚████║   ██║   ██║  ██║██║  ██║╚██████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
        logo = tk.Label(root, text=logo_text, fg="#007acc",
                        bg="#f2f6f9", font=("Consolas", 8, "bold"))
        logo.pack(pady=(10, 0))

        naslov = tk.Label(root, text="Kućni budžet 1.5", font=("Segoe UI", 14, "bold"),
                          bg="#f2f6f9", fg="#00334d")
        naslov.pack()

        
        menubar = tk.Menu(root)
        app_menu = tk.Menu(menubar, tearoff=0)
        app_menu.add_command(label="O aplikaciji", command=self.o_aplikaciji)
        app_menu.add_separator()
        app_menu.add_command(label="Izlaz", command=self.autosave_and_quit)
        menubar.add_cascade(label="Aplikacija", menu=app_menu)

        opcije_menu = tk.Menu(menubar, tearoff=0)
        opcije_menu.add_command(label="Postavke", command=self.otvori_postavke)
        menubar.add_cascade(label="Opcije", menu=opcije_menu)

        root.config(menu=menubar)

 

        okvir = ttk.LabelFrame(root, text="Unos transakcije")
        okvir.pack(fill="x", padx=15, pady=10)

        ttk.Label(okvir, text="Datum (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Opis:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Iznos:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Valuta:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(okvir, text="Dodatno:").grid(row=4, column=0, padx=5, pady=2, sticky="e")

        self.datum = ttk.Entry(okvir)
        self.opis = ttk.Entry(okvir)
        self.iznos = ttk.Entry(okvir)
        self.valuta = ttk.Combobox(okvir, values=["EUR", "USD"], width=10)
        self.valuta.current(0)
        self.dodatno = ttk.Entry(okvir)

        self.datum.grid(row=0, column=1, pady=2)
        self.opis.grid(row=1, column=1, pady=2)
        self.iznos.grid(row=2, column=1, pady=2)
        self.valuta.grid(row=3, column=1, pady=2)
        self.dodatno.grid(row=4, column=1, pady=2)

        self.tip = tk.StringVar(value="prihod")
        ttk.Radiobutton(okvir, text="Prihod", variable=self.tip,
                        value="prihod").grid(row=0, column=2)
        ttk.Radiobutton(okvir, text="Rashod", variable=self.tip,
                        value="rashod").grid(row=1, column=2)

        ttk.Button(okvir, text="➕ Dodaj transakciju",
                   command=self.dodaj_transakciju).grid(row=5, column=0, columnspan=3, pady=8)

        

        ttk.Label(root, text="📋 Pregled transakcija:").pack()

        self.lista = tk.Listbox(root, height=10, width=85,
                                font=("Consolas", 9))
        self.lista.pack(padx=15, pady=5)

       
        filtar_frame = ttk.Frame(root)
        filtar_frame.pack(pady=5)

        ttk.Label(filtar_frame, text="Tip:").pack(side="left", padx=5)
        self.filtar = ttk.Combobox(filtar_frame, values=["Sve", "Prihodi", "Rashodi"], width=12)
        self.filtar.current(0)
        self.filtar.pack(side="left")

        
        ttk.Label(filtar_frame, text="Od:").pack(side="left")
        self.f_od = ttk.Entry(filtar_frame, width=12)
        self.f_od.pack(side="left")

        ttk.Label(filtar_frame, text="Do:").pack(side="left")
        self.f_do = ttk.Entry(filtar_frame, width=12)
        self.f_do.pack(side="left")

        
        ttk.Label(filtar_frame, text="Traži:").pack(side="left")
        self.search = ttk.Entry(filtar_frame, width=12)
        self.search.pack(side="left")

        ttk.Button(filtar_frame, text="🔍 Primijeni",
                   command=self.osvjezi_prikaz).pack(side="left", padx=5)

        
        ttk.Button(filtar_frame, text="📊 Mjesečni sažetak",
                   command=self.prikazi_mjesecni_sazetak).pack(side="left", padx=5)

        
        self.saldo_label = ttk.Label(root, text="Saldo: 0.00 €",
                                     font=("Segoe UI", 13, "bold"),
                                     foreground="#004d40")
        self.saldo_label.pack(pady=10)

        
        gumbo_frame = ttk.Frame(root)
        gumbo_frame.pack(pady=5)

        ttk.Button(gumbo_frame, text="💾 Spremi u XML",
                   command=self.spremi_xml).pack(side="left", padx=8)
        ttk.Button(gumbo_frame, text="📂 Učitaj XML",
                   command=self.ucitaj_xml).pack(side="left", padx=8)

        
        self.status = ttk.Label(root, text="Spreman",
                                relief="sunken", anchor="w", padding=3)
        self.status.pack(side="bottom", fill="x")

       
        self.root.protocol("WM_DELETE_WINDOW", self.autosave_and_quit)

    

    def dodaj_transakciju(self):
        try:
            datum = self.datum.get()
            opis = self.opis.get()
            iznos = float(self.iznos.get())
            dodatno = self.dodatno.get()
            valuta = self.valuta.get()

            if not datum or not opis:
                messagebox.showwarning("Upozorenje", "Molimo unesite datum i opis.")
                return

            if self.tip.get() == "prihod":
                t = Prihod(datum, opis, iznos, dodatno, valuta)
            else:
                t = Rashod(datum, opis, iznos, dodatno, valuta)

            self.transakcije.append(t)
            self.osvjezi_prikaz()
            self.ocisti_unos()
            self.status.config(text=f"Uspješno dodana transakcija: {opis}")

        except ValueError as e:
            messagebox.showerror("Greška", str(e))

    

    def osvjezi_prikaz(self):
        self.lista.delete(0, tk.END)
        tip = self.filtar.get()
        search = self.search.get().lower().strip()
        od = self.f_od.get().strip()
        do = self.f_do.get().strip()

        saldo = 0

        for t in self.transakcije:

            
            if od:
                try:
                    od_d = datetime.strptime(od, "%Y-%m-%d")
                    if t.datum_obj < od_d:
                        continue
                except:
                    pass

            if do:
                try:
                    do_d = datetime.strptime(do, "%Y-%m-%d")
                    if t.datum_obj > do_d:
                        continue
                except:
                    pass

            
            if tip == "Prihodi" and not isinstance(t, Prihod):
                continue
            if tip == "Rashodi" and not isinstance(t, Rashod):
                continue

            
            if search:
                full_text = f"{t.opis} {getattr(t, 'izvor', '')} {getattr(t, 'kategorija', '')}".lower()
                if search not in full_text:
                    continue

            
            if isinstance(t, Prihod):
                saldo += t.iznos
            else:
                saldo -= t.iznos

            self.lista.insert(tk.END, str(t))

        self.saldo_label.config(text=f"Saldo: {saldo:.2f} €")
        self.status.config(text="Filtriranje dovršeno.")

    def ocisti_unos(self):
        self.datum.delete(0, tk.END)
        self.opis.delete(0, tk.END)
        self.iznos.delete(0, tk.END)
        self.dodatno.delete(0, tk.END)

   

    def spremi_xml(self):
        dat = filedialog.asksaveasfilename(defaultextension=".xml",
                                           filetypes=[("XML datoteka", "*.xml")])
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
                idd = el.find("ID").text
                datum = el.find("Datum").text
                opis = el.find("Opis").text
                iznos = float(el.find("Iznos").text)
                valuta = el.find("Valuta").text

                if el.tag == "Prihod":
                    izvor = el.find("Izvor").text
                    self.transakcije.append(Prihod(datum, opis, iznos, izvor, valuta, idd))

                elif el.tag == "Rashod":
                    kat = el.find("Kategorija").text
                    self.transakcije.append(Rashod(datum, opis, iznos, kat, valuta, idd))

            self.osvjezi_prikaz()
            self.status.config(text=f"Učitano iz {dat}")

        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati datoteku: {e}")



    def prikazi_mjesecni_sazetak(self):
        if not self.transakcije:
            messagebox.showinfo("Info", "Nema transakcija.")
            return

        prozor = tk.Toplevel(self.root)
        prozor.title("Mjesečni sažetak")
        prozor.geometry("400x400")

        zbir = defaultdict(lambda: {"prihod": 0, "rashod": 0})

        for t in self.transakcije:
            key = t.datum[:7]  # YYYY-MM
            if isinstance(t, Prihod):
                zbir[key]["prihod"] += t.iznos
            else:
                zbir[key]["rashod"] += t.iznos

        txt = tk.Text(prozor)
        txt.pack(fill="both", expand=True)

        for mjesec, podaci in sorted(zbir.items()):
            saldo = podaci["prihod"] - podaci["rashod"]
            txt.insert("end",
                       f"{mjesec}\n"
                       f"  Prihod: {podaci['prihod']:.2f}\n"
                       f"  Rashod: {podaci['rashod']:.2f}\n"
                       f"  Neto saldo: {saldo:.2f}\n\n")

 

    def otvori_postavke(self):
        win = tk.Toplevel(self.root)
        win.title("Postavke")
        win.geometry("350x300")

        ttk.Label(win, text="Izvori prihoda:").pack(pady=5)
        izvori_box = tk.Text(win, height=5)
        izvori_box.insert("end", "\n".join(self.default_izvori))
        izvori_box.pack()

        ttk.Label(win, text="Kategorije rashoda:").pack(pady=5)
        kat_box = tk.Text(win, height=5)
        kat_box.insert("end", "\n".join(self.default_kategorije))
        kat_box.pack()

        def spremi():
            self.default_izvori = izvori_box.get("1.0", "end").strip().split("\n")
            self.default_kategorije = kat_box.get("1.0", "end").strip().split("\n")
            win.destroy()

        ttk.Button(win, text="Spremi", command=spremi).pack(pady=10)



    def autosave_and_quit(self):
        try:
            # automatsko spremanje u autosave.xml
            root = ET.Element("Transakcije")
            for t in self.transakcije:
                t.to_xml(root)
            ET.ElementTree(root).write("autosave.xml",
                                       encoding="utf-8",
                                       xml_declaration=True)
        except:
            pass

        self.root.destroy()


    def o_aplikaciji(self):
        messagebox.showinfo(
            "O aplikaciji",
            "💰 FinTrack – Kućni budžet\n"
            "Verzija: 1.5\n"
            "Autor: Vi\n\n"
            "Sadrži: jedinstvene ID-e, validaciju datuma, valute,\n"
            "napredno filtriranje, sažetke, postavke i autosave."
       




if __name__ == "__main__":
    root = tk.Tk()
    app = FinTrackApp(root)
    root.mainloop()



