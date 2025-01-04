import copy
import hodnoceni_vytvoreneho_rozvrhu
import pomocne_funkce
import tvorba_seznamu_z_nactenych_dat
import vypis_vytvorenych_rozvrhu
# from typing import Union
from itertools import permutations


# rozvrh_type = list[list[list[list[Union[list[int], list[[]]]]]]]
rozvrh_type = list


def TvorRozvrhyProRuzneVlivy(seznam_poradi_predmetu: list[list[int]], seznam_vlivu: list[list[int]], pocet_potrebnych_prednasek_dle_oboru: list[list[int]],
                             pocet_potrebnych_prednasek_dle_vyucujiciho: list[list[int]], vyucujici_casy: list[list[list[int]]], obory_casy: list[list[list[int]]], mistnosti_casy: list[list[list[int]]],
                             seznam_delkaPredmetu_predmet: list[int], preference_mistnosti: list[list[int]], seznam_predmetu: list[str], sablona_rozvrhu: rozvrh_type,
                             seznam_hodnoceni: list[list[float]], seznam_oboru: list[str], seznam_mistnosti: list[str], seznam_vyucujicich: list[str], data_o_jiz_zapsanych_p: list[list[str]], pocet_prepsani: int):
    """
    Hlavní funkce pro tvorbu rozvrhů procházením posloupností předmětů.
    :param seznam_poradi_predmetu: seznam seznamů pořadí předmětů
    :param seznam_vlivu: seznam "vektorů"
    :param pocet_potrebnych_prednasek_dle_oboru: pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný
    :param pocet_potrebnych_prednasek_dle_vyucujiciho: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param vyucujici_casy: data volných hodin vyučujících
    :param obory_casy: data volných hodin oborů
    :param mistnosti_casy: data volných hodin místností
    :param seznam_delkaPredmetu_predmet: seznam délek předmětů (index = předmět, hodnota = délka)
    :param preference_mistnosti: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param seznam_predmetu: seznam předmětů
    :param sablona_rozvrhu: rozvrh s natvrdo zapsanými předměty
    :param seznam_hodnoceni: seznam seznamů hodnocení každého předmětu (index podseznamu = seznam s pořadovými čísly předmětů)
    :param seznam_oboru: seznam oborů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :param data_o_jiz_zapsanych_p: data natvrdo zapsaných předmětů
    :return: vytvorene_rozvrhy: rozvrhy s plným počtem zapsaných předmětů
             seznam_vlivu_vytvorenych_rozvrhu: vektory vlivů vytvořených rozvrhů
             seznam_vliv_predmety_hodnoty_nezapsane: seznam se seznamy, které obsahují vektor vlivů, předměty v zapisovaném pořadí, hodnocení předmětů, nezapsané předměty
    """
    vytvorene_rozvrhy = []
    seznam_vlivu_vytvorenych_rozvrhu = []
    seznam_vliv_predmety_hodnoty_nezapsane = []
    poradi_predmetu = []
    vlivy = []
    hodnoceni = []
    posloupnosti_navic = []
    nove_vlivy = []
    nove_hodnoceni = []
    permutace_byly_pridany = False
    tvorba_upravou_posloupnosti = False
    pocet_nezapsanych_predmetu = 0
    for poradi in range(len(seznam_poradi_predmetu)):
        pom_sablona_rozvrhu = copy.deepcopy(sablona_rozvrhu)
        pom_pocet_potrebnych_prednasek_dle_oboru = copy.deepcopy(pocet_potrebnych_prednasek_dle_oboru)
        pom_pocet_potrebnych_prednasek_dle_vyucujiciho = copy.deepcopy(pocet_potrebnych_prednasek_dle_vyucujiciho)
        pom_obory_casy = copy.deepcopy(obory_casy)
        pom_vyucujici_casy = copy.deepcopy(vyucujici_casy)
        pom_mistnosti_casy = copy.deepcopy(mistnosti_casy)

        for i in range(pocet_prepsani + 1):
            rozvrh, pppdo, pppdv, obs_vyuc, obs_oboru, obs_mist = Vytvor_Rozvrh_dlePredmetu(seznam_poradi_predmetu[poradi],
                                                                                            pom_pocet_potrebnych_prednasek_dle_oboru,
                                                                                            pom_pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                                                            pom_vyucujici_casy,
                                                                                            pom_obory_casy,
                                                                                            pom_mistnosti_casy,
                                                                                            seznam_delkaPredmetu_predmet,
                                                                                            preference_mistnosti,
                                                                                            pom_sablona_rozvrhu,
                                                                                            seznam_oboru,
                                                                                            seznam_predmetu,
                                                                                            seznam_mistnosti,
                                                                                            seznam_vyucujicich)

            # vypis_vytvorenych_rozvrhu.Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich)
            nezapsane_predmety, seznam_pom_dat = hodnoceni_vytvoreneho_rozvrhu.Ohodnot_Rozvrh(vytvorene_rozvrhy,
                                                rozvrh,
                                                pppdo,
                                                seznam_predmetu,
                                                seznam_vlivu[poradi],
                                                seznam_vlivu_vytvorenych_rozvrhu,
                                                seznam_vliv_predmety_hodnoty_nezapsane,
                                                seznam_poradi_predmetu[poradi],
                                                seznam_hodnoceni[poradi])

            if nezapsane_predmety:
                nezapsane_predmety = pomocne_funkce.Odstran_OpakPrvkySeznamu(nezapsane_predmety)

            if not tvorba_upravou_posloupnosti:
                poradi_predmetu = seznam_poradi_predmetu[poradi]
                vlivy = seznam_vlivu[poradi]
                hodnoceni = seznam_hodnoceni[poradi]
                tvorba_upravou_posloupnosti = True
                pocet_nezapsanych_predmetu = len(nezapsane_predmety)
                # print(f"Pořadí předmětů s 1 nezapsanou přednáškou: {poradi_predmetu}")
            if pocet_nezapsanych_predmetu < len(nezapsane_predmety):
                poradi_predmetu = seznam_poradi_predmetu[poradi]
                vlivy = seznam_vlivu[poradi]
                hodnoceni = seznam_hodnoceni[poradi]
            if len(nezapsane_predmety) == 1 and nezapsane_predmety[0][1] == 1:
                # vypis_vytvorenych_rozvrhu.Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich)
                data_k_presunuti = Zjisti_MohouLiSePremistitPredmety(rozvrh,
                                                                     obs_vyuc,
                                                                     obs_oboru,
                                                                     obs_mist,
                                                                     nezapsane_predmety,
                                                                     pppdv,
                                                                     seznam_delkaPredmetu_predmet,
                                                                     pppdo,
                                                                     preference_mistnosti,
                                                                     vyucujici_casy,
                                                                     seznam_predmetu,
                                                                     seznam_vyucujicich,
                                                                     seznam_mistnosti,
                                                                     data_o_jiz_zapsanych_p)
                if not data_k_presunuti:
                    break
                pom_sablona_rozvrhu = Proved_PridejDoSablonyRozvrhu(pom_sablona_rozvrhu,
                                                                    data_k_presunuti,
                                                                    pom_vyucujici_casy,
                                                                    pom_mistnosti_casy,
                                                                    pom_obory_casy,
                                                                    pom_pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                                    pom_pocet_potrebnych_prednasek_dle_oboru,
                                                                    seznam_vyucujicich)
    return vytvorene_rozvrhy, seznam_vlivu_vytvorenych_rozvrhu, seznam_vliv_predmety_hodnoty_nezapsane, poradi_predmetu, vlivy, hodnoceni


