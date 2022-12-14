def rezie(prompt: str = '', fce = str, odmitnuti: str = '', prikaz: str = '', special: tuple = ()):
    """
    Vraci zadany vstup, jenz prosel funkci fce, popripade vstup nezmeneny,
    ktery byl v n-tici special.
    :param prompt: prikaz, kterym je uzivatel vyzvan k zadani vstupu
    :param fce: funkce, pres kterou ma vstup projit a byt zmenen
    :param odmitnuti: zprava informujici uzivatele o nevalidnim vstupu
                      Pokud je odmitnuti nastaveno na '', vypise se
                      printem vyjimka z Pythonu
    :param prikaz: prikaz, jenz uzivateli rika, co ma zadat (vypisuje se
                   jen poprve pred prvnim promptem)
                   Pokud je prikaz nastaven na '', nevypisuje se
    :param special: n-tice vstupu, ktere nemuseji prochazet funkci fce
    :return: object
    """

    if prikaz:
        print(prikaz)
    vystup = None
    while vystup == None:
        vstup = input(prompt)
        if vstup in special:
            vystup = vstup
        try:
            vystup = fce(vstup)
        except Exception as err:
            if odmitnuti:
                print(odmitnuti)
            else:
                print(err)
    return vystup