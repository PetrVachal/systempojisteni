from pojistenidata import PojisteniData
import rezierezimy
import time

pojist_data = PojisteniData()

navod_pojist = "navod"
zapis_pojist = "zapis"
vypis_pojist = "vypis"
smazat_pojist = "smazat"
rezimy = (zapis_pojist, vypis_pojist, smazat_pojist)
ne = "nn"
navod = f"""
\nProgram Pojist vám zajišťuje celkovou správu nad databází vašich pojištěnců!

V adresáři uložení tohoto programu vám Pojist vytvoří databázi pro ukládání
pojištěnců, jehož správa je prostřednictvím tohoto programu plně ve vašich rukou.
V databázi jakožto v textovém dokumentu je každý pojištěnec uložen s vlastnostmi:
ID    jméno    příjmení    věk    telefon

zápis nových pojištěnců aktivujete příkazem     {zapis_pojist}
výpis pojištěnců aktivujete příkazem            {vypis_pojist}
mazání pojištěnců aktivujete příkazem           {smazat_pojist}

Pro ukončení programu
nebo ukončení daného režimu zadejte příkaz      {ne}"""
odmitnuti_pojist = f"""Takovou odpověď neumím zpracovat, zadejte prosím jeden z platných příkazů.
{zapis_pojist} | {vypis_pojist} | {smazat_pojist}"""
prikaz_pojist = "\nZadejte režim."
prompt_pojist = ": "
uvodni_info = f"""\nVítá vás Pojist!
Program pro správu databáze pojištěnců.
Pokud program neznáte, zadejte '{navod_pojist}'.
"""
doba_rozlouceni = 3
rozlouceni = "Petr Váchal vám děkuje za použití programu. Nashledanou."

instance_pojist = PojisteniData()

print(uvodni_info)
ulozit_zmeny = False
rezim = ''
while rezim != ne:
    print(prikaz_pojist)
    rezim = input(prompt_pojist)
    if rezim == ne:
        if ulozit_zmeny:
            rezierezimy.ulozit(instance_pojist)
        print(rozlouceni)
        time.sleep(doba_rozlouceni)
        exit(0)
    if rezim == navod_pojist:
        print(navod)
        continue
    if rezim not in rezimy:
        print(odmitnuti_pojist)
        continue
    # rezim je zadan spravne
    if rezim == zapis_pojist:
        pridan_pojistenec = rezierezimy.zapis(instance_pojist)
        if pridan_pojistenec:
            ulozit_zmeny = True
    elif rezim == vypis_pojist:
        rezierezimy.vypis(instance_pojist)
    else:
        smazan_pojistenec = rezierezimy.smazat(instance_pojist)
        if smazan_pojistenec:
            ulozit_zmeny = True