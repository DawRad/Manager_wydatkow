from Fundamenty import *

class Interfejs:
    def __init__(self) -> None:
        self.__posiadacze_ = list(Posiadacz)
    
    def utworzPosiadacza(self, idx = 1, imie = "Jan", nazwisko = "Kowalski"):
        self.__posiadacze_.append(Posiadacz(idx, imie, nazwisko))