from typing import Union

#rozvrh_type = list[list[list[list[Union[list[int], list[[]]]]]]]
rozvrh_type = list


def Zjisti_PocetJednicekVyuc(vyuc: int, vyucujici_casy: list[list[list[int]]]) -> int:
    """
    Počítá počet volných hodin vyučujícího.
    :param vyuc: index vyučujícího v seznamu vyučujících
    :param vyucujici_casy: v řádcích jsou vyučující, ve sloupcích dny s hodinami, 1 -> má volno, 0 -> nemá volno
    :return: počet volných hodin
    """
    pocet_jednicek = 0
    for den in range(5):
        for cas in range(12):
            if vyucujici_casy[vyuc][den][cas] == 1:
                pocet_jednicek += 1
    return pocet_jednicek


def Najdi_PredmetyVyucujiciho(pppdv: list[list[int]], vyuc: int, seznam_delkaPredmetu_predmet: list[int], seznam_vyuc: list[str]) -> list[list[int]]:
    """
    Hledá indexy předmětů vyučujícího.
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param vyuc: index vyučujícího v seznamu vyučujících
    :param seznam_delkaPredmetu_predmet: seznam délek předmětů
    :param seznam_vyuc: seznam vyučujících
    :return: seznam indedxů předmětů, počtů přednášek a délek
    """
    seznam_predmety_delky = []
    for predmet in range(len(seznam_delkaPredmetu_predmet)):
        if pppdv[vyuc][predmet] != 0:
            seznam_predmety_delky.append([predmet, pppdv[vyuc][predmet], int(seznam_delkaPredmetu_predmet[predmet])])
    return seznam_predmety_delky


def Najdi_Mistnosti_Predmetu(pref_mistnosti: list[list[int]], predmet: int) -> list[int]:
    """
    Hledá povolené místnosti předmětu.
    :param pref_mistnosti: v řádcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param predmet: inndex předmětu v seznamu předmětů
    :return: seřazený seznam použitelných místností
    """
    mist_poradi = []
    mistnosti = []
    for mist in range(len(pref_mistnosti)):
        if pref_mistnosti[mist][predmet] != 0:
            mist_poradi.append([mist, pref_mistnosti[mist][predmet]])  # cislo mistnosti, hodnota poradi
    mist_poradi = sorted(mist_poradi, key=lambda x: x[1])

    for hodnoty in range(len(mist_poradi)):
        mistnosti.append(mist_poradi[hodnoty][0])
    return mistnosti


def Najdi_Cas_Vyucujiciho(casy_vyuc: list[list[list[int]]], vyuc: int, delka_prednasky: int, jiz_vybrane: list[list[int]]) -> list[int]:
    """
    Hledá čas vyučujícího, kdy může začít vyučovat předmět.
    :param casy_vyuc: v řádcích jsou vyučující, ve sloupcích dny s hodinami, 1 -> má volno, 0 -> nemá volno
    :param vyuc: index vyučujícího v seznamu vyučujících
    :param delka_prednasky: délka přednášky
    :param jiz_vybrane: seznam již vybraných časů
    :return: seznam dne a hodiny, od které může vyučovat a dvojice již nebyla použitá dříve
    """
    casy = []
    for den in range(5):
        for cas in range(13 - delka_prednasky):
        # for cas in range(12 - delka_prednasky, -1, -1):
            je_tam = False
            for prvek in jiz_vybrane:
                if prvek[0] == den and prvek[1] == cas:
                    je_tam = True
            if not je_tam:
                ma_volno = True
                for hodina in range(delka_prednasky):
                    if casy_vyuc[vyuc][den][cas + hodina] != 1:
                        ma_volno = False
                if ma_volno:
                    casy = [den, cas]
                    jiz_vybrane.append(casy)
                    return casy
    return casy


def Najdi_Vyucujici_Predmetu(pppdv: list[list[int]], predmet: int) -> list[int]:
    """
    Hledá vyučující předmětu.
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param predmet: index předmětu v seznamu předmětů
    :return: indexy vyučujících co tento předmět vyučují
    """
    indexy_vyuc = []
    for vyuc in range(len(pppdv)):
        if pppdv[vyuc][predmet] != 0:
            indexy_vyuc.append(vyuc)
    return indexy_vyuc


def Zjisti_Je_Mistnost_Volna(obs_mist: list[list[list[int]]], mistnost: int, den_odH: list[int], delka_prednasky: int) -> bool:
    """
    Zjišťuje, zda je mísnost volná.
    :param obs_mist: v řádcích jsou mistnosti, ve sloupcích dny s hodinami, 1 -> je volno, 0 -> není volno
    :param mistnost: index místnosti v seznamu místnotí
    :param den_odH: seznam obsahující den a hodinu, od které má být místnost volná po dobu délky přednášky
    :param delka_prednasky: délka přednášky
    :return: místnost je / není volná
    """
    je_volna = True
    if den_odH[1] <= 12 - delka_prednasky:
        for hodina in range(delka_prednasky):
            if obs_mist[mistnost][den_odH[0]][den_odH[1] + hodina] != 1:
                je_volna = False
                break
    else:
        return False
    if je_volna:
        return True
    else:
        return False


def Zjisti_Ma_Vyucujici_Volno(obs_vyuc: list[list[list[int]]], vyuc: int, den: int, cas: int, delka_prednasky: int) -> bool:
    """
    Zjišťuje, zda vyučující má volno.
    :param obs_vyuc: v řádcích jsou vyučující, ve sloupcích dny s hodinami, 1 -> má volno, 0 -> nemá volno
    :param vyuc: index vyučujícího v seznamu vyučujících
    :param den: index dne (0-4)
    :param cas: index hodiny
    :param delka_prednasky: délka přednášky
    :return: má vyučující volno tento den, od této hodiny po dobu délky přednášky -> bool
    """
    # if cas <= 12 - (delka_prednasky-1):
    if cas <= 12 - delka_prednasky:
        for c in range(delka_prednasky):
            if obs_vyuc[vyuc][den][cas + c] != 1:
                return False
    return True


