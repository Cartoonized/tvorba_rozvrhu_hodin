import copy
import pomocne_funkce


def Proved_Hodnoceni_Predmetu(pppdv: list[list[int]], vyucujici_casy: list[list[list[int]]], predmety: list[str], seznam_delkaPredmetu_predmet: list[int], preference_mistnosti: list[list[int]], pppdo: list[list[int]], index_vlivu: list[int]) -> list[float]:
    """
    funkce, která hodnotí předměty
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param vyucujici_casy: v řádcích jsou vyučující, ve sloupcích dny, 1 -> má volno, 0 -> nemá volno
    :param predmety: seznam předmětů
    :param seznam_delkaPredmetu_predmet: index je predmet, hodnota je delka prednasky
    :param preference_mistnosti: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = poradi
    :param pppdo: pokud je ve sloupci více nenulových čísel -> pro tyto řádky(obory) je tento sloupec(předmět) společný
    :param index_vlivu: seznam vlivů na každou složku hodnocení předmětů
    :return: seznam hodnocení předmětů
    """
    pom_seznam = []
    seznam_hodnoceni_predmetu = []
    for predmet in range(len(predmety)):
        seznam_vyucujicich_tohoto_predmetu = Zjisti_Seznam_Vyucujicich(pppdv, predmet)

        pocet_vyucujicich = len(seznam_vyucujicich_tohoto_predmetu)  # 1.
        pocet_prednasek = Zjisti_Pocet_Vyucovanych_Prednasek(pppdv, seznam_vyucujicich_tohoto_predmetu, predmet)
        delka_prednasky = seznam_delkaPredmetu_predmet[predmet]  # 6.
        pocet_volnych_hodin = pomocne_funkce.Zjisti_Pocet_Volnych_Hodin(vyucujici_casy, seznam_vyucujicich_tohoto_predmetu)
        pocet_vyucovanych_hodin = pocet_prednasek * delka_prednasky

        pomer_VyucH_ku_VolH = pocet_vyucovanych_hodin / pocet_volnych_hodin  # 2.

        pocet_mistnosti = pomocne_funkce.Zjisti_Pocet_Mistnosti(preference_mistnosti, predmet)  # 3.
        pocet_oboru_predmetu = len(pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, predmet))  # 4.
        den_kdy_hlavne_uci = Zjisti_JakyDenPrevazneUci(vyucujici_casy, seznam_vyucujicich_tohoto_predmetu) + 1
        """
        seznam_hodnoceni_predmetu.append(pocet_vyucujicich*index_vlivu[0]       # čím více tím později  (-)
                                         + pomer_VyucH_ku_VolH*index_vlivu[1]   # čím větší tím dříve   (+)
                                         + pocet_mistnosti*index_vlivu[2]       # čím větší tím později (-)
                                         + pocet_oboru_predmetu*index_vlivu[3]  # čím větší tím dříve   (+)
                                         + delka_prednasky*index_vlivu[4]       # čím větší tím dříve   (+)
                                         + den_kdy_hlavne_uci*index_vlivu[5])   # čím větší tím později (-)
        """
        pom_seznam.append([pocet_vyucujicich, pomer_VyucH_ku_VolH, pocet_mistnosti, pocet_oboru_predmetu, delka_prednasky, den_kdy_hlavne_uci])

    # transpozice seznamu pro snadnější práci
    transponovane = list(zip(*pom_seznam))

    # funkce pro normalizaci min-max
    def normalizace(sloupec):
        min_val = min(sloupec)
        max_val = max(sloupec)
        return [(x - min_val) / (max_val - min_val) if max_val > min_val else 0 for x in sloupec]

    # normalizace jednotlivých sloupců
    normalizovane_sloupce = [normalizace(sloupec) for sloupec in transponovane]

    # transpozice zpět do původního tvaru
    normalizovany_seznam = [list(x) for x in zip(*normalizovane_sloupce)]

    seznam_hodnoceni_predmetu = []
    for predmet in range(len(predmety)):
        seznam_hodnoceni_predmetu.append(normalizovany_seznam[predmet][0] * index_vlivu[0]  # čím více tím později  (-)
                                         + normalizovany_seznam[predmet][1] * index_vlivu[1]  # čím větší tím dříve   (+)
                                         + normalizovany_seznam[predmet][2] * index_vlivu[2]  # čím větší tím později (-)
                                         + normalizovany_seznam[predmet][3] * index_vlivu[3]  # čím větší tím dříve   (+)
                                         + normalizovany_seznam[predmet][4] * index_vlivu[4]  # čím větší tím dříve   (+)
                                         + normalizovany_seznam[predmet][5] * index_vlivu[5])  # čím větší tím později (-)
    return seznam_hodnoceni_predmetu


