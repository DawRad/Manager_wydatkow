import datetime as dtm
import pandas as pd
import numpy as np
from functools import reduce


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
    '''
    Parametr df -> parametr ty pandas.DataFrame
    '''
    def __init__(self, nazwa_tab: str, kolumny = ["Sklep", "Data", "Towar", "Cena"], df = pd.DataFrame({'A':[]}), wart_domyslne = ("Nieznany", dtm.date.today(), "pieczywo", 4.4)) -> None:
        super().__init__()
        self.__nazwa_ = nazwa_tab

        if not df.empty: self.__tabela_ = df
        else: self.__tabela_ = pd.DataFrame(columns=kolumny)      

    def podajNazwyKol(self):
        return self.__tabela_.columns.values
    
    def podajDF(self):
        return self.__tabela_
    
    def podajUnikatoweWartZKol(self, nazwa_kol: str):
        return self.__tabela_[nazwa_kol].unique().sort()
    
    def dolaczDF(self, new_df):
        self.__tabela_ = pd.concat([self.__tabela_, new_df], ignore_index=True)
    

"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Posiadacz*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Posiadacz(Obiekt):
    def __init__(self, imie: str, nazwisko: str) -> None:
        super().__init__()
        self.__tabWydatki_ = {}
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = {}
        self.__hash_ = (self.__imie_ + self.__nazwisko_).lower()

    def podajHash(self):
        return self.__hash_
    
    def podajImieINazw(self):
        return [self.__imie_, self.__nazwisko_]
    
    def podajNazwyTabWydatkow(self):
        return list(self.__tabWydatki_.keys())
    
    '''
    Od tej metody do następnej po niej:
    Wyżej powinien być zwrócony wyjątek, jeśli tabela o podanej nazwie
    nie istnieje
    '''
    def podajTabDF(self, nazwa_tab: str):
        tabela = self.__tabWydatki_.get(nazwa_tab, None)
        result = tabela.podajDF() if tabela is not None else pd.DataFrame({'A' : []})
        return result
    
    def podajTab(self, nazwa_tab: str):
        return self.__tabWydatki_.get(nazwa_tab, None)
    
    def podajUnikatoweNazwyKol(self, nazwy_tab: list()):
        res = []
        for nazwa in nazwy_tab: res.append(self.__tabWydatki_[nazwa].podajNazwyKol())
        if len(res) > 1: res = reduce(np.union1d, res).tolist()
        elif len(res) == 1: res = sorted(res[0].tolist())

        return res

    def podajUnikatoweWartZKol(self, nazwy_tab: list(), nazwa_kol: str):
        res = []
        for nazwa in nazwy_tab: res.append(self.__tabWydatki_[nazwa].podajUnikatoweWartZKol(nazwa_kol))
        if len(res) > 1: res = reduce(np.union1d, res).tolist()
        elif len(res) == 1: res = sorted(res[0].tolist())

        return res
    
    def dodajTab(self, tabela: TabWydatki):
        self.__tabWydatki_.append(tabela)

    def dodajTabDF(self, nazwa_tab: str, df: pd.DataFrame):
        # TODO: 
        #   sprawdzenie, czy element o podanym kluczu już nie istnieje

        new_tab = TabWydatki(nazwa_tab, df=df)
        self.__tabWydatki_[nazwa_tab] = new_tab

    '''
    Od tej metody we wszystkich dół:
    Wyżej powinien być zwrócony wyjątek, jeśli tabela o podanej nazwie
    nie istnieje
    '''
    def dodajWierszWTab(self, new_row: list, nazwa_tab = " "):
        tabela = self.__tabWydatki_.get(nazwa_tab, None)
        if tabela is not None: tabela.loc[len(tabela)] = new_row

    def dolaczDoTab(self, nazwa_tab, new_df):
        target = self.podajTab(nazwa_tab)
        if target == None: pass
        else: target.dolaczDF(new_df)

    def podajNazwyKolWTab(self, nazwa_tab: str):
        tabela = self.__tabWydatki_.get(nazwa_tab, None)
        return tabela.podajNazwyKol() if tabela is not None else []
