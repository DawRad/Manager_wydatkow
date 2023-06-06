from Fundamenty import *
from Wyjatki import OutOfBondsError

class Interfejs:
    def __init__(self) -> None:
        self.__posiadacze_ = list()
        self.__posiadaczPos_ = -2   # aktualna pozycja na liście posiadaczy (-2 ---> lista pusta)
    
    def utworzPosiadacza(self, imie = "Jan", nazwisko = "Kowalski"):
        self.__posiadacze_.append(Posiadacz(imie, nazwisko))

    def dodajTabWydatki(self, posiadacz_hash, nazwa: str, kolumny: list[str]):
        for posiadacz in self.__posiadacze_:
            if posiadacz.podajHash() == posiadacz_hash:
                nowa_tab = TabWydatki(nazwa, kolumny)
                posiadacz.dodajTab(nowa_tab)

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

    # def drukujTabWydatki(self, posiada)         