def Tvor_RozvrhyUpravouPosloupnosti(posl_predmetu, vlivy_posl, pocet_potrebnych_prednasek_dle_oboru: list[list[int]],
                                    pocet_potrebnych_prednasek_dle_vyucujiciho: list[list[int]], vyucujici_casy: list[list[list[int]]], obory_casy: list[list[list[int]]], mistnosti_casy: list[list[list[int]]],
                                    seznam_delkaPredmetu_predmet: list[int], preference_mistnosti: list[list[int]], seznam_predmetu: list[str], sablona_rozvrhu: rozvrh_type,
                                    hodnoceni_posl, seznam_oboru: list[str], seznam_mistnosti: list[str], seznam_vyucujicich: list[str]):
    """
    Přesouvá předměty dopředu v posloupnosti předmětů, pokud se nezapíší. Pokud takováto posloupnost už byla
    testována (např. se předmět opět nezapsal), tak se předmět posouvá dopředu o 2 pozice, atd. Tento proces se opakuje,
    dokud:
        se všechny předměty nezapíší
        posloupnost už byla testována a předmět už nejde dále posunout
    :param posl_predmetu: seznam seřezených předmětů podle důležitosti
    :param vlivy_posl: vlivy použité na vytvoření dané posloupnosti
    :param pocet_potrebnych_prednasek_dle_oboru: data předmětů oborů
    :param pocet_potrebnych_prednasek_dle_vyucujiciho: data přednášek vyučujících
    :param vyucujici_casy: data volných hodin vyučujících
    :param obory_casy: data volných hodin oborů
    :param mistnosti_casy: data volných hodin místností
    :param seznam_delkaPredmetu_predmet: seznam délek předmětů
    :param preference_mistnosti:  v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param seznam_predmetu: seznam předmětů
    :param sablona_rozvrhu: šablona rozvrhu
    :param hodnoceni_posl: seznam hodnocení předmětů posloupnosti
    :param seznam_oboru: seznam oborů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :return: vytvořené rozvrhy
    """
    vytvorene_rozvrhy = []
    pouzite_posl = []
    while len(vytvorene_rozvrhy) != 1:
        pom_sablona_rozvrhu = copy.deepcopy(sablona_rozvrhu)
        pom_pocet_potrebnych_prednasek_dle_oboru = copy.deepcopy(pocet_potrebnych_prednasek_dle_oboru)
        pom_pocet_potrebnych_prednasek_dle_vyucujiciho = copy.deepcopy(pocet_potrebnych_prednasek_dle_vyucujiciho)
        pom_obory_casy = copy.deepcopy(obory_casy)
        pom_vyucujici_casy = copy.deepcopy(vyucujici_casy)
        pom_mistnosti_casy = copy.deepcopy(mistnosti_casy)
        rozvrh, pppdo, pppdv, obs_vyuc, obs_oboru, obs_mist = Vytvor_Rozvrh_dlePredmetu(posl_predmetu,
                                                                                        pom_pocet_potrebnych_prednasek_dle_oboru,
                                                                                        pom_pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                                                        pom_vyucujici_casy,
                                                                                        pom_obory_casy,
                                                                                        pom_mistnosti_casy,
                                                                                        seznam_delkaPredmetu_predmet,
                                                                                        preference_mistnosti,
                                                                                        pom_sablona_rozvrhu,
                                                                                        seznam_oboru,
                                                                                        seznam_predmetu,
                                                                                        seznam_mistnosti,
                                                                                        seznam_vyucujicich)

        # vypis_vytvorenych_rozvrhu.Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich)
        nezapsane_predmety, seznam_pom_dat = hodnoceni_vytvoreneho_rozvrhu.Ohodnot_Rozvrh(vytvorene_rozvrhy,
                                                                                          rozvrh,
                                                                                          pppdo,
                                                                                          seznam_predmetu,
                                                                                          vlivy_posl,
                                                                                          [],
                                                                                          [],
                                                                                          posl_predmetu,
                                                                                          hodnoceni_posl)
        if nezapsane_predmety:
            nezapsane_predmety = pomocne_funkce.Odstran_OpakPrvkySeznamu(nezapsane_predmety)
        if len(nezapsane_predmety) == 0:
            vytvorene_rozvrhy.append(rozvrh)
            break
        pouzite_posl.append(posl_predmetu)
        posl_predmetu = Uprav_Posloupnost(posl_predmetu, nezapsane_predmety[0][0], pouzite_posl, len(seznam_predmetu))
        if not posl_predmetu:
            break
    return vytvorene_rozvrhy


