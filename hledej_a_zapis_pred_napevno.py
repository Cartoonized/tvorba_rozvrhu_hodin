import pomocne_funkce


def Zjisti_KdyZacinaUcit(vyuc: int, vyucujici_casy: list[list[int]]) -> [int, int]:
    """
    funkce vrací číslo dne (0-4) a číslo hodiny (0-11)
    :param vyuc: index vyučujícího
    :param vyucujici_casy: data volných hodin vyučujících
    :return: index dne od 0, index hodiny od 0
    """
    den_kdy_zacina_ucit = 0
    cas_kdy_zacina_ucit = 0
    nalezeno = False
    while not nalezeno:
        for den in range(5):
            for cas in range(12):
                if vyucujici_casy[vyuc][den][cas] == 1:
                    den_kdy_zacina_ucit = den
                    cas_kdy_zacina_ucit = cas
                    nalezeno = True
                    break
    return den_kdy_zacina_ucit, cas_kdy_zacina_ucit


def Zjisti_PocetPrednasekVyuc(pppdv, vyuc) -> int:
    """
    vrací celkový počet přednášek, co má tento vyučující odučit
    :param pppdv: data přednášek vyučujících
    :param vyuc: index vyučujícího
    :return: počet přednášek
    """
    pocet_prednasek = 0
    for predmet in range(len(pppdv[0])):
        if pppdv[vyuc][predmet] != 0:
            pocet_prednasek += pppdv[vyuc][predmet]
    return pocet_prednasek


def Proved_ZapisPredmetuNapevno(data_o_jiz_zapsanych_p, vyucujici_casy, pppdv, seznam_delkaPredmetu_predmet,
                                seznam_vyuc, pppdo, pref_mistnosti, seznam_predmetu, seznam_vyucujicich,
                                seznam_mistnosti, mistnosti_casy):
    """
    Přidává data o předmětu do seznamu obsahující předměty, co se mají zapsat do šablony, pokud je jasné z dat, že je napevno.
    :param data_o_jiz_zapsanych_p: data natvrdo zapsaných předmětů
    :param vyucujici_casy: data volných hodin vyučujících
    :param pppdv: data přednášek vyučujících
    :param seznam_delkaPredmetu_predmet: seznam délek předmětů (index = předmět, hodnota = délka)
    :param seznam_vyuc: seznam vyučujících
    :param pppdo: data předmětů oborů
    :param pref_mistnosti: v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    :param seznam_predmetu: seznam předmětů
    :param seznam_vyucujicich: seznam vyučujících
    :param seznam_mistnosti: seznam místností
    :param mistnosti_casy: data volných hodin místností
    :return: None
    """
    jiz_pouzite_casy = []
    for vyuc in range(len(seznam_vyuc)):
        pocet_jednicek = pomocne_funkce.Zjisti_PocetJednicekVyuc(vyuc, vyucujici_casy)
        seznam_predmety_pp_delky = pomocne_funkce.Najdi_PredmetyVyucujiciho(pppdv, vyuc,
                                                                            seznam_delkaPredmetu_predmet,
                                                                            seznam_vyuc)
        # [[predmet1, pocet_prednasek, delka_predenasky], [predmet2, pocet_prednasek, delka_predenasky], ...]
        pocet_hodin_k_oduceni = 0
        if seznam_predmety_pp_delky:
            for p in range(len(seznam_predmety_pp_delky)):
                pocet_hodin_k_oduceni += seznam_predmety_pp_delky[p][1] * seznam_predmety_pp_delky[p][2]
        uci_1ci2_predmety_pro_jeden_obor = Zjisti_Uci1ci2PredmetyPro1obor(seznam_predmety_pp_delky, pppdo)
        if pocet_jednicek == pocet_hodin_k_oduceni:
            if uci_1ci2_predmety_pro_jeden_obor:
                for p in range(len(seznam_predmety_pp_delky)):
                    predmet = seznam_predmety_pp_delky[p][0]
                    vyucujici = vyuc
                    mistnost = pomocne_funkce.Najdi_Mistnosti_Predmetu(pref_mistnosti, seznam_predmety_pp_delky[p][0])
                    den, casOd = Zjisti_KdyZacinaUcit(vyuc, vyucujici_casy)
                    if [den, casOd] not in jiz_pouzite_casy:
                        jiz_pouzite_casy.append([den, casOd])
                        # zacina ucit ve stejnou dobu -> zohlednovat predtim zapsane predmety protoze tady neblokuju
                        # casy, treba si vytvorit pomocne casy vyuc, mistnosti, oboru
                        # (pokud uci 2 predmety -> prekryji se)
                        delka_prednasky = seznam_delkaPredmetu_predmet[predmet]

                        data_o_jiz_zapsanych_p.append([seznam_predmetu[predmet],
                                                       seznam_vyucujicich[vyucujici],
                                                       seznam_mistnosti[mistnost[0]],
                                                       den + 1,
                                                       casOd + 1,
                                                       delka_prednasky])


def Zjisti_Uci1ci2PredmetyPro1obor(seznam_predmety_pp_delky, pppdo) -> bool:
    """
    Zjišťuje, zda vyučující učí 1 nebo 2 předměty pro jeden obor
    :param seznam_predmety_pp_delky: seznam obsahující délku přdnášky a jejich počet ke každému předmětu
    :param pppdo: data předmětů oborů
    :return: bool
    """
    if len(seznam_predmety_pp_delky) <= 2:
        obory_predmetu = pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, seznam_predmety_pp_delky[0][0])
        for predmet in range(len(seznam_predmety_pp_delky)):
            if pomocne_funkce.Zjisti_Obory_Predmetu(pppdo, seznam_predmety_pp_delky[predmet][0]) != obory_predmetu:
                return False
            if len(seznam_predmety_pp_delky) == 2 and seznam_predmety_pp_delky[predmet][1] != 1:
                return False
        return True
    else:
        return False
