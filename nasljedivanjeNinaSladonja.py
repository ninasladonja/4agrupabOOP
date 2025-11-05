class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        # Pohranjujemo osnovne podatke o zaposleniku
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self):
        # Ispis podataka o zaposleniku
        print(f"Ime i prezime: {self.ime} {self.prezime}, Plaća: {self.placa} EUR")




class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezici):
        # Poziv konstruktora roditeljske klase
        super().__init__(ime, prezime, placa)
        # Dodajemo novi atribut specifičan za programera
        self.programski_jezici = programski_jezici

    def prikazi_info(self):
        # Prvo ispiši osnovne podatke
        super().prikazi_info()
        # Zatim dodaj ispis programskih jezika
        jezici = ", ".join(self.programski_jezici)
        print(f"Programski jezici: {jezici}")




class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        # Poziv konstruktora roditeljske klase
        super().__init__(ime, prezime, placa)
        # Dodaj atribut tim (lista članova)
        self.tim = tim

    def prikazi_info(self):
        # Prvo ispiši osnovne podatke
        super().prikazi_info()
        # Zatim prikaži članove tima
        print("Tim:", ", ".join(self.tim))

    # Bonus zadatak: metoda za dodavanje člana tima
    def dodaj_clana_tima(self, novi_clan):
        self.tim.append(novi_clan)
        print(f"Član '{novi_clan}' dodan u tim.")




if __name__ == "__main__":
    # Kreiranje objekata
    z1 = Zaposlenik("Ana", "Anić", 1200)
    p1 = Programer("Petar", "Perić", 1800, ["Python", "JavaScript"])
    m1 = Menadzer("Iva", "Ivić", 2500, ["Ana Anić", "Petar Perić"])

    # Pozivanje metoda
    print("--- Podaci o zaposleniku ---")
    z1.prikazi_info()

    print("\n--- Podaci o programeru ---")
    p1.prikazi_info()

    print("\n--- Podaci o menadžeru ---")
    m1.prikazi_info()

    # Testiranje bonus metode
    print("\n--- Dodavanje člana tima ---")
    m1.dodaj_clana_tima("Marko Marić")
    m1.prikazi_info()