def Uprav_Posloupnost(posloupnost: list[int], nezap_predmet: int, pouzite_posl: list[list[int]], pocet_predmetu: int) -> list[int]:
    """
    Nezapsaný předmět se prohodí s tím co je na indexu i-1.
    Pokud tato posloupnost již byla použitá, tak se předmět prohodí s předmětem co je na indexu i-2 pokud to jde
    :param posloupnost: posloupnost předmětů
    :param nezap_predmet: index nezapsaného předmětu
    :param pouzite_posl: seznam použitých posloupností
    :param pocet_predmetu: počet předmětů
    :return: upravená posloupnost předmětů
    """
    index_nezapsaneho = posloupnost.index(nezap_predmet)
    for i in range(1, pocet_predmetu):
        if index_nezapsaneho - i >= 0:
            nova_posl = copy.deepcopy(posloupnost)
            nova_posl.insert(index_nezapsaneho - i, nova_posl[index_nezapsaneho])
            nova_posl.pop(index_nezapsaneho + 1)
            if pouzite_posl:
                if nova_posl not in pouzite_posl:
                    return nova_posl
    return []


"""
def Vytvor_Permutace(poradi_predmetu, vlivy, hodnoceni):
    seznam_vlivu = []
    seznam_hodnoceni = []
    zacatek = poradi_predmetu[:10]
    zbytek = poradi_predmetu[10:]
    vsechny_permutace = list(permutations(zacatek))
    posloupnosti = [list(perm) + zbytek for perm in vsechny_permutace]
    pocet_posloupnosti = len(posloupnosti)
    for i in range(pocet_posloupnosti):
        seznam_vlivu.append(vlivy)
        seznam_hodnoceni.append(hodnoceni)
    return posloupnosti, seznam_vlivu, seznam_hodnoceni
"""


