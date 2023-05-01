class Obiekt:
    def __init__(self, idx: int) -> None:
        self.nrPorz_ = idx

    def __str__(self) -> str:
        return "Numer porzadkowy: " + str(self.nrPorz_)

class Zasob(Obiekt):
    __liczObZas_ = dict()

    def __init__(self, rodzaj: str, kwota: float) -> None:
        if self.__liczObZas_.get(rodzaj) != None: self.__liczObZas_[rodzaj] += 1
        else: self.__liczObZas_[rodzaj] = 1
        super().__init__(self.__liczObZas_[rodzaj])

        self.rodzaj_ = rodzaj
        self.kwota_ = kwota        

    def __str__(self) -> str:
        return super().__str__() + "\nRodzaj zasobu: " + self.rodzaj_ + "\n" + "Dostepne srodki: " + str(self.kwota_)
    
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