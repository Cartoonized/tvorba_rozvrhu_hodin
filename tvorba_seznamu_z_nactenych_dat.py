# from typing import Union
# rozvrh = list[list[list[list[Union[list[int], list[[]]]]]]]
rozvrh_type = list


def Priprav_Seznam_Vyuc(seznam):
    seznam_vyucujicich = []
    seznam_vyucujicich.append(seznam[0][0])
    for radek in range(len(seznam)):
        je_tam = False
        for prvek in seznam_vyucujicich:
            if prvek == seznam[radek][0]:
                je_tam = True
                break
        if not je_tam:
            seznam_vyucujicich.append(seznam[radek][0])
    return seznam_vyucujicich


def Priprav_Seznam_Oboru(seznam):
    seznam_oboru = []
    seznam_oboru.append(seznam[0][0])
    for radek in range(len(seznam)):
        je_tam = False
        for obor in seznam_oboru:
            if obor == seznam[radek][0]:
                je_tam = True
                break
        if not je_tam:
            seznam_oboru.append(seznam[radek][0])
    return seznam_oboru


def Priprav_Seznam_Mistnosti(seznam):
    seznam_mistnosti = []
    seznam_mistnosti.append(seznam[0][1])
    for radek in range(len(seznam)):
        je_tam = False
        for mistnost in seznam_mistnosti:
            if mistnost == seznam[radek][1]:
                je_tam = True
                break
        if not je_tam:
            seznam_mistnosti.append(seznam[radek][1])
    return seznam_mistnosti


def Priprav_Seznam_Predmetu(seznam):
    seznam_predmetu = []
    seznam_predmetu.append(seznam[0][1])
    for radek in range(len(seznam)):
        je_tam = False
        for predmet in seznam_predmetu:
            if predmet == seznam[radek][1]:
                je_tam = True
                break
        if not je_tam:
            seznam_predmetu.append(seznam[radek][1])
    return seznam_predmetu


def Vytvor_Matici(radky, sloupce):
    seznam = []
    for radek in range(len(radky)):
        row = []
        for sloupec in range(len(sloupce)):
            row.append(0)
        seznam.append(row)
    return seznam


def Vytvor_DP(seznam_predmet_delkaPredmetu, predmety):
    seznam_delek_predmetu = []
    # print(f"seznam_predmet_delkaPredmetu: {len(seznam_predmet_delkaPredmetu)}")
    for predmet_in_p in range(len(predmety)):
        for radek in range(len(seznam_predmet_delkaPredmetu)):
            if predmety[predmet_in_p] == seznam_predmet_delkaPredmetu[radek][0]:
                seznam_delek_predmetu.append(int(seznam_predmet_delkaPredmetu[radek][1]))
    return seznam_delek_predmetu


def Vytvor_PPPDO(seznam: list[list[str]], obory: list[str], predmety: list[str]) -> list[list[int]]:  # dříve pocet_potrebnych_prednasek_dle_trid_zaku
    # index řádku = index oboru v seznamu 'obory'
    # index sloupce = index předmětu v seznamu 'predmety'
    # hodnoty = počet přednášek u tohoto oboru(řádek) tohoto předmětu(sloupec)
    # potřeba -> obory, předměty, počet_přednášek
    """
    vem obor(řádek) a pro každý předmět(sloupec), zapisuj 0 (není u tohoto oboru) nebo číslo udávájící počet
    požadovaných oborem přednášek tohot předmětu
    :param seznam: seznam_obor_predmet (data z csv)
    :param obory: seznam oborů
    :param predmety: seznam předmětů
    :return: pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný -> (2d pole)
    """

    # předvytvoření tabulky
    pppdtz = Vytvor_Matici(obory, predmety)

    """
    najdu vybraný obor spolu s vybraným předmětem v seznamu a zapíšu hodnotu
    tím se zapíší hodnoty u předmětů, které k oboru patří
    poté se do nevyplněných míst zapíše 0
    """
    for obor in range(len(obory)):
        for predmet in range(len(predmety)):
            for radek in range(len(seznam)):
                if obory[obor] == seznam[radek][0]:
                    if predmety[predmet] == seznam[radek][1]:
                        pppdtz[obor][predmet] = int(seznam[radek][2])
    return pppdtz


