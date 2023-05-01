class Obiekt:
    def __init__(self, idx: int) -> None:
        self.nrPorz_ = idx

    def __str__(self) -> str:
        return "Numer porzadkowy: " + str(self.nrPorz_)

class Zasob(Obiekt):
    def __init__(self, idx: int, rodzaj: str, kwota: float) -> None:
        super(idx)
        self.rodzaj_ = rodzaj
        self.kwota_ = kwota

    def __str__(self) -> str:
        return super().__str__() + "\nRodzaj zasobu: " + self.rodzaj_ + "\n" + "Dostepne srodki: " + str(self.kwota_)
