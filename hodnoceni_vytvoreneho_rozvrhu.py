# from typing import Union

# rozvrh_type = list[list[list[list[Union[list[int], list[[]]]]]]]
rozvrh_type = list


def Ohodnot_Rozvrh(vytvorene_rozvrhy: list[rozvrh_type], rozvrh: rozvrh_type, pppdo: list[list[int]],
                   seznam_predmetu: list[str], pouzite_vlivy: list[int], seznam_vlivu_vytvorenych_rozvrhu: list[list[int]],
                   seznam_vliv_predmety_hodnoty_nezapsaneP, predmety_dle_poradi: list[int], hodnoty_premetu: list[float]) -> [list[list[int]], list]:
    """

    :param vytvorene_rozvrhy: seznam všech vytvořených rozvrhů
    :param rozvrh: vytvořený rozvrh
    :param pppdo: data předmětů oborů
    :param seznam_predmetu:
    :param pouzite_vlivy: "vektor" (seznam) vlivů
    :param seznam_vlivu_vytvorenych_rozvrhu: seznam "vektorů" (seznamů) vlivů
    :param seznam_vliv_predmety_hodnoty_nezapsaneP: seznam s pomocnými daty
    :param predmety_dle_poradi: seznam pořadí předmětů
    :param hodnoty_premetu: seznam hodnocení předmětů
    :return: seznam nezapsaných předmětů, seznam s pomocnými daty
    """
    nezapsane_predmety = Najdi_Nezapsane_Predmety(pppdo, seznam_predmetu)
    if len(nezapsane_predmety) == 0:
        # pocet_volnych_dni = Zjisti_Pocet_Volnych_Dni(rozvrh)
        # pocet_mezer_mezi_predmety = Zjisti_Pocet_Mezer(rozvrh)
        # print(f"Počet volných dní: {pocet_volnych_dni}, počet mezer mezi předměty: {pocet_mezer_mezi_predmety}")
        if seznam_vlivu_vytvorenych_rozvrhu:
            seznam_vlivu_vytvorenych_rozvrhu.append(pouzite_vlivy)
        vytvorene_rozvrhy.append(rozvrh)
    else:
        seznam_predmetu_dle_poradi = []
        for p in range(len(seznam_predmetu)):
            seznam_predmetu_dle_poradi.append(seznam_predmetu[predmety_dle_poradi[p]])

        seznam_vliv_predmety_hodnoty_nezapsaneP.append([pouzite_vlivy,
                                                        seznam_predmetu_dle_poradi,
                                                        hodnoty_premetu,
                                                        nezapsane_predmety])

    return nezapsane_predmety, seznam_vliv_predmety_hodnoty_nezapsaneP


def Najdi_Nezapsane_Predmety(pppdo: list[list[int]], predmety: list[str]) -> list[list[int]]:
    """
    Vrací seznam dvojic předmět-počet_přednášek nezapsaných předmětů
    :param pppdo: pokud je ve sloupci více nenulových čísel -> pro tyto řádky(obory) je tento sloupec(předmět) společný
    :param predmety: seznam předmětů
    :return: seznam dvojic [index_předmětu, počet_přednášek]
    """
    seznam_nezapsanych_predmetu = []
    for obor in range(len(pppdo)):
        for p in range(len(pppdo[obor])):
            if pppdo[obor][p] != 0:
                if seznam_nezapsanych_predmetu:
                    je_tam = False
                    for predmet in seznam_nezapsanych_predmetu:
                        if predmet[0] == predmety[p]:
                            je_tam = True
                    if not je_tam:
                        seznam_nezapsanych_predmetu.append([p, pppdo[obor][p]])
                else:
                    seznam_nezapsanych_predmetu.append([p, pppdo[obor][p]])
    return seznam_nezapsanych_predmetu


"""
def Zjisti_Pocet_Volnych_Dni(rozvrh: rozvrh_type) -> int:
    
    :param rozvrh: vytvořený rozvrh
    :return: celkový počet volných dní přes všechny obory
    
    pocet_volnych_dni = 0
    for obor in range(len(rozvrh)):
        for den in range(len(rozvrh[obor])):
            prazdne_casy = 0
            for cas in rozvrh[obor][den]:
                if not cas:
                    prazdne_casy += 1
            if prazdne_casy == 12:
                pocet_volnych_dni += 1
    return pocet_volnych_dni
"""


"""
def Zjisti_Pocet_Mezer(rozvrh: rozvrh_type) -> int:
    
    :param rozvrh: vytvořený rozvrh
    :return: celkový počet volných hodin mezi předměty přes všechny obory
    
    pocet_mezer = 0
    for obor in range(len(rozvrh)):
        for den in range(5):
            interval = Zjisti_Interval(rozvrh, obor, den)
            for hodina in range(interval[0], interval[1]):
                if not rozvrh[obor][den][hodina]:
                    pocet_mezer += 1
    return pocet_mezer
"""


def Zjisti_Interval(rozvrh: rozvrh_type, obor: int, den: int) -> list[int]:
    """
    Vrací dvě hodnoty určující interval
    :param rozvrh: vytvořený rozvrh
    :param obor: index oboru
    :param den: index dne (0-4)
    :return: seznam, od: první vyučovaná hodina, do: poslední vyučovaná hodina (tento den)
    """
    od = 0
    do = 0
    for cas in range(0, 12):
        if rozvrh[obor][den][cas]:
            od = cas
            break
    for cas in range(11, -1, -1):
        if rozvrh[obor][den][cas]:
            do = cas
            break
    return [od, do]