def Vytvor_PPPDV(seznam: list[list[str]], vyucujici: list[str], predmety: list[str]) -> list[list[int]]:
    # potřebuji seznam s vyucujici_predmet_pocetPrednasek

    # index řádku = index vyucujiciho v seznamu 'vyucujici'
    # index sloupce = index předmětu v seznamu 'predmety'
    # hodnoty = počet přednášek u tohoto vyucujiciho(řádek) tohoto předmětu(sloupec)
    # potřeba -> vyučuiící, předměty, počet_přednášek
    """
    :param seznam: seznam_vyucujici_predmet_pocetPrednasek (načtená data z csv)
    :param vyucujici: seznam vyučujících
    :param predmety: seznam předmětů
    :return: 2d pole, kde v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    """
    # předvytvoření tabulky
    pppdv = Vytvor_Matici(vyucujici, predmety)

    """
    najdu vybraný obor spolu s vybraným předmětem v seznamu a zapíšu hodnotu
    tím se zapíší hodnoty u předmětů, které k oboru patří
    poté se do nevyplněných míst zapíše 0
    """
    for vyuc in range(len(vyucujici)):
        for predmet in range(len(predmety)):
            for radek in range(len(seznam)):
                if vyucujici[vyuc] == seznam[radek][0]:
                    if predmety[predmet] == seznam[radek][1]:
                        pppdv[vyuc][predmet] = int(seznam[radek][2])
    return pppdv


def Vytvor_PrefMist(seznam: list[list[str]], mistnosti: list[str], predmety: list[str]) -> list[list[int]]:
    """
    Vytváří seznam povolených místností pro předměty.
    :param seznam: seznam_predmet_mistnost_poradi (data načtená z csv)
    :param mistnosti:
    :param predmety:
    :return: 2d pole, kde v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    """
    # předvytvoření tabulky
    pref_mist = Vytvor_Matici(mistnosti, predmety)

    for mistnost in range(len(mistnosti)):
        for predmet in range(len(predmety)):
            for radek in range(len(seznam)):
                if mistnosti[mistnost] == seznam[radek][1]:
                    if predmety[predmet] == seznam[radek][0]:
                        pref_mist[mistnost][predmet] = int(seznam[radek][2])
                        # pref_mist[mistnost][predmet] = 1
    return pref_mist


def Vytvor_Casy(seznam: list, pom: list[str], upozorneni: list[str], index_seznamu: int) -> list[list[list[int]]]:
    """
    Vytváří seznam volných hodin.
    Zohlednuje také situaci, kdy v json souborech nejsou data o vyučujícím/místnosti, které jsou v seznamu
    vyučujících/místnosti -> je volno vždy.
    :param seznam: seznam, ze kterého budu čerpat data (seznam_mistnosti_casy/seznam_vyucujici_casy)
    :param pom: seznam určující pořadí (seznam_mistnosti/seznam_vyucujicich)
    :param upozorneni: seznam, do kterého se ukládají upozornění o automatickému přidání místnosti/vyučujícího
    :param index_seznamu: index seznamu -- vyučující = 0, místnosti = 1
    :return: data o dnech a hodinách, kdy je volno
    """
    seznam_casy = []
    for p in range(len(pom)):
        je_tam = False
        index = 0
        for radek in range(len(seznam)):
            if seznam[radek][0] == pom[p]:
                index = radek
                je_tam = True
                break
        if je_tam:
            seznam_casy.append(seznam[index][1])
        else:
            seznam_casy.append([[1] * 12 for _ in range(5)])
            if index_seznamu == 0:
                upozorneni.append(f"[UPOZORNENI] V souboru vyucujici_casy.json chybí vyučující {pom[p]} a byl přidán automaticky!")
            else:
                upozorneni.append(f"[UPOZORNENI] V souboru mistnosti_casy.json chybí místnost {pom[p]} a byla přidána automaticky!")
    return seznam_casy


def Vytvor_Tabulku_Obsazenosti(obory) -> list[list[list[int]]]:
    """
    Vytváří prázdný seznam volných hodin.
    :param obory: seznam oborů
    :return: v řádcích jsou obory, ve sloupcích dny s hodinami, obs[obor][den][hodina] == 1 -> má volno, == 0 -> nemá volno
    """
    seznam = []
    for r in range(len(obory)):
        row = []
        for s in range(5):
            col = []
            for hodina in range(12):
                col.append(1)
            row.append(col)
        seznam.append(row)
    return seznam


def Vytvor_Prazdny_Rozvrh(pocet_oboru: int) -> rozvrh_type:
    """
    Vytváří prázdný rozvrh.
    :param pocet_oboru: počet oborů
    :return: prázdná šablona rozvrhu
    """
    rozvrh = []
    for obor in range(pocet_oboru):
        row = []
        for den in range(5):
            col = []
            for cas in range(12):
                col.append([])
            row.append(col)
        rozvrh.append(row)
    return rozvrh