def Vypis_Vlivy(vlivy: list[list[int]]) -> None:
    """
    Výpis vektorů s vlivy.
    :param vlivy: seznam seznamů vlivů ("seznam vektorů")
    :return: None
    """
    for vliv in vlivy:
        print(vliv)


def Zjisti_CisloPomociKodu(seznam: list[str], kod: str) -> int:
    """
    Zjišťuje index pomocí kódu.
    :param seznam: seznam místností/vyučujících/oborů/předmětů
    :param kod: kód místnosti/vyučujícího/oboru/předmětu
    :return: index v seznamu m/v/o/p
    """
    for x in range(len(seznam)):
        if seznam[x] == kod:
            return x
    return 0


def Zjisti_Pocet_Volnych_Hodin(vyucujici_casy: list[list[list[int]]], seznam_vyucujicich_pro_tento_predmet: list[int]) -> int:
    """
    Zjišťuje počet volných hodin vyučujících zvoleného předměu.
    :param vyucujici_casy: data volných hodin vyučujících
    :param seznam_vyucujicich_pro_tento_predmet: seznam vyučujících co tento předmět vyučují
    :return: počet volných hodin vyučujících tohoto předmětu
    """
    pocet_volnych_hodin = 0
    for vyuc in seznam_vyucujicich_pro_tento_predmet:
        for den in range(5):
            for hodina in range(12):
                if vyucujici_casy[vyuc][den][hodina] == 1:
                    pocet_volnych_hodin += 1
    return pocet_volnych_hodin


def Zjisti_Pocet_Mistnosti(preference_mistnosti: list[list[int]], predmet: int) -> int:
    """
    Zjišťuje počet místností pro tento předmět určených.
    :param preference_mistnosti: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param predmet: index přemětu v seznamu předmětů
    :return: počet povolených místností pro tento předmět
    """
    pocet_mistnosti = 0
    for radek in preference_mistnosti:
        if radek[predmet] != 0:
            pocet_mistnosti += 1
    return pocet_mistnosti


def Zjisti_Obory_Predmetu(pppdo: list[list[int]], predmet: int) -> list[int]:
    """
    Zjišťuje, které obory mají tento předmět.
    :param pppdo: pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný
    :param predmet: index předmětu v seznamu předmětů
    :return: seznam indexů oborů co tento předmět mají mít v rozvrhu
    """
    seznam_oboru_predmetu = []
    for radek in range(len(pppdo)):
        if pppdo[radek][predmet] != 0:
            seznam_oboru_predmetu.append(radek)
    return seznam_oboru_predmetu


def Zjisti_ZdaPredmetJeNapevno(data_o_jiz_zapsanych_p: list[list[str]], seznam_predmetu: list[str], predmet: int) -> bool:
    """
    Zjišťuje, zda je tento předmět zapsán do šablony rozvrhů.
    :param data_o_jiz_zapsanych_p: seznam seznamů dat o předem zapsaných předmětech do rozvrhu
    :param seznam_predmetu: seznam předmětů
    :param predmet: index předmětu v seznamu předmětů
    :return: předmět je/není zapsán předem
    """
    for p in range(len(data_o_jiz_zapsanych_p)):
        if seznam_predmetu[predmet] == data_o_jiz_zapsanych_p[p][0]:
            return True
    return False


def Zjisti_JeVolnoVRozvrhu(rozvrh: rozvrh_type, den: int, cas: int, delka_prednasky: int, obory_predmetu: list[int]) -> bool:
    """
    Zjišťuje, zda je v rozvrhu volno.
    :param rozvrh: rozvrh
    :param den: index dne (0-4)
    :param cas: index hodiny (0-11)
    :param delka_prednasky: délka přednášky
    :param obory_predmetu: seznam indexů oborů co tento předmět mají mít v rozvrhu
    :return: zda, každý z oborů má volno, aby se předmět dal odučit pro všechny obory, pro které je předmět společný
    """
    for obor in range(len(obory_predmetu)):
        for i in range(delka_prednasky):
            if rozvrh[obory_predmetu[obor]][den][cas+i]:
                return False
    return True


def Odstran_OpakPrvkySeznamu(seznam: list) -> list:
    """
    Odstraňuje opakující se prvky seznamu.
    :param seznam: seznam
    :return:
    """
    pom = []
    for i in seznam:
        if i not in pom:
            pom.append(i)
    return pom


def Odstran_OpakujiciSeRozvrhy(rozvrhy: list[rozvrh_type]) -> list[rozvrh_type]:
    """
    Odstraňuje opakující se rozvrhy v seznamu vytvořených.
    :param rozvrhy: seznam vytvořených rozvrhů, kde se rozvrhy mohou opakovat
    :return: seznam jedinečných rozvrhů
    """
    seznam_rozvrhu = []
    for r in range(len(rozvrhy)):
        if r == 0:
            seznam_rozvrhu.append(rozvrhy[r])
        else:
            je_tam = False
            for roz_in_seznam in seznam_rozvrhu:
                if rozvrhy[r] == roz_in_seznam:
                    je_tam = True
                    break
            if not je_tam:
                seznam_rozvrhu.append(rozvrhy[r])
    return seznam_rozvrhu

