"""
Rezie pro uzivatele pro rezimy:
vypis, zapis, smazat, ulozit
"""

def zapis(instance_pojist) -> bool:
    """
    Vstupni rezie pro zapis novych pojistencu od uzivatele.
    :param instance_pojist: instance tridy PojisteniData
    :return: True/False <=> byl pridan pojistenec/nebyl pridan
    """

    pridan_pojistenec = False
    ne = "nn"
    while True:
        print("\nZadejte...")
        jmeno = input("jméno: ")
        if jmeno == ne:
            break
        prijmeni = input("příjmení: ")
        vek = input("věk: ")
        telefon = input("telefon: ")
        try:
            instance_pojist.zapis(jmeno, prijmeni, vek, telefon)
            pridan_pojistenec = True
            print(f"{jmeno.capitalize()} {prijmeni.capitalize()} zapsán do databáze.")
        except Exception as err:
            print(err)
    return pridan_pojistenec

def vypis(instance_pojist) -> None:
    """
    Vstupni rezie pro vypis z databaze pojistencu.
    :param instance_pojist: instance tridy PojisteniData
    :return: None
    """

    if not instance_pojist.data:
        print("Databáze pojištěnců je prázdná.")
        return None
    ne = "nn"
    prompt = ": "
    while True:
        print("""\nZadejte ID, jméno, příjmení, věk nebo telefon pojištěnce, kterého chcete najít.
Pro výpis všech pojištěnců zadejte Enter.""")
        pozadavek = input(prompt)
        if pozadavek == ne:
            break
        nalezene_shody = instance_pojist.vypis_jednoduchy(pozadavek)
        if nalezene_shody:
            print()
        for ID in nalezene_shody:
            print(f"{ID} {nalezene_shody[ID].jmeno} {nalezene_shody[ID].prijmeni} {nalezene_shody[ID].vek} {nalezene_shody[ID].telefon}")
        if not nalezene_shody:
            print("0 nalezených shod")
        if len(nalezene_shody) > 5:
            print(f"Nalezeno {len(nalezene_shody)} pojištěnců.")

def smazat(instance_pojist) -> bool:
    """
    Vstupni rezie pro mazani pojistencu v databazi.
    Vstup od uzivatele se porovna s hodnotami vlastnosti vsech pojistencu a
    vsechny nalezene shody se pak uzivateli predlozi k rozhodnuti, jakeho
    pojistence chce smazat.
    :param instance_pojist: instance tridy PojisteniData
    :return: True/False <=> byl smazan pojistenec/nebyl smazan
    """

    ano = "aa"
    ne = "nn"
    prompt = ": "
    smazan_pojistenec = False
    while True:
        print("\nZadejte ID, jméno, příjmení, věk nebo telefon pojištěnce, kterého chcete smazat.")
        pozadavek = input(prompt)
        if pozadavek == ne:
            break
        nalezene_shody = instance_pojist.vypis_jednoduchy(pozadavek)
        if not nalezene_shody:
            # zadna shoda
            print("0 nalezených shod")
            continue
        # alespon jedna shoda byla nalezena
        shody_ID, shody_instance = list(nalezene_shody.keys()), list(nalezene_shody.values())
        if len(nalezene_shody) == 1:
            # prave jedna shoda
            while True:
                print("""\nChcete smazat tohoto pojištěnce?
{0[0]} {1[0].jmeno} {1[0].prijmeni} {1[0].vek} {1[0].telefon}""".format(shody_ID, shody_instance))
                odpoved = input(f"({ano}/{ne}): ")
                if odpoved == ano:
                    instance_pojist.smaz(shody_ID[0])
                    smazan_pojistenec = True
                    print("{0[0].jmeno} {0[0].prijmeni} smazan.".format(shody_instance))
                    break
                elif odpoved == ne:
                    break
                else:
                    print(f"Takovou odpoved neumim zpracovat, zadejte prosím {ano} | {ne}.")
        else:
            # alespon 2 shody
            while True:
                print("\nVyberte ID pojištěnce, kterého chcete smazat:")
                for aktual_ID in shody_ID:
                    print(f"{aktual_ID} {nalezene_shody[aktual_ID].jmeno} {nalezene_shody[aktual_ID].prijmeni} {nalezene_shody[aktual_ID].vek} {nalezene_shody[aktual_ID].telefon}")
                vst_ID = input(prompt)
                if vst_ID == ne:
                    break
                if vst_ID in shody_ID:
                    instance_pojist.smaz(vst_ID)
                    smazan_pojistenec = True
                    print(f"{nalezene_shody[vst_ID].jmeno} {nalezene_shody[vst_ID].prijmeni} smazan.")
                    break
                else:
                    print("Vaše ID není v databázi nalezených pojištěnců.")
    return smazan_pojistenec

def ulozit(instance_pojist) -> None:
    """
    Vstupni rezie pro potvrzeni / odmitnuti ulozeni zmen do txt dokumentu.
    :param instance_pojist: instance tridy PojisteniData
    :return: None
    """

    ano = "aa"
    ne = "nn"
    while True:
        print("\nChcete uložit změny do databáze pojištěnců?")
        odpoved = input(f"({ano}/{ne}): ")
        if odpoved == ano:
            try:
                instance_pojist.uloz("pojisteni_data.txt")
                print("Změny byly uloženy.")
                break
            except Exception as err:
                print(err)
        elif odpoved == ne:
            break
        else:
            print(f"Takovou odpoved neumim zpracovat, zadejte prosím {ano} | {ne}.")