def Proved_PridejDoSablonyRozvrhu(rozvrh: rozvrh_type, data_k_presunuti: list[int], obs_vyuc: list[list[list[int]]], obs_mist: list[list[list[int]]], obs_oboru: list[list[list[int]]], pppdv: list[list[int]], pppdo: list[list[int]], seznam_vyuc: list[str]) -> rozvrh_type:
    """
    Přidává předmět do šablony rozvrhu.
    :param rozvrh: sablona rozvrhu
    :param data_k_presunuti: [index_předmětu: int, index_vyučujícího: int, index_místnosti:int , den_od_1: int, cas_od_1: int, délka_přednášky: int]
    :return: šablona s přidaným předmětem
    """
    obory_predmetu = pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, data_k_presunuti[0])
    Obsad(obs_vyuc, [data_k_presunuti[3], data_k_presunuti[4]], data_k_presunuti[5], [data_k_presunuti[1]])
    Obsad(obs_oboru, [data_k_presunuti[3], data_k_presunuti[4]], data_k_presunuti[5], obory_predmetu)
    Obsad(obs_mist, [data_k_presunuti[3], data_k_presunuti[4]], data_k_presunuti[5], [data_k_presunuti[2]])
    Odecti_Pocet_Prednasek(pppdv, [data_k_presunuti[1]], data_k_presunuti[0])
    Odecti_Pocet_Prednasek(pppdo, obory_predmetu, data_k_presunuti[0])
    Zapis_Do_Rozvrhu(obory_predmetu, [data_k_presunuti[3], data_k_presunuti[4]], data_k_presunuti[5], data_k_presunuti[1], data_k_presunuti[2], rozvrh, data_k_presunuti[0])
    return rozvrh


