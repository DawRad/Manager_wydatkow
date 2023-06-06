from Fundamenty import *
from Wyjatki import OutOfBondsError
from Wyjatki import BadFileFormatError

class Interfejs:
    def __init__(self) -> None:
        self.__posiadacze_ = []
        self.__posiadaczPos_ = -2   # aktualna pozycja na liście posiadaczy (-2 ---> lista pusta)
    
    def utworzPosiadacza(self, imie = "Jan", nazwisko = "Kowalski"):
        self.__posiadacze_.append(Posiadacz(imie, nazwisko))
        if self.__posiadaczPos_ == -2: self.__posiadaczPos_ = 0

    def dodajTabWydatki(self, posiadacz_hash, nazwa: str, kolumny: list):
        '''
        W tej metodzie trzeba się upewnić czy używając tego sposobu iteracji
        na pewno zmieniane są oryginalne obiekty
        '''
        for posiadacz in self.__posiadacze_:
            if posiadacz.podajHash() == posiadacz_hash:
                nowa_tab = TabWydatki(nazwa, kolumny)
                posiadacz.dodajTab(nowa_tab)

    def dodajTabWydatki(self, nazwa: str, kolumny = []):
        if kolumny == []: nowa_tab = TabWydatki(nazwa)
        else: nowa_tab = TabWydatki(nazwa, kolumny)
        target = self.__posiadacze_[self.__posiadaczPos_]
        target.dodajTab(tabela=nowa_tab)

    '''
    Parametr polacz - łączy z istniejąca tabelą, jeśli 'True', w przeciwnym razie dodaje nową tabelę
    '''
    def wczytajTabZPliku(self, file_path = "", nazwa_tab = "", polacz=True):
        if file_path[-4:len(file_path)] == ".csv": read_func = pd.read_csv
        elif file_path[-5:len(file_path)] == ".xlsx": read_func = pd.read_excel
        else: raise BadFileFormatError("Format pliku z tabelą musi mieć rozszerzenie .csv lub .xlsx")

        new_df = read_func(file_path)
        if polacz:
            self.__posiadacze_[self.__posiadaczPos_].dolaczDoTab(nazwa_tab, new_df)
        else:
            self.__posiadacze_[self.__posiadaczPos_].dodajTabDF(nazwa_tab, new_df)

    def dodajWierszTabWydatki(self, nazwa_tab: str, nowy_wiersz = []):
        self.__posiadacze_[self.__posiadaczPos_].dodajWierszWTab(nowy_wiersz, nazwa_tab)

    def przesunWPrawo(self):
        if self.__posiadaczPos_ == -2:
            raise OutOfBondsError("Pusta lista Posiadaczy")
        else:
            self.__posiadaczPos_ += 1
            if self.__posiadaczPos_ == len(self.__posiadacze_): self.__posiadaczPos_ = 0
    
    def przesunWLewo(self):
        if self.__posiadaczPos_ == -2:
            raise OutOfBondsError("Pusta lista Posiadaczy")
        else:
            self.__posiadaczPos_ -= 1
            if self.__posiadaczPos_ == -1: self.__posiadaczPos_ = len(self.__posiadacze_) - 1

    def przejdzNaPoz(self, pozycja_posiadacza = 0):
        if self.__posiadaczPos_ == -2: raise OutOfBondsError("Pusta lista Posiadaczy")
        else: self.__posiadaczPos_ = pozycja_posiadacza

    def drukujTabWydatki(self, nazwa):
        print(self.__posiadacze_[self.__posiadaczPos_].podajTabDF(nazwa))

    def podajListePosiadaczy(self):
        out_list = []
        for posiadacz in self.__posiadacze_:
            dane = posiadacz.podajImieINazw()
            out_list.append(dane[0] + " " + dane[1])

        return out_list
    
    def podajListeNazwTabWydatkow(self):
        return self.__posiadacze_[self.__posiadaczPos_].podajNazwyTabWydatkow()
    
    '''
    W tym przypadku chodzi o posiadacza na aktualnie ustawionej pozycji na liście
    '''
    def podajDanePosiadacza(self):
        return self.__posiadacze_[self.__posiadaczPos_].podajImieINazw()