def Zjisti_JakyDenPrevazneUci(vyucujici_casy: list[list[list[int]]], vyucujici: list[int]) -> int:
    """
    Vrací index dne, kdy vyučující může učit nejdéle.
    :param vyucujici_casy: data volných hodin vyučujících
    :param vyucujici: seznam indexů vyučujících
    :return: index dne
    """
    dny = [0, 0, 0, 0, 0]
    for vyuc in vyucujici:
        for den in range(5):
            pocet_jednicek = 0
            for hodina in range(12):
                if vyucujici_casy[vyuc][den][hodina] == 1:
                    pocet_jednicek += 1
            dny[den] += pocet_jednicek
    return dny.index(max(dny))


def Zjisti_Seznam_Vyucujicich(pppdv: list[list[int]], predmet: int) -> list[int]:
    """
    Vrací seznam vyučujících co udí daný předmět.
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param predmet: index předmětu v seznamu předmětů
    :return: vrací seznam vyučujících tohoto předmětu
    """
    seznam = []
    for vyuc in range(len(pppdv)):
        if pppdv[vyuc][predmet] != 0:
            seznam.append(vyuc)
    return seznam


def Zjisti_Pocet_Vyucovanych_Prednasek(pppdv: list[list[int]], seznam_vyucujicich_pro_tento_predmet: list[int], predmet: int) -> int:
    """
    Vrací počet všech vyučovaných přednášek tohoto předmětu.
    :param pppdv: řádky jsou vyučující, sloupce jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param seznam_vyucujicich_pro_tento_predmet: seznam indexů vyučujících co tento předmět vyučují
    :param predmet: index předmětu v seznamu předmětů
    :return: počet přednášek tohoto předmětu k odučení
    """
    pocet_vyucovanych_prednasek = 0
    for vyuc in seznam_vyucujicich_pro_tento_predmet:
        pocet_vyucovanych_prednasek += pppdv[vyuc][predmet]
    return pocet_vyucovanych_prednasek


def Vytvor_SeznamPoradiPredmetu(pppdv: list[list[int]], vyucujici_casy: list[list[list[int]]],
                                seznam_predmetu: list[str], seznam_delkaPredmetu_predmet: list[int],
                                preference_mistnosti: list[list[int]], pppdo: list[list[int]]) -> [list[int], list[int], list[float]]:
    """
    Vytváří všechny možné posloupnosti předmětů s použitím vlivů.
    :param pppdv: řádky jsou vyučující, sloupce jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param vyucujici_casy: data volen vyučujících
    :param seznam_predmetu: seznam s kódy předmětů
    :param seznam_delkaPredmetu_predmet: seznam s délkami předmětů
    :param preference_mistnosti: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = poradi
    :param pppdo: pokud je ve sloupci více nenulových čísel -> pro tyto řádky(obory) je tento sloupec(předmět) společný
    :return: seznam s pořadovými čísly předmětů, použitý vektor vlivů, seznam hodnoocení předmětů
    """
    seznam_vlivu = VytvorVlivy()
    seznam_poradi_predmetu = []
    seznam_hodnoceni = []
    for vliv in seznam_vlivu:
        # ve sloupcích předměty, hodnoty -> hodnocení, čím větší tím je předmět dříve
        predmety_hodnoceni = Proved_Hodnoceni_Predmetu(pppdv,
                                                       vyucujici_casy,
                                                       seznam_predmetu,
                                                       seznam_delkaPredmetu_predmet,
                                                       preference_mistnosti,
                                                       pppdo,
                                                       vliv)
        # predmet_poradi = Vytvor_Posloupnost(predmety_hodnoceni)  # 0. hodnota je index prvku co má být první
        predmet_poradi = sorted(range(len(predmety_hodnoceni)), key=lambda i: predmety_hodnoceni[i], reverse=True)
        pom_seznam = copy.deepcopy(predmety_hodnoceni)
        for i in range(len(predmet_poradi)):
            pom_seznam[predmet_poradi[i]] = i
        seznam_poradi_predmetu.append(predmet_poradi)
        seznam_hodnoceni.append(predmety_hodnoceni)
    return seznam_poradi_predmetu, seznam_vlivu, seznam_hodnoceni


