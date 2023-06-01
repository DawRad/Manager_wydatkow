import datetime as dtm
import pandas as pd


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Obiekt*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Obiekt:
    def __init__(self, idx: int) -> None:
        self.nrPorz_ = idx

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
| - - - - - ***Klasa Wydatek*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Wydatek(Obiekt):
    def __init__(self, idx: int, cena: float, nazwa = "inne", dzial = "inny") -> None:
        super().__init__(idx)
        self.__cena_ = cena
        self.__dzial_ = dzial
        self.__nazwa_ = nazwa

    def __str__(self) -> str:
        return super().__str__() + "\nDział: " + str(self.__dzial_) + "\nNazwa: " + self.__nazwa_ + "\nCena: " + str(self.__cena_)
    
    def podajCene(self) -> float:
        return self.__cena_


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Paragon*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Paragon(Obiekt):
    def __init__(self, idx: int, data: dtm.date, miejsce = "nieznane", pozycje = [Wydatek(1, 999.99)]) -> None:
        super().__init__(idx)
        self.__data_ = data
        self.__miejsce_ = miejsce
        self.__pozycje_ = pozycje

    def __str__(self) -> str:
        lista_pozycji = str("")
        for pozycja in self.__pozycje_: lista_pozycji += pozycja.__str__() + "\n- - - - -\n"
        lista_pozycji = lista_pozycji.removesuffix("\n- - - - -\n")

        return super().__str__() + "\nData: " + self.__data_.__str__() + "\nMiejsce: " + self.__miejsce_ + "\n\nLista wydatków:\n" + lista_pozycji
    
    def dodajPozycje(self, pozycja: Wydatek) -> None:
        self.__pozycje_.append(pozycja)

    def sumujWydatki(self) -> float:
        suma = 0.0
        for wydatek in self.__pozycje_: suma += wydatek.podajCene()
        return suma


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa TabWydatki*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""

class TabWydatki(Obiekt):
    def __init__(self, idx: int, nazwa: str, kolumny = ["Sklep", "Data", "Towar", "Cena"], wart_domyslne = ("Nieznany", dtm.date.today(), "pieczywo", 4.4)) -> None:
        super().__init__(idx)
        self.__nazwa_ = nazwa
        self.__tabela_ = pd.DataFrame(columns=kolumny)        

    def podajNazwyKol(self):
        return self.__tabela_.columns
    

"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Posiadacz*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Posiadacz(Obiekt):
    def __init__(self, idx: int, imie: str, nazwisko: str) -> None:
        super().__init__(idx)
        self.__tabWydatki_ = list(TabWydatki)
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = list(Zasob)

    def dodajTab(self, tabela: TabWydatki):
        self.__tabWydatki_.append(tabela)     