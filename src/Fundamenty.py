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

    def podajNazwe(self):
        return self.__nazwa_

    def podajNazwyKol(self):
        return self.__tabela_.columns.values
    
    def podajDF(self):
        return self.__tabela_
    
    def podajUnikatoweWartZKol(self, nazwa_kol: str) -> None | np.ndarray:
        """ Podaje tylko niepowtarzające się wartości z danej kolumny pola TabWydatki.__tabela_

        Parametry
        ----------
        nazwa_kol : str
            Nazwa kolumny, w której są szukane unikalne wartości

        Zwraca
        ----------
        None, jeżeli w tabeli nie ma podanej kolumny. W przeciwnym wypadku: numpy.ndarray
        """

        res = None
        if nazwa_kol in self.__tabela_.columns.values: 
            res = self.__tabela_[nazwa_kol].unique()
            res.sort()

        return res
    
    def podajDaneTabeliDoWykresu(self, kol_etykiet: str, kol_wart = '', wart_kolumn = [], sumuj = False) -> dict():
        """ Zbiera dane z tabeli DataFrame.

        Domyślnie dane są używane w rysowaniu wykresów.

        Zwraca
        ----------
        Pusty słownik, jeśli nie znaleziono pasujących wartości.
        Słownik, w którym: unikalne wartości to klucze, odpowiadające im zliczenia lub sumy wartości to wartości słownika.
        """

        res = {}
        if not sumuj:
            # tu zliczane są tylko wystąpienia unikalnych wartości z kolumny etykiet
            res = self.__tabela_[kol_etykiet].value_counts() if len(wart_kolumn) == 0 else self.__tabela_[self.__tabela_[kol_etykiet].isin(wart_kolumn)][kol_etykiet].value_counts()
            res_keys, res_values = res.index.tolist(), res.values.tolist()
            res = dict[str, int]()
            for key, value in zip(res_keys, res_values): res[key] = value
        elif sumuj and kol_wart != '':
            # tu sumowane są wartości z kolumny wartości dla wszystkich lub wybranych etykiet z kolumny etykiet
            res = dict[str, float]()
            if len(wart_kolumn) == 0:
                # jeżeli nie ma wybranych wartości kolumny etykiet do uwzględnienia
                for idx, row in self.__tabela_.iterrows(): res[row[kol_etykiet]] = (res[row[kol_etykiet]] + row[kol_wart]) if res.get(row[kol_etykiet], None) is not None else row[kol_wart]
            else:
                # gdy uwzględniamy tylko wybrane wartości kolumny etykiet
                for idx, row in self.__tabela_.iterrows(): 
                    if row[kol_etykiet] in wart_kolumn: res[row[kol_etykiet]] = (res[row[kol_etykiet]] + row[kol_wart]) if res.get(row[kol_etykiet], None) is not None else row[kol_wart]

        return res
    
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
        self.__tabWydatki_ = dict[str, TabWydatki]()
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = dict[str, Zasob]()
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
        for nazwa in nazwy_tab:
            tmp = self.__tabWydatki_[nazwa].podajUnikatoweWartZKol(nazwa_kol)
            if tmp is not None: res.append(tmp)
        if len(res) > 1: res = reduce(np.union1d, res).tolist()
        elif len(res) == 1: res = sorted(res[0].tolist())

        return res
    
    def podajDaneTabelDoWykresu(self, nazwy_tab: list[str](), kol_etykiet: str, kol_wart = '', etykiety_kol = [], sumuj = False) -> dict():
        """ Wyszukuje wskazane dane w podanych tabelach.

        Domyślnie dane są pobierane dla tworzenia wykresów.

        Zwraca
        ----------
        Pusty słownik, jeśli nie znaleziono pasujących wartości.
        Słownik, w którym: unikalne wartości oraz odpowiadające im zliczenia lub sumy wartości (dla każdej z podanych tabel) to, odpowiednio, klucze i wartości słownika.
        """

        res = {}
        for nazwa in nazwy_tab: 
            tmp = self.__tabWydatki_[nazwa].podajDaneTabeliDoWykresu(kol_etykiet, kol_wart, etykiety_kol, sumuj)
            for key in tmp.keys(): res[key] = (res[key] + tmp[key]) if res.get(key, None) is not None else tmp[key] 

        return res
    
    def dodajTab(self, tabela: TabWydatki):
        #TODO:
        #   sprawdzenie, czy element o podanym kluczu już nie istnieje

        self.__tabWydatki_[tabela.podajNazwe()] = tabela

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
