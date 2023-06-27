import datetime as dtm
import pandas as pd
import numpy as np
from functools import reduce
from Wyjatki import *


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
    def __init__(self, nazwa_tab: str, kolumny = ["Data", "Nazwa", "Kwota", "Wykonanie"], df = pd.DataFrame({'A':[]}), mnoznik = -1) -> None:
        super().__init__()
        self._nazwa_ = nazwa_tab
        self._mnoznik_ = mnoznik 

        if not df.empty: przekazane_kol = df.columns.values
        else: 
            przekazane_kol = kolumny
            df = pd.DataFrame(columns=kolumny)    
        
        if "Data" not in przekazane_kol or "Nazwa" not in przekazane_kol or "Kwota" not in przekazane_kol or "Wykonanie" not in przekazane_kol: 
            raise BadDFCols("DataFrame nie zawiera kolumn: \"Data\", \"Nazwa\", \"Kwota\" ani \"Wykonanie\"")
        else: 
            self._tabela_ = df
            self._tabela_['Data'] = pd.to_datetime(self._tabela_['Data'])
            self._tabela_['Wykonanie'] = self._tabela_['Wykonanie'].astype(bool)

    def podajNazwe(self):
        return self._nazwa_

    def podajNazwyKol(self):
        return self._tabela_.columns.values
    
    def podajDF(self):
        return self._tabela_
    
    def podajUnikatoweWartZKol(self, nazwa_kol: str) -> None | np.ndarray:
        """ Podaje tylko niepowtarzające się wartości z danej kolumny pola TabWydatki._tabela_

        Parametry
        ----------
        nazwa_kol : str
            Nazwa kolumny, w której są szukane unikalne wartości

        Zwraca
        ----------
        None, jeżeli w tabeli nie ma podanej kolumny. W przeciwnym wypadku: numpy.ndarray
        """

        res = None
        if nazwa_kol in self._tabela_.columns.values: 
            res = self._tabela_[nazwa_kol].unique()
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
            res = self._tabela_[kol_etykiet].value_counts() if len(wart_kolumn) == 0 else self._tabela_[self._tabela_[kol_etykiet].isin(wart_kolumn)][kol_etykiet].value_counts()
            res_keys, res_values = res.index.tolist(), res.values.tolist()
            res = dict[str, int]()
            for key, value in zip(res_keys, res_values): res[key] = value
        elif sumuj and kol_wart != '':
            # tu sumowane są wartości z kolumny wartości dla wszystkich lub wybranych etykiet z kolumny etykiet
            res = dict[str, float]()
            if len(wart_kolumn) == 0:
                # jeżeli nie ma wybranych wartości kolumny etykiet do uwzględnienia
                for idx, row in self._tabela_.iterrows(): res[row[kol_etykiet]] = (res[row[kol_etykiet]] + row[kol_wart]) if res.get(row[kol_etykiet], None) is not None else row[kol_wart]
            else:
                # gdy uwzględniamy tylko wybrane wartości kolumny etykiet
                for idx, row in self._tabela_.iterrows(): 
                    if row[kol_etykiet] in wart_kolumn: res[row[kol_etykiet]] = (res[row[kol_etykiet]] + row[kol_wart]) if res.get(row[kol_etykiet], None) is not None else row[kol_wart]

        return res
    
    def podajSumeDoUaktualKonta(self, data: dtm.datetime):
        """ Oblicza kwotę, o jaką powinno zostać zaktualizowane konto.

        Kwota może być ujemna, gdy uwzględniane są wydatki lub dodatnia, gdy chodzi o przychody.
        Dodatkowo, metoda uaktualnia stan każdej z pozycji tabeli - jeśli jakiś wiersz wg podanej daty ma zostać uwzględniony
        w bilansie, wtedy wartość kolumny 'Wykonanie' jest zmieniana na True.

        Parametry
        ----------
        data : datetime.datetime
            Dzień oraz godzina odniesienia - jeśli data rozpatrywanej pozycji jest dokładnie taka, jak podana, lub wcześniejsza, wtedy
            pozycja jest uwzględniana w rachunkach.
        """

        res = 0.0
        self._tabela_ = self._tabela_.sort_values(['Wykonanie', 'Data'], ascending=[True, False])
        for idx, row in self._tabela_.iterrows():
            if row['Data'] <= data and not row["Wykonanie"]: 
                res += row['Kwota'] * self._mnoznik_
                self._tabela_.at[idx, 'Wykonanie'] = True
            elif row["Wykonanie"]: break

        return res
    
    def dolaczDF(self, new_df):
        self._tabela_ = pd.concat([self._tabela_, new_df], ignore_index=True)

    def dodajWiersz(self, wiersz: pd.Series):
        pd.concat([self._tabela_, wiersz.T], ignore_index=True)           


"""
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - \
| - - - - - ***Klasa Posiadacz*** - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - /
"""
class Posiadacz(Obiekt):
    def __init__(self, imie: str, nazwisko: str, zasoby: float = 0.0) -> None:
        super().__init__()
        self.__tabWydatki_ = dict[str, TabWydatki]()
        self.__tabPrzychody_ = TabWydatki("Przychody", mnoznik=1)
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = zasoby
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

    def dodajWierszFinansow(self, nowy_wiersz: pd.Series, rodzaj_tab: str = 'Przychody', nazwa_tab_wydatki = ''):
        if rodzaj_tab == 'Przychody':
            self.__tabPrzychody_.dodajWiersz(nowy_wiersz)
        if rodzaj_tab == 'Wydatki':
            if self.__tabWydatki_.get(nazwa_tab_wydatki, None) is None: raise MissingKeyError("Tabela wydatków o podanym kluczu - \"" + nazwa_tab_wydatki + "\" - nie istnieje")
            self.__tabWydatki_[nazwa_tab_wydatki].dodajWiersz(nowy_wiersz)

    def uaktualnijKonto(self, data: dtm.datetime):
        """ Wykonuje metody wyznaczające kwotę do uaktualnienia konta dla każdej z tabel wydatków lub przychodów posiadacza.

        Parametry
        ----------
        data : datetime.datetime
            Dzień i godzina, według których obliczane jest uaktualnienie.

        Zwraca
        ----------
        Uaktualniony stan konta.
        """

        res = 0.0
        res += self.__tabPrzychody_.podajSumeDoUaktualKonta(data)
        for key in self.__tabWydatki_.keys(): res += self.__tabWydatki_[key].podajSumeDoUaktualKonta(data)

        self.__zasoby_ += res
        
        return self.__zasoby_

    def dolaczDoTab(self, nazwa_tab, new_df):
        target = self.podajTab(nazwa_tab)
        if target == None: pass
        else: target.dolaczDF(new_df)

    def podajNazwyKolWTab(self, nazwa_tab: str):
        tabela = self.__tabWydatki_.get(nazwa_tab, None)
        return tabela.podajNazwyKol() if tabela is not None else []