"""
def Vytvor_Posloupnost(seznam_hodnoceni: list[float]) -> list[int]:

    Vytváří seznam pořadí předmětů, ve kterém se budou zapisovat do rozvrhu.
    :param seznam_hodnoceni: seznam hodnot hodnocení
    :return: seznam pořadí předmětů

    skup_hodnota = []  # slovník, [[předmětX, předmětY, ...]: hodnota, [předmětZ, předmětW, ...]: hodnota]
    for hodnota in seznam_hodnoceni:
        seznam_indexu_se_stejnou_hodnotou = []
        for stejna_hodnota in range(len(seznam_hodnoceni)):
            if hodnota == seznam_hodnoceni[stejna_hodnota]:
                seznam_indexu_se_stejnou_hodnotou.append(stejna_hodnota)
        if skup_hodnota:
            je_tam = False
            for skup in skup_hodnota:
                for index in skup[0]:
                    if index == seznam_indexu_se_stejnou_hodnotou[0]:
                        je_tam = True
                        break
            if not je_tam:
                skup_hodnota.append(copy.deepcopy([seznam_indexu_se_stejnou_hodnotou, hodnota]))
        else:
            skup_hodnota.append(copy.deepcopy([seznam_indexu_se_stejnou_hodnotou, hodnota]))
    seznam_poradi = Uprav_Skupiny(skup_hodnota)
    return seznam_poradi
"""


def Uprav_Skupiny(skup: dict[list[int]: float]) -> list[int]:
    """
    Vytváří seznam s pořadovými čísly předmětů.
    :param skup: slovník, [[předmětX, předmětY, ...]: hodnota, [předmětZ, předmětW, ...]: hodnota], ...
    :return: seznam s pořadovými čísly předmětů
    """
    posl = []
    pocet_skupin = len(skup)
    index_skup = 0
    for k in range(pocet_skupin):
        indexy_ve_skupine = []
        max = skup[0][1]
        for skupina in range(len(skup)):
            if skup[skupina][1] > max:
                max = skup[skupina][1]
                indexy_ve_skupine = skup[skupina][0]
                index_skup = skupina
        if max == skup[0][1]:
            index_skup = 0
            indexy_ve_skupine = skup[0][0]
        for index in indexy_ve_skupine:
            posl.append(index)
        del skup[index_skup]
    return posl


def VytvorVlivy() -> list[list[int]]:
    """
    Vytváří vlivy, kterými násobím složky hodnocení předmětů.
    :return: seznam vektorů
    """
    vlivy = []
    for pocet_vyucujicich in range(-2, 1):
        for pomer in range(8, 12):
            for pocet_mistnosti in range(-2, 1):
                for pocet_oboru in range(0, 3):
                    for delka_prednasky in range(0, 3):
                        for den_kdy_hlavne_uci in range(-5, 1):
                            vlivy.append([pocet_vyucujicich,
                                          pomer,
                                          pocet_mistnosti,
                                          pocet_oboru,
                                          delka_prednasky,
                                          den_kdy_hlavne_uci])
    return vlivy
