class PojisteniData:
    '''
    Z textoveho dokumentu sestavi a nasledne uchovava slovnik vsech pojistenych
    osob. Textovy dokument musi byt ulozen ve stejnem adresari jako program,
    ktery k nemu pristupuje.

    Struktura slovniku pojistenych:
    {ID: instance tridy Pojistenec}
    (Kazdy pojistenec ma svuj jedinecny ID klic.)

    Prostrednictvim teto tridy je mozno vypisovat, zapisovat a mazat data vsech
    pojistenych.
    '''

    def __init__(self):
        '''
        Sestavi z dat z textoveho dokumentu "pojisteni_data.txt" nebo
        "pojisteni_data(x).txt", kde x je cislo, slovnik vsech pojistenych
        a ulozi jej do instance.
        V pripade, ze dokument neexistuje, vytvori dokument novy prazdny a
        slovnik pojistenych pro praci v instanci pak bude taktez prazdny.
        '''

        self._vrat_data()

    @property
    def data(self) -> dict:
        return self._data

    def smaz(self, ID: str) -> None:
        '''
        Smaze pojistence podle ID.
        :param ID: ID pojistence
        :return: None
        '''

        try:
            del self._data[ID]
        except KeyError:
            raise ValueError(f'{type(self).__name__}: Pojištěnec s ID {ID} neexistuje.')

    def uloz(self, nazev_txt: str = '') -> None:
        '''
        Ulozi do zadane adresy txt dokumentu upraveny slovnik pojistencu.
        Pokud adresa neni zadana, data se ulozi do dokumentu s vygenerovanym nazvem.
        :param nazev_txt: adresa txt dokumentu
        :return: None
        '''

        def _vytvor_nazev_txt(puvodni_nazev_txt: str) -> str:
            '''
            Vytvori nazev noveho txt dokumentu na zaklade nazvu stareho.
            :param puvodni_nazev_txt: puvodni nazev txt dokumentu
            :return:
            '''

            vychozi_nazev = 'pojisteni_data.txt'
            if puvodni_nazev_txt == vychozi_nazev:
                return 'pojisteni_data(1).txt'
            index_leve_zavorky = puvodni_nazev_txt.index('(')
            index_prave_zavorky = puvodni_nazev_txt.index(')')
            aktual_cislo = puvodni_nazev_txt[index_leve_zavorky + 1:index_prave_zavorky]
            nove_cislo = int(aktual_cislo) + 1
            return f'{puvodni_nazev_txt[:index_leve_zavorky + 1]}{nove_cislo}).txt'

        vychozi_nazev = 'pojisteni_data.txt'

        if not nazev_txt:
            # nazev neni zadan
            if not self._nase_txt:
                # v adresari neni ulozeny zadny nas txt dokument
                nazev_txt = vychozi_nazev
            else:
                # v adresari je ulozeny alespon jeden nas txt dokument
                nazev_txt = _vytvor_nazev_txt(self._nase_txt)
        # je nastaven nazev txt dokumentu pro ulozeni dat
        with open(nazev_txt, mode = 'w', encoding = 'utf-8') as txt:
            for ID in self._data:
                jmeno, prijmeni, vek, telefon = self._data[ID].jmeno, self._data[ID].prijmeni, self._data[ID].vek, self._data[ID].telefon
                txt.write(f'{ID} {jmeno} {prijmeni} {vek} {telefon}\n')

    def vypis(self, ID: str = '', jmeno: str = '', prijmeni: str = '', vek: str = '', telefon: str = '') -> dict:
        '''
        Vraci slovnik vsech nalezenych pojistencu podle zadanych vlastnosti.
        Pokud je nektera z vlastnosti nastavena na '', pak se podle ni
        nevyhledava.
        Pokud jsou vsechny vlastnosti nastavene na '', vrati se obsah cele databaze.
        :param ID: ID pojistence
        :param jmeno: jmeno pojistence
        :param prijmeni: prijmeni pojistence
        :param vek: vek pojistence
        :param telefon: telefonni cislo pojistence
        :return: slovnik vyhledanych pojistencu
        '''

        vyhledani_pojistenci = {}
        # je vyhledavano podle ID
        if ID:
            if ID in self._data:
                return {ID: self._data[ID]}
            return {}
        # neni vyhledavano podle ID
        for ID in self._data:
            if jmeno and self._data[ID].jmeno != jmeno:
                continue
            if prijmeni and self._data[ID].prijmeni != prijmeni:
                continue
            if vek and self._data[ID].vek != vek:
                continue
            if telefon and self._data[ID].telefon != telefon:
                continue
            # vyhovujici pojistenec
            vyhledani_pojistenci[ID] = self._data[ID]
        return vyhledani_pojistenci

    def vypis_jednoduchy(self, hledany_retezec: str) -> dict:
        """
        Vraci vsechny nalezeny shody v datech podle hledaneho retezce.
        Shody jsou vraceny ve slovniku {ID: instance tridy Pojistenec}
        :param hledany_retezec: hledany retezec
        :return: slovnik {ID: instance tridy Pojistenec}
        """

        if not self.data:
            return {}
        nalezene_shody = {}
        maxi_ID = max(self.data.keys(), key=int)
        if hledany_retezec.isdigit() and int(hledany_retezec) <= int(maxi_ID):
            return self.vypis(ID=hledany_retezec)
        hledany_retezec = hledany_retezec.strip().lower()
        for ID in self.data:
            aktual_pojistenec = self.data[ID]
            vlastnosti_pojistence_v_retezci = f"{ID} {aktual_pojistenec.jmeno} {aktual_pojistenec.prijmeni} {aktual_pojistenec.vek} {aktual_pojistenec.telefon}".lower()
            if hledany_retezec in vlastnosti_pojistence_v_retezci:
                nalezene_shody[ID] = aktual_pojistenec
        return nalezene_shody

    def zapis(self, jmeno: str, prijmeni: str, vek: str, telefon: str) -> None:
        '''
        Ulozi do slovniku pojistencu noveho pojistence se zadanymi vlastnostmi.
        :param jmeno: jmeno pojistence
        :param prijmeni: prijmeni pojistence
        :param vek: vek pojistence
        :param telefon: telefonni cislo pojistence
        :return: None
        '''

        from pojistenec import Pojistenec as _Pojist

        if len(jmeno) < 2:
            raise ValueError('Jméno musí obsahovat alespoň 2 znaky.')
        if len(prijmeni) < 2:
            raise ValueError('Příjmení musí obsahovat alespoň 2 znaky.')
        vekovy_limit = 120
        if not vek.isdigit() or vek == '0' or int(vek) > vekovy_limit:
            raise ValueError(f'{type(self).__name__}: Věk musí ležet v intervalu [1; {vekovy_limit}].')
        jmeno = jmeno.lower().capitalize()
        prijmeni = prijmeni.lower().capitalize()
        telefon = telefon.replace(' ', '')
        if not telefon.isdigit() or len(telefon) != 9:
            raise ValueError(f'{type(self).__name__}: Nesprávný formát telefonního čísla. Správný formát je 9 číslic bez mezer.')
        telefony_vsech = (pojisteny.telefon for pojisteny in self._data.values())
        if telefon in telefony_vsech:
            raise ValueError(f'{type(self).__name__}: Zadaný telefon je již v databázi pojištěnců uložený.')
        # vse v poradku
        try:
            nove_ID = int(max(self._data.keys(), key = int)) + 1
        except ValueError:
            nove_ID = 1
        self._data[nove_ID] = _Pojist(jmeno, prijmeni, vek, telefon)

    def _vrat_data(self) -> None:
        '''
        Pokud v adresari s programem vyhovujici txt dokument
        a) neexistuje, pak vytvori prazdny slovnik
        b) existuje prave jeden, pak vytvori slovnik s obsahem tohoto dokumentu
        c) existuje alespon 2x, pak vytvori slovnik s obsahem nejnovejsiho dokumentu
        :return: None
        '''

        import os as _os, re as _re
        from pojistenec import Pojistenec as _Pojist

        def _sestavSlovnik(adresa_txt):
            """
            Vraci sestaveny slovnik z databaze pojistencu z txt dokumentu.
            :param adresa_txt: adresa txt dokumentu - databaze pojistencu
            :return: slovnik {ID: instance tridy Pojistenec}
            """

            data = {}
            with open(adresa_txt, mode='r', encoding='utf-8') as txt:
                for radek in txt:
                    ID, jmeno, prijmeni, vek, telefon = radek[:-1].split(' ')
                    data[ID] = _Pojist(jmeno, prijmeni, vek, telefon)
            return data

        vzor = _re.compile("^pojisteni_data(\(\d+\))?.txt$")
        aktual_adr = _os.getcwd()
        obsah_adr = _os.listdir(aktual_adr)
        data_kandidati = [soubor for soubor in obsah_adr if _re.search(vzor, soubor)]
        if not data_kandidati:
            self._nase_txt = ''
            self._data = {}
            return None
        if len(data_kandidati) == 1:
            nase_txt = data_kandidati[0]
        else:
            # nasleduje vyber nejnovejsiho txt dokumentu
            uplne_adresy_txt = [_os.path.join(aktual_adr, txt) for txt in data_kandidati]
            nase_txt = uplne_adresy_txt[0]
            for txt_kandidat in uplne_adresy_txt:
                if _os.stat(txt_kandidat).st_mtime > _os.stat(nase_txt).st_mtime:
                    nase_txt = txt_kandidat
        self._nase_txt = nase_txt
        # txt dokument je vybran
        # nasleduje vytvoreni a vraceni slovniku pojistencu
        self._data = _sestavSlovnik(nase_txt)
        # data jsou zapsana ve slovniku