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
    '''
    Parametr df -> parametr ty pandas.DataFrame
    '''
    def __init__(self, nazwa: str, kolumny = ["Sklep", "Data", "Towar", "Cena"], df: pd.DataFrame = None, wart_domyslne = ("Nieznany", dtm.date.today(), "pieczywo", 4.4)) -> None:
        super().__init__()
        self.__nazwa_ = nazwa

        if df != None: self.__tabela_ = df
        else: self.__tabela_ = pd.DataFrame(columns=kolumny)      

    def podajNazwyKol(self):
        return self.__tabela_.columns
    
    def podajNazwe(self):
        return self.__nazwa_
    
    def podajDF(self):
        return self.__tabela_
    
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
        self.__tabWydatki_ = []
        self.__imie_ = imie
        self.__nazwisko_ = nazwisko
        self.__zasoby_ = []
        self.__hash_ = (self.__imie_ + self.__nazwisko_).lower()

    def podajHash(self):
        return self.__hash_
    
    def podajTabDF(self, nazwa_tab: str):
        for tabela in self.__tabWydatki_:
            if tabela.podajNazwe() == nazwa_tab: return tabela.podajDF()

        return pd.DataFrame({'A' : []})
    
    def podajTab(self, nazwa_tab: str):
        for tabela in self.__tabWydatki_:
            if tabela.podajNazwe() == nazwa_tab: return tabela

        return None
    
    def dodajTab(self, tabela: TabWydatki):
        self.__tabWydatki_.append(tabela)

    def dodajTabDF(self, nazwa_tab: str, df: pd.DataFrame):
        new_tab = TabWydatki(nazwa_tab, df=df)
        self.__tabWydatki_.append(new_tab)

    def dodajWierszWTab(self, new_row: list, nazwa_tab = " "):
        for tabela in self.__tabWydatki_:
            if tabela.podajNazwe() == nazwa_tab:
                targetTab = tabela.podajDF()
                break

        # target = pd.concat([target, new_row.to_frame().T], ignore_index=True)
        targetTab.loc[len(targetTab)] = new_row

    def dolaczDoTab(self, nazwa_tab, new_df):
        target = self.podajTab(nazwa_tab)
        if target == None: pass
        else: target.dolaczDF(new_df)

    def podajNazwyKolWTab(self, nazwa: str):
        for tab in self.__tabWydatki_:
            if tab.podajNazwe() == nazwa: return tab.podajNazwyKol()

        return None