def Vytvor_Rozvrh_dlePredmetu(posloupnost_predmetu: list[int], pom_pppdo: list[list[int]], pom_pppdv: list[list[int]], pom_obs_vyuc: list[list[list[int]]], pom_obs_oboru: list[list[list[int]]],
                              pom_obs_mist: list[list[list[int]]], delky_prednasek: list[int], prefer_mist: list[list[int]], sablona_rozvrhu: rozvrh_type, seznam_oboru: list[str],
                              seznam_predmetu: list[str], seznam_mistnosti: list[str], seznam_vyucujicich: list[str]) -> [list[rozvrh_type], list[list[int]], list[list[int]], list[list[list[int]]], list[list[list[int]]], list[list[list[int]]]]:
    """
    Tvoří rozvrhy pomocí posloupnosti předmětů.
    :param posloupnost_predmetu: seznam pořadí předmětů (předměty jsou v pořadí dle seznamu předmětů, hodnoty jsou pořadí zápisu)
    :param pom_pppdo: pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný
    :param pom_pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param pom_obs_vyuc: data volných hodin vyučujících
    :param pom_obs_oboru: data volných hodin oborů
    :param pom_obs_mist: data volných hodin místností
    :param delky_prednasek: seznam délek přednášek (index = předmět, hodnota = délka)
    :param prefer_mist: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param sablona_rozvrhu: rozvrh s napevno zapsanými předměty
    :param seznam_oboru: seznam oborů
    :param seznam_predmetu: seznam předmětů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :return: rozvrh: rozvrh s nějakým počtem zapsaných předmětů
             pppdo: parametr ovlivněný zápisem předmětů
             pppdv: parametr ovlivněný zápisem předmětů
             obs_vyuc: parametr ovlivněný zápisem předmětů
             obs_oboru: parametr ovlivněný zápisem předmětů
             obs_mist: parametr ovlivněný zápisem předmětů
    """
    obs_oboru = copy.deepcopy(pom_obs_oboru)
    obs_vyuc = copy.deepcopy(pom_obs_vyuc)
    obs_mist = copy.deepcopy(pom_obs_mist)
    pppdv = copy.deepcopy(pom_pppdv)
    pppdo = copy.deepcopy(pom_pppdo)
    rozvrh = copy.deepcopy(sablona_rozvrhu)
    # print("sablona: ")
    # Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich)

    for predmet in posloupnost_predmetu:
        vyucujici_predmetu = pomocne_funkce.Najdi_Vyucujici_Predmetu(pppdv, predmet)
        for vyuc in vyucujici_predmetu:
            # if pppdv[vyuc][predmet] > 0:  # vyuc jeste ma tento predmet oducit
            delka_prednasky = delky_prednasek[predmet]
            jiz_vybrane = []
            while pppdv[vyuc][predmet] != 0:
                casy_den_h = pomocne_funkce.Najdi_Cas_Vyucujiciho(obs_vyuc, vyuc, delka_prednasky, jiz_vybrane)
                if not casy_den_h:
                    break
                #if pomocne_funkce.Zjisti_Ma_Vyucujici_Volno(obs_vyuc, vyuc, casy_den_h[0], casy_den_h[1], delka_prednasky):
                den_odH = [casy_den_h[0], casy_den_h[1]]
                obory_predmetu = pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, predmet)
                if Zjisti_Maji_Obory_Volno(obs_oboru, obory_predmetu, den_odH, delka_prednasky):
                    mistnosti_predmetu = pomocne_funkce.Najdi_Mistnosti_Predmetu(prefer_mist, predmet)
                    for mistnost in mistnosti_predmetu:
                        if pomocne_funkce.Zjisti_Je_Mistnost_Volna(obs_mist, mistnost, den_odH, delka_prednasky):
                            Obsad(obs_vyuc, den_odH, delka_prednasky, [vyuc])
                            Obsad(obs_oboru, den_odH, delka_prednasky, obory_predmetu)
                            Obsad(obs_mist, den_odH, delka_prednasky, [mistnost])
                            Odecti_Pocet_Prednasek(pppdv, [vyuc], predmet)
                            Odecti_Pocet_Prednasek(pppdo, obory_predmetu, predmet)
                            Zapis_Do_Rozvrhu(obory_predmetu,
                                             den_odH,
                                             delka_prednasky,
                                             vyuc,
                                             mistnost,
                                             rozvrh,
                                             predmet)
                            break
    # print(f"rozvrh: {rozvrh}")
    # print("vystup: ")
    # Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich)
    return rozvrh, pppdo, pppdv, obs_vyuc, obs_oboru, obs_mist


