from Fundamenty import *

class Interfejs:
    def __init__(self) -> None:
        self.__posiadacze_ = list(Posiadacz)
    
    def utworzPosiadacza(self, imie = "Jan", nazwisko = "Kowalski"):
        self.__posiadacze_.append(Posiadacz(imie, nazwisko))

    def dodajTabWydatki(self, posiadacz_hash, nazwa: str, kolumny: list(str)):
        for posiadacz in self.__posiadacze_:
            if posiadacz.podajHash() == posiadacz_hash:
                nowa_tab = TabWydatki(nazwa, kolumny)
                posiadacz.dodajTab(nowa_tab)

         