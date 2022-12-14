class Pojistenec:
    '''
    Uchovava v sobe instanci pojistence s vlastnostmi:
    jmeno, prijmeni, vek, telefonni cislo
    '''

    def __init__(self, jmeno, prijmeni, vek, telefon):
        self.__jmeno, self.__prijmeni, self.__vek, self.__telefon = jmeno, prijmeni, vek, telefon

    def __str__(self):
        return f'{self.__jmeno} {self.__prijmeni}'

    @property
    def jmeno(self):
        return self.__jmeno

    @property
    def prijmeni(self):
        return self.__prijmeni

    @property
    def telefon(self):
        return self.__telefon
    
    @property
    def vek(self):
        return self.__vek

    def toString(self):
        return str(self)