def Zjisti_MohouLiSePremistitPredmety(rozvrh: rozvrh_type, obs_vyuc: list[list[list[int]]], obs_oboru: list[list[list[int]]], obs_mist: list[list[list[int]]], nezapsane_predmety: list[list[int]], pppdv: list[list[int]], delky_predmetu: list[int],
                                      pppdo: list[list[int]], prefer_mist: list[list[int]], vyucujici_casy: list[list[list[int]]], seznam_predmetu: list[str], seznam_vyucujicich: list[str],
                                      seznam_mistnosti: list[str], data_o_jiz_zapsanych_p: list[list[str]]) -> list[int]:
    """
    Zjišťuje, zda existuje způsob přepsat zapsaný předmět na jiné místo, kdy po nevytvoření rozvrhu zbylo místo.
    Beru předmět, co se nezapsal, a zjišťuji, zda ten předmět, co ho vyblokoval, mohl být zapsán jinam.
    :param rozvrh: rozvrh
    :param obs_vyuc: ovlivněná data volných hodin vyučujících
    :param obs_oboru: ovlivněná data volných hodin oborů
    :param obs_mist: ovlivněná data volných hodin místností
    :param nezapsane_predmety: seznam nezapsaných předmětů
    :param pppdv: data přednášek vyučujících
    :param delky_predmetu: seznam délek předmětů
    :param pppdo: data předmětů oborů
    :param prefer_mist: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param vyucujici_casy: neovlivněná data volných hodin vyučujících
    :param seznam_predmetu: seznam předmětů
    :param seznam_vyucujicich: seznam vyučujících
    :param seznam_mistnosti: seznam místností
    :param data_o_jiz_zapsanych_p: data natvrdo zapsaných předmětů
    :return: data předmětu, co se zapíše do šablony rozvrhů
    """
    data_k_presunuti = []
    nezap_predmet = nezapsane_predmety[0][0]
    delka_nezap_predmetu = delky_predmetu[nezap_predmet]
    vyuc_nezap_predmetu = pomocne_funkce.Najdi_Vyucujici_Predmetu(pppdv, nezap_predmet)

    # dvojice vyučující-předmět co blokují nezapsaný předmět
    blok_vyuc_predmet_s_dupl = Najdi_VyucBlokujiciNezapPredmet(rozvrh, vyucujici_casy, vyuc_nezap_predmetu, obs_oboru)
    blok_vyuc_predmet = pomocne_funkce.Odstran_OpakPrvkySeznamu(blok_vyuc_predmet_s_dupl)

    for p in range(len(blok_vyuc_predmet)):
        predmet = blok_vyuc_predmet[p][1]
        vyuc = blok_vyuc_predmet[p][0]
        # ma někdo, z těch co blokují, možnost se napsat jinam?
        jiz_vybrane = []
        delka_prednasky = delky_predmetu[predmet]
        casy_den_h = pomocne_funkce.Najdi_Cas_Vyucujiciho(obs_vyuc, vyuc, delka_prednasky, jiz_vybrane)
        if delka_nezap_predmetu <= delka_prednasky:
            if casy_den_h:
                if not pomocne_funkce.Zjisti_ZdaPredmetJeNapevno(data_o_jiz_zapsanych_p, seznam_predmetu, predmet):
                    if pomocne_funkce.Zjisti_Ma_Vyucujici_Volno(obs_vyuc, vyuc, casy_den_h[0], casy_den_h[1], delka_prednasky):
                        den_odH = [casy_den_h[0], casy_den_h[1]]
                        obory_predmetu = pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, predmet)
                        if pomocne_funkce.Zjisti_JeVolnoVRozvrhu(rozvrh, casy_den_h[0], casy_den_h[1], delka_prednasky, obory_predmetu):
                            if Zjisti_Maji_Obory_Volno(obs_oboru, obory_predmetu, den_odH, delka_prednasky):
                                mistnosti_predmetu = pomocne_funkce.Najdi_Mistnosti_Predmetu(prefer_mist, predmet)
                                for mistnost in mistnosti_predmetu:
                                    if pomocne_funkce.Zjisti_Je_Mistnost_Volna(obs_mist, mistnost, den_odH, delka_prednasky):
                                        data_k_presunuti = [predmet,
                                                            vyuc,
                                                            mistnost,
                                                            casy_den_h[0],
                                                            casy_den_h[1],
                                                            delka_prednasky]
                                        break
    return data_k_presunuti


def Obsad(casy: list[list[list[int]]], den_odH: [int, int], delka_prednasky: int, kdo_se_ma_obsadit: list[int]) -> None:
    """
    Mění volné hodiny na obsazené.
    :param casy: data volen vyučujících/místností/oborů
    :param den_odH: [den, hodina]. (0 hodina - od 8h do 9h, 1 hodina - od 9h do 10h)
    :param delka_prednasky: délka přednášky
    :param kdo_se_ma_obsadit: seznam indexů vyučujících/místností/oborů
    :return: None
    """
    for hodina in range(delka_prednasky):
        # for co in range(len(radek)):
        for co in kdo_se_ma_obsadit:  # pro případ obsazení oborů -> obsadí se více oborů
            casy[co][den_odH[0]][den_odH[1] + hodina] = 0


def Zapis_Do_Rozvrhu(seznam_oboru: list[int], den_odH: [int, int], delka_prednasky: int, vyuc: int, mistnost: int, rozvrh: rozvrh_type, predmet: int) -> None:
    """
    Přidává určitým oborům do určitých časových slotů v rozvrhu seznam obsahující vyučujícího, předmět, místnost.
    :param seznam_oboru: seznam indexů oborů
    :param den_odH: [den, hodina], hodina = číslo slotu (0 hodina = od 8h do 9h)
    :param delka_prednasky: délka přednášky
    :param vyuc: index vyučujícího
    :param mistnost: index  místnosti
    :param rozvrh: rozvrh kam se to mají zapsat data
    :param predmet: index předmětu
    :return: None
    """
    for obor in seznam_oboru:
        for hodina in range(delka_prednasky):
            rozvrh[obor][den_odH[0]][den_odH[1] + hodina] = [vyuc, predmet, mistnost]


def Odecti_Pocet_Prednasek(pppd_: list[list[int]], seznam_oboru_nebo_vuyc: list[int], predmet: int) -> None:
    """
    Odečítá počet přednášek oborům nebo vyučujícímu
    :param pppd_: (pocet_potrebnych_prednasek_dle_oboru/pocet_potrebnych_prednasek_dle_vyucujiciho)
    :param seznam_oboru_nebo_vuyc: seznam indexů oborů/vyučujících
    :param predmet: index předmětu
    :return: None
    """
    for prvek in seznam_oboru_nebo_vuyc:
        pppd_[prvek][predmet] -= 1


def Zjisti_Maji_Obory_Volno(obs_oboru: list[list[list[int]]], obory: list[int], den_odH: [int, int], delka_prenasky: int) -> bool:
    """
    Zjišťuje, zda mají obory volno po dobu délky přednášky.
    :param obs_oboru: data volen oborů (obsazenost)
    :param obory: seznam indexů obrů
    :param den_odH: [den, hodina] (0 hodina = od 8h do 9h)
    :param delka_prenasky: délka přednášky
    :return: obory mají/nemají volno po dobu délky přednášky
    """
    for obor in obory:
        if den_odH[1] <= 12 - delka_prenasky:
            for hodina in range(delka_prenasky):
                if obs_oboru[obor][den_odH[0]][den_odH[1] + hodina] != 1:
                    return False
    return True


def Najdi_VyucBlokujiciNezapPredmet(rozvrh: rozvrh_type, vyucujici_casy: list[list[list[int]]], vyuc_nezap_predmetu: list[int], obs_oboru: list[list[list[int]]]) -> list[list[int]]:
    """
    Hledá vyučující, co blokovaly čas nezapsanému předmětu.
    :param rozvrh: rozvrh, kde se nějaký předmět nezapsal
    :param vyucujici_casy: data vole vyučujících (obsazenost)
    :param vyuc_nezap_predmetu: seznam vyučujících předmětu, který se nezapsal
    :param obs_oboru: data volen oborů (obsazenost)
    :return: seznam dvojic vyučující-předmět co blokovaly časy (všechny) vyučujících blokovaného předmětu
    """
    blokujici_vyuc_predmet = []
    for vyuc in range(len(vyuc_nezap_predmetu)):  # vyučující, kterému blokovali předmět
        for den in range(5):
            for cas in range(12):
                if vyucujici_casy[vyuc_nezap_predmetu[vyuc]][den][cas] == 1:
                    for obor in range(len(obs_oboru)):
                        if rozvrh[obor][den][cas]:
                            blokujici_vyuc_predmet.append([rozvrh[obor][den][cas][0], rozvrh[obor][den][cas][1]])
    return blokujici_vyuc_predmet


def Vytvor_SablonuRozvrhu(pocet_oboru: int, pppdo: list[list[int]], pppdv: list[list[int]], obs_oboru: list[list[list[int]]], obs_vyuc: list[list[list[int]]], obs_mist: list[list[list[int]]], seznam_predmetu: list[str], seznam_vyuc: list[str],
                          seznam_mistnosti: list[str], data_o_jiz_zapsanych_p: list[list[str]], seznam_oboru: list[str]) -> rozvrh_type:
    """
    Vytváří šablonu rozvrhů.
    :param pocet_oboru: počet oborů
    :param pppdo: pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param obs_oboru: data volen oborů (obsazenost oborů)
    :param obs_vyuc: data volen vyučujících (obsazenost vyučujících)
    :param obs_mist: data volen místností (obsazenost místností)
    :param seznam_predmetu: seznam předmětů
    :param seznam_vyuc: seznam vyučujících
    :param seznam_mistnosti: seznam místností
    :param data_o_jiz_zapsanych_p: seznam s daty napevno zapsaných předmětů
    :param seznam_oboru: seznam
    :return: šablona rozvrhu
    """
    # bez deepcopy aby se to propsalo pro vsechny data
    rozvrh = tvorba_seznamu_z_nactenych_dat.Vytvor_Prazdny_Rozvrh(pocet_oboru)
    # obory se musi najit v seznamu, dny on 1, casy od 1

    # zapis do rozvrhu
    pom = []
    if data_o_jiz_zapsanych_p:
        for data in range(len(data_o_jiz_zapsanych_p)):
            predmet = pomocne_funkce.Zjisti_CisloPomociKodu(seznam_predmetu, data_o_jiz_zapsanych_p[data][0])
            obory_predmetu = pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, predmet)
            den_odH = int(data_o_jiz_zapsanych_p[data][3]) - 1, int(data_o_jiz_zapsanych_p[data][4]) - 1
            vyuc = pomocne_funkce.Zjisti_CisloPomociKodu(seznam_vyuc, data_o_jiz_zapsanych_p[data][1])
            delka_prednasky = int(data_o_jiz_zapsanych_p[data][5])
            mistnost = pomocne_funkce.Zjisti_CisloPomociKodu(seznam_mistnosti, data_o_jiz_zapsanych_p[data][2])

            Obsad(obs_vyuc, den_odH, delka_prednasky, [vyuc])
            Obsad(obs_oboru, den_odH, delka_prednasky, obory_predmetu)
            Obsad(obs_mist, den_odH, delka_prednasky, [mistnost])
            Odecti_Pocet_Prednasek(pppdv, [vyuc], predmet)
            Odecti_Pocet_Prednasek(pppdo, obory_predmetu, predmet)
            Zapis_Do_Rozvrhu(obory_predmetu, den_odH, delka_prednasky, vyuc, mistnost, rozvrh, predmet)
            pom.append([predmet, obory_predmetu, den_odH, vyuc, delka_prednasky, mistnost])
        # Vypis_Rozvrh([rozvrh], seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyuc)
        # print(pom)
    return rozvrh


