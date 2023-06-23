from Fundamenty import *
from Wyjatki import *

class Interfejs:
    def __init__(self) -> None:
        self.__posiadacze_ = dict[str, Posiadacz]()
        self.__actKey_ = "" # klucz, który wskazuje obiekt typu Posiadacz, na którym aktualnie dokonuje się wszystkich akcji
    
    def utworzPosiadacza(self, imie = "Jan", nazwisko = "Kowalski"):
        key = imie + " " + nazwisko

        if self.__posiadacze_.get(key, None) is not None: raise RepKeyError("Podana wartość klucza już istnieje w słowniku")

        self.__posiadacze_[key] = Posiadacz(imie, nazwisko)
        if self.__actKey_ == "": self.__actKey_ = key

    def dodajTabWydatki(self, nazwa: str, kolumny: list):
        posiadacz = self.__posiadacze_[self.__actKey_]
        nowa_tab = TabWydatki(nazwa, kolumny)
        posiadacz.dodajTab(nowa_tab)                

    # def dodajTabWydatki(self, nazwa: str, kolumny = []):
    #     if kolumny == []: nowa_tab = TabWydatki(nazwa)
    #     else: nowa_tab = TabWydatki(nazwa, kolumny)
    #     target = self.__posiadacze_[self.__actKey_]
    #     target.dodajTab(tabela=nowa_tab)

    '''
    Parametr polacz - łączy z istniejąca tabelą, jeśli 'True', w przeciwnym razie dodaje nową tabelę
    '''
    def wczytajTabZPliku(self, file_path = "", nazwa_tab = "", data_sep = ';', dec_sep = ',', polacz=False):
        if file_path[-4:len(file_path)] == ".csv":             
            read_func = lambda path: pd.read_csv(filepath_or_buffer=path, sep=data_sep, decimal=dec_sep)
        elif file_path[-5:len(file_path)] == ".xlsx": read_func = pd.read_excel
        else: raise BadFileFormatError("Format pliku z tabelą musi mieć rozszerzenie .csv lub .xlsx")

        new_df = read_func(file_path)
        if polacz:
            self.__posiadacze_[self.__actKey_].dolaczDoTab(nazwa_tab, new_df)
        else:
            self.__posiadacze_[self.__actKey_].dodajTabDF(nazwa_tab, new_df)

    def dodajWierszTabWydatki(self, nazwa_tab: str, nowy_wiersz = []):
        self.__posiadacze_[self.__actKey_].dodajWierszWTab(nowy_wiersz, nazwa_tab)

    def przejdzNaPoz(self, key):
        if self.__actKey_ == "": raise OutOfBondsError("Pusta lista Posiadaczy")
        else: self.__actKey_ = key

    def drukujTabWydatki(self, nazwa):
        print(self.__posiadacze_[self.__actKey_].podajTabDF(nazwa))

    def podajListePosiadaczy(self):
        out_list = []
        for key in self.__posiadacze_.keys():
            dane = self.__posiadacze_[key].podajImieINazw()
            out_list.append(dane[0] + " " + dane[1])

        return out_list
    
    def podajListeNazwTabWydatkow(self):
        return self.__posiadacze_[self.__actKey_].podajNazwyTabWydatkow()
    
    def podajNazwyKolTabWydatkow(self, nazwa_tab: str):
        return self.__posiadacze_[self.__actKey_].podajNazwyKolWTab(nazwa_tab)
        
    def podajDanePosiadacza(self):
        '''W tym przypadku chodzi o posiadacza na aktualnie ustawionej pozycji na liście        
        '''

        return self.__posiadacze_[self.__actKey_].podajImieINazw()
    
    def podajTabWydatki(self, nazwa_tab: str) -> pd.DataFrame:
        result = self.__posiadacze_[self.__actKey_].podajTabDF(nazwa_tab)
        if result.empty: raise KeyError("Nie znaleziono tabeli o podanym kluczu")
        
        return result
    
    def podajUnikatoweNazwyKol(self, nazwy_tab: list()):
        """ Podaje unikatowe nazwy ze wszystkich podanych kolumn.

        Zwraca
        ----------
        list(str) : Listę z unikalnymi nazwami kolumn ze wszystkich podanych tabel.
        """

        return self.__posiadacze_[self.__actKey_].podajUnikatoweNazwyKol(nazwy_tab)
    
    def podajUnikatoweWartZKol(self, nazwy_tab: list(), nazwa_kol: str):
        """ Zwraca listę unikatowych wartości z danej kolumny tabeli. 

        Bierze pod uwagę kolumnę z tabel, o podanych nazwach.

        Parametry
        ----------
        nazwy_tab : str
            Nazwa tabeli ze słownika obiektów typu TabWydatki klasy Posiadacz

        nazwa_kol : str
            Nazwa analizowanej kolumny tabeli

        Zwraca
        ----------
        list() : Listę unikatowych wartości
        """

        return self.__posiadacze_[self.__actKey_].podajUnikatoweWartZKol(nazwy_tab, nazwa_kol)
    
    def podajDaneDoWykresu(self, tabs: list(), kolumna_etykiet: str, kolumna_wart: str, etykiety_kolumn = [], zliczaj = False):
        """ Podaje odpowiednie dane do wyrysowania wykresu.

        W zależności od tego, jakie parametry podano, dane mogą uwzględniać zliczone 
        wystąpienia albo zsumowane wartości dla komórek z wybranych kolumn.

        Parameters
        ----------
        tabs : list(str)
            Lista nazw tabel, które mają zostać uwzględnione

        kolumna_etykiet : str
            Analizowana kolumna, która zawiera etykiety danych

        kolumna_wart : str
            Kolumna, która zawiera wartości do sumowania

        etykiety_kolumn : list(str)
            Przekazuje, jakie pozycje z analizowanej kolumny są brane pod uwagę

        zliczaj : bool
            Jeżeli True - zlicza wystąpienia każdej unikatowej (lub każdej z wybranych w parametrze wart_kolumn) wartości z kolumn podanych w parametrze kolumny_celu.
            Jeżeli False - analogicznie, jak w przeciwnym wypadku, ale nie zlicza, tylko sumuje te wartości.
            Domyślnie = False.        
        """

        pass