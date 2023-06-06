import datetime as dtm
import pandas as pd


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Obiekt*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Obiekt:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Indeks: " + str(self.nrPorz_)


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Zasob*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Zasob(Obiekt):
    __liczObZas_ = dict()

    def __init__(self, rodzaj: str, kwota: float, waluta = "PLN") -> None:
        if self.__liczObZas_.get(rodzaj) != None: self.__liczObZas_[rodzaj] += 1
        else: self.__liczObZas_[rodzaj] = 1
        super().__init__(self.__liczObZas_[rodzaj])

        self.__rodzaj_ = rodzaj
        self.__kwota_ = kwota
        self.__waluta_ = waluta

    def __str__(self) -> str:
        return super().__str__() + "\nRodzaj zasobu: " + self.__rodzaj_ + "\n" + "Dostepne srodki: " + str(self.__kwota_)
    
    # W argumencie "kwota" znak musi uwzględniać czy pole klasy jest zmniejszane lub powiększane
    def aktualizujKwote(self, kwota):
        self.__kwota_ += kwota
    
    @classmethod
    def resetujLicznikZasobow(cls):
        Zasob.__liczObZas_ = dict()

    @classmethod
    def dodajRodzZasobow(cls, rodzaje: list[str]):
        for rodzaj in rodzaje:
            if Zasob.__liczObZas_.get(rodzaj) == None: Zasob.__liczObZas_[rodzaj] = 0

    @classmethod
    def wypiszRodzajeZasobow(cls):
        for [klucz, wart] in Zasob.__liczObZas_.items(): print("Rodzaj: ", klucz, "\nLiczba instancji: ", wart, "\n")


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa TabWydatki*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""

class TabWydatki(Obiekt):
    def __init__(self, nazwa: str, kolumny = ["Sklep", "Data", "Towar", "Cena"], wart_domyslne = ("Nieznany", dtm.date.today(), "pieczywo", 4.4)) -> None:
        super().__init__(idx)
        self.__nazwa_ = nazwa
        self.__tabela_ = pd.DataFrame(columns=kolumny)        

    def podajNazwyKol(self):
        return self.__tabela_.columns
    
    def podajNazwe(self):
        return self.__nazwa_
    

"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Posiadacz*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Posiadacz(Obiekt):
    def __init__(self, imie: str, nazwisko: str) -> None:
        super().__init__()
        self.__tabWydatki_ = list()
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = list()
        self.__hash_ = (self.__imie_ + self.__nazwisko_).lower()

    def podajHash(self):
        return self.__hash_
    
    def dodajTab(self, tabela: TabWydatki):
        self.__tabWydatki_.append(tabela)

    def dodajWierszWTab(self, new_row: list(), nazwa_tab = " "):
        for tabela in self.__tabWydatki_:
            if tabela.podajNazwe() == nazwa_tab:
                target = tabela
                break

        # target = pd.concat([target, new_row.to_frame().T], ignore_index=True)
        target.loc[len(target)] = new_row

    def podajNazwyKolWTab(self, nazwa: str):
        for tab in self.__tabWydatki_:
            if tab.podajNazwe() == nazwa: return tab.podajNazwyKol()

        return None
