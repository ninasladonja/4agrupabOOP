import tkinter as tk
from tkinter import messagebox
import csv
import os


class Ucenik:
    def __init__(self, ime, prezime, razred):
        # Inicijalizacija atributa
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        # Definira kako će se objekt prikazivati kao tekst
        return f"{self.prezime} {self.ime} ({self.razred})"


class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija učenika")
        self.root.geometry("550x420")

        # Lista učenika i indeks odabranog
        self.ucenici = []
        self.odabrani_ucenik_index = None

        # Konfiguracija prozora
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Okviri (Frame-ovi)
        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        # Widgeti za unos podataka
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        # Gumbi
        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10)

        self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="W")

        # Novi gumbi za BONUS fazu
        self.spremi_csv_gumb = tk.Button(unos_frame, text="Spremi CSV", command=self.spremi_u_csv)
        self.spremi_csv_gumb.grid(row=4, column=0, padx=5, pady=5)

        self.ucitaj_csv_gumb = tk.Button(unos_frame, text="Učitaj CSV", command=self.ucitaj_iz_csv)
        self.ucitaj_csv_gumb.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        # Widgeti za prikaz podataka
        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Povezivanje događaja
        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)

        # Automatski učitaj ako datoteka postoji
        if os.path.exists("ucenici.csv"):
            self.ucitaj_iz_csv()

    # Glavne funkcije aplikacije
    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if not ime or not prezime or not razred:
            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena!")
            return

        # Kreiraj novi objekt i dodaj u listu
        novi_ucenik = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi_ucenik)

        # Osvježi prikaz i očisti polja
        self.osvjezi_prikaz()
        self.ocisti_polja()

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))

    def odaberi_ucenika(self, event):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return

        self.odabrani_ucenik_index = odabrani_indeksi[0]
        odabrani_ucenik = self.ucenici[self.odabrani_ucenik_index]

        # Popuni polja
        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, odabrani_ucenik.ime)

        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, odabrani_ucenik.prezime)

        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, odabrani_ucenik.razred)

    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is None:
            messagebox.showinfo("Upozorenje", "Nije odabran nijedan učenik.")
            return

        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if not ime or not prezime or not razred:
            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena!")
            return

        # Ažuriraj podatke učenika
        ucenik = self.ucenici[self.odabrani_ucenik_index]
        ucenik.ime = ime
        ucenik.prezime = prezime
        ucenik.razred = razred

        # Osvježi prikaz i resetiraj stanje
        self.osvjezi_prikaz()
        self.ocisti_polja()
        self.odabrani_ucenik_index = None

    def ocisti_polja(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)

    # BONUS: Spremanje i učitavanje CSV
    def spremi_u_csv(self):
        if not self.ucenici:
            messagebox.showinfo("Info", "Nema učenika za spremanje.")
            return

        with open("ucenici.csv", mode="w", newline="", encoding="utf-8") as datoteka:
            polja = ["ime", "prezime", "razred"]
            writer = csv.DictWriter(datoteka, fieldnames=polja)
            writer.writeheader()
            for u in self.ucenici:
                writer.writerow({"ime": u.ime, "prezime": u.prezime, "razred": u.razred})
        messagebox.showinfo("Uspjeh", "Podaci su uspješno spremljeni u 'ucenici.csv'.")

    def ucitaj_iz_csv(self):
        if not os.path.exists("ucenici.csv"):
            messagebox.showinfo("Info", "Datoteka 'ucenici.csv' ne postoji.")
            return

        self.ucenici = []
        with open("ucenici.csv", mode="r", encoding="utf-8") as datoteka:
            reader = csv.DictReader(datoteka)
            for red in reader:
                u = Ucenik(red["ime"], red["prezime"], red["razred"])
                self.ucenici.append(u)

        self.osvjezi_prikaz()
        messagebox.showinfo("Uspjeh", "Podaci su uspješno učitani iz 'ucenici.csv'.")


# Pokretanje aplikacije
if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()