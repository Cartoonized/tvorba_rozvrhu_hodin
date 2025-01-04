import os
import sys
import pomocne_funkce


def Kontrola_Vst_Dat(seznam_predmetu: list[str], seznam_predmet_delkaPredmetu: list[list[str]], seznam_predmet_mistnost_poradi: list[list[str]],
                     seznam_vyucujici_predmet_pocetPrednasek: list[list[str]], data_o_jiz_zapsanych_p: list[list[str]], delky_predmetu: list[int],
                     seznam_vyucujicich: list[str], seznam_mistnosti: list[str], vyucujici_casy: list[list[list[int]]], mistnosti_casy: list[list[list[int]]], pppdv: list[list[int]],
                     seznam_delkaPredmetu_predmet: list[int]) -> list[str]:
    """
    :param seznam_predmetu: seznam předmětů načtených z csv
    :param seznam_predmet_delkaPredmetu: seznam délek předmětů
    :param seznam_predmet_mistnost_poradi: seznam načtených dat z csv
    :param seznam_vyucujici_predmet_pocetPrednasek: seznam načtených dat z csv
    :param data_o_jiz_zapsanych_p: seznam načtených dat z csv
    :param delky_predmetu: seznam délek předmětů
    :param seznam_vyucujicich: seznam kódů vyučujících
    :param seznam_mistnosti: seznam kódů místností
    :param vyucujici_casy: v řádcích jsou vyučující, ve sloupcích dny, 1 -> má volno, 0 -> nemá volno
    :param mistnosti_casy: v řádcích jsou mistnosti, ve sloupcích dny s hodinami, 1 -> je volno, 0 -> není volno
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param seznam_delkaPredmetu_predmet: index je predmet, hodnota je delka prednasky
    :return: seznam nalezených chyb
    """
    chyby = []
    Kontrola_PredmetDelkaPrednasky(chyby, seznam_predmetu, seznam_predmet_delkaPredmetu)
    Kontrola_PredmetMistnostPoradi(chyby, seznam_predmetu, seznam_predmet_mistnost_poradi)
    Kontrola_VyucujiciPredmetPocetPrednasek(chyby, seznam_predmetu, seznam_vyucujici_predmet_pocetPrednasek)
    Kontrola_CasuVyucujicich(chyby, vyucujici_casy, pppdv,
                             seznam_delkaPredmetu_predmet, seznam_vyucujicich)
    if data_o_jiz_zapsanych_p:
        Kontrola_PredmetuNapevnoZapsanych(chyby,
                                          data_o_jiz_zapsanych_p,
                                          seznam_predmetu,
                                          seznam_vyucujicich,
                                          seznam_mistnosti,
                                          delky_predmetu,
                                          vyucujici_casy,
                                          mistnosti_casy)
    return chyby


def Kontrola_PredmetuNapevnoZapsanych(chyby: list[str], data_o_jiz_zapsanych_p: list[list[str]], seznam_predmetu: list[str], seznam_vyucujicich: list[str],
                                      seznam_mistnosti: list[str], delky_predmetu: list[int], vyucujici_casy: list[list[list[int]]], mistnosti_casy: list[list[list[int]]]) -> None:
    """
    Hledá chyby a ukládá do seznamu chyb.
    :param chyby: seznam chybových hlášek
    :param data_o_jiz_zapsanych_p: seznam načtených dat z csv
    :param seznam_predmetu: seznam předmětů
    :param seznam_vyucujicich: seznam vyučujících
    :param seznam_mistnosti: seznam místností
    :param delky_predmetu: seznam délek předmětů
    :param vyucujici_casy: data volných hodin vyučujících
    :param mistnosti_casy: data volných hodin místností
    :return: None
    """
    for radek in range(len(data_o_jiz_zapsanych_p)):
        je_spravne_predmet = Kontrola_JeSpravneKod(data_o_jiz_zapsanych_p[radek][0], seznam_predmetu)
        je_spravne_vyucujici = Kontrola_JeSpravneKod(data_o_jiz_zapsanych_p[radek][1], seznam_vyucujicich)
        je_spravne_mistnost = Kontrola_JeSpravneKod(data_o_jiz_zapsanych_p[radek][2], seznam_mistnosti)
        je_spravne_den = Kontrola_JsouSpravneHodnoty(int(data_o_jiz_zapsanych_p[radek][3]), 1, 5)
        je_spravne_casOd = Kontrola_JsouSpravneHodnoty(int(data_o_jiz_zapsanych_p[radek][4]), 1,
                                                       12-(int(data_o_jiz_zapsanych_p[radek][5])-1))
        je_spravne_delkaPrednasky = Kontrola_JsouSpravneHodnoty(int(data_o_jiz_zapsanych_p[radek][5]),
                                                                delky_predmetu[0],
                                                                delky_predmetu[-1])

        if not je_spravne_predmet:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně předmět.")
        if not je_spravne_vyucujici:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně vyučující")
        if not je_spravne_mistnost:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně místnost")
        if not je_spravne_den:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně den")
        if not je_spravne_casOd:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně cas_Od")
        if not je_spravne_delkaPrednasky:
            chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, je špatně délka přednášky")
        if je_spravne_vyucujici and je_spravne_den and je_spravne_casOd and je_spravne_delkaPrednasky:
            index = 0
            for v in range(len(seznam_vyucujicich)):
                if seznam_vyucujicich[v] == data_o_jiz_zapsanych_p[radek][1]:
                    index = v
                    break
            muze_vyucujici_ucit = pomocne_funkce.Zjisti_Ma_Vyucujici_Volno(vyucujici_casy,
                                                            index,
                                                            int(data_o_jiz_zapsanych_p[radek][3]) - 1,
                                                            int(data_o_jiz_zapsanych_p[radek][4]) - 1,
                                                            int(data_o_jiz_zapsanych_p[radek][5]))
            if not muze_vyucujici_ucit:
                chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, vyučující NEMÁ volno tento čas")
        if je_spravne_mistnost and je_spravne_den and je_spravne_casOd and je_spravne_delkaPrednasky:
            mistnost = 0
            for v in range(len(seznam_mistnosti)):
                if seznam_mistnosti[v] == data_o_jiz_zapsanych_p[radek][2]:
                    mistnost = v
                    break
            je_mistnost_volna = pomocne_funkce.Zjisti_Je_Mistnost_Volna(mistnosti_casy, mistnost, [int(data_o_jiz_zapsanych_p[radek][3])-1,
                                                            int(data_o_jiz_zapsanych_p[radek][4]) - 1],
                                                         int(data_o_jiz_zapsanych_p[radek][5]))
            if not je_mistnost_volna:
                chyby.append(f"[CHYBA] V souboru: predmety_napevno.csv, na řádku: {radek + 2}, místnost NENÍ volná tento čas.")


def Kontrola_JsouSpravneHodnoty(cislo: int, od: int, do: int) -> bool:
    """
    Kontroluje, zda čísla uvedená v predmety_napevno.csv jsou ve správném intervalu.
    :param cislo: číslo, které chci zkontrolovat, zda patří do svého intervalu
    :param od: první hodnota intervalu
    :param do: poslední hodnota intervalu (včetně)
    :return: patří/nepatří
    """
    if od <= cislo <= do:
        return True
    else:
        return False


def Kontrola_JeSpravneKod(kod: str, seznam: list[str]) -> bool:
    """
    Kontroluje, zda kód uvedený v predmety_napevno.csv místnosti/vyučujícího/oboru/předmětu lze najít v seznamu m/v/o/p.
    :param kod: kód místnosti/vyučujícího/oboru/předmětu
    :param seznam: seznam, ve kterém chci tento kód hledat
    :return: je v seznamu / není v seznamu
    """
    for hodnota in range(len(seznam)):
        if seznam[hodnota] == kod:
            return True
    return False


def Zjisti_JeZdePredmetNavic(seznam_predmetu: list[str], kontrolovany_seznam: list, predmet: int, index: int) -> bool:
    """
    Zjišťuje, zda je v seznamu předmět navíc.
    :param seznam_predmetu: seznam předmětů
    :param kontrolovany_seznam: seznam, ve kterém mám předmět hledat
    :param predmet: index předmětu v seznamu předmětů
    :param index:
    :return:
    """
    for radek in range(len(kontrolovany_seznam)):
        if kontrolovany_seznam[radek][index] == seznam_predmetu[predmet]:
            return True
    return False


def Zjisti_ZdaChybiPredmet(seznam_predmetu: list[str], kontrolovany_seznam: list, radek: int, index: int) -> bool:
    """
    Zjišťuje, zda v seznamu předmět chybí.
    :param seznam_predmetu: seznam předmětů
    :param kontrolovany_seznam: seznam, ve kterém mám předmět hledat
    :param radek: první index seznamu
    :param index: index hodnoty
    :return: chybí / nechybí
    """
    for predmet in range(len(seznam_predmetu)):
        if kontrolovany_seznam[radek][index] == seznam_predmetu[predmet]:
            return True
    return False


def Kontrola_PredmetDelkaPrednasky(chyby: list[str], seznam_predmetu: list[str], seznam_predmet_delkaPredmetu: list[list[str]]) -> None:
    """
    Kontroluje, zda v souboru predmet_delkaPredmetu.csv jsou přítomny všechny předměty.
    :param chyby: seznam s chybami
    :param seznam_predmetu: seznam předmětů
    :param seznam_predmet_delkaPredmetu: seznam načtených dat z csv
    :return: Noe
    """
    # když předmět chybí
    for predmet in range(len(seznam_predmetu)):
        if not Zjisti_JeZdePredmetNavic(seznam_predmetu, seznam_predmet_delkaPredmetu, predmet, 0):
            chyby.append(f"[CHYBA] V souboru: predmet_delkaPredmetu.csv, chybí předmět: {seznam_predmetu[predmet]}")
    # když je předmět navíc
    for radek in range(len(seznam_predmet_delkaPredmetu)):
        if not Zjisti_ZdaChybiPredmet(seznam_predmetu, seznam_predmet_delkaPredmetu, radek, 0):
            chyby.append(f"[CHYBA] V souboru: predmet_delkaPredmetu.csv, je navíc předmět: {seznam_predmet_delkaPredmetu[radek][0]}")


def Kontrola_PredmetMistnostPoradi(chyby: list[str], seznam_predmetu: list[str], seznam_predmet_mistnost_poradi: list[list[str]]) -> None:
    """
    Kontroluje, zda v souboru predmet_mistnost_poradi.csv jsou přítomny všechny předměty.
    :param chyby: seznam s chybami
    :param seznam_predmetu: seznam předmětů
    :param seznam_predmet_mistnost_poradi: seznam načtených dat z csv
    :return: None
    """
    # když předmět chybí
    for predmet in range(len(seznam_predmetu)):
        if not Zjisti_JeZdePredmetNavic(seznam_predmetu, seznam_predmet_mistnost_poradi, predmet, 0):
            chyby.append(f"[CHYBA] V souboru: predmet_mistnost_poradi.csv, chybí předmět: {seznam_predmetu[predmet]}")
    # když je předmět navíc
    for radek in range(len(seznam_predmet_mistnost_poradi)):
        if not Zjisti_ZdaChybiPredmet(seznam_predmetu, seznam_predmet_mistnost_poradi, radek, 0):
            chyby.append(f"[CHYBA] V souboru: predmet_mistnost_poradi.csv, je navíc předmět: {seznam_predmet_mistnost_poradi[radek][0]}")


def Kontrola_VyucujiciPredmetPocetPrednasek(chyby: list[str], seznam_predmetu: list[str], seznam_vyucujici_predmet_pocetPrednasek: list[list[str]]) -> None:
    """
    Kontroluje, zda v souboru vyucujici_predmet_pocetPrednasek.csv jsou přítomny všechny předměty.
    :param chyby: seznam s chybami
    :param seznam_predmetu: seznam předmětů
    :param seznam_vyucujici_predmet_pocetPrednasek: seznam načtených dat z csv
    :return: None
    """
    # když předmět chybí
    for predmet in range(len(seznam_predmetu)):
        if not Zjisti_JeZdePredmetNavic(seznam_predmetu, seznam_vyucujici_predmet_pocetPrednasek, predmet, 1):
            chyby.append(f"[CHYBA] V souboru: vyucujici_predmet_pocetPrednasek.csv, chybí předmět: {seznam_predmetu[predmet]}")
    # když je předmět navíc
    for radek in range(len(seznam_vyucujici_predmet_pocetPrednasek)):
        if not Zjisti_ZdaChybiPredmet(seznam_predmetu, seznam_vyucujici_predmet_pocetPrednasek, radek, 1):
            chyby.append(f"[CHYBA] V souboru: vyucujici_predmet_pocetPrednasek.csv, je navíc předmět: {seznam_vyucujici_predmet_pocetPrednasek[radek][1]}")


def Kontrola_CasuVyucujicich(chyby: list[str], vyucujici_casy: list[list[list[int]]], pppdv: list[list[int]], seznam_delkaPredmetu_predmet: list[int], seznam_vyuc: list[str]) -> None:
    """
    Kontroluje, zda počet volných hodin odpovídá potřebnému počtu hodin k odučení.
    Kontroluje, zda se do úseku volen vejdou všechny přednášky z hlediska délek.
    :param chyby: seznam s chybami
    :param vyucujici_casy: data volných hodin vyučujících
    :param pppdv: v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    :param seznam_delkaPredmetu_predmet: seznam délek předmětů
    :param seznam_vyuc: seznam vyučujících
    :return: None
    """
    for vyuc in range(len(seznam_vyuc)):
        pocet_jednicek = pomocne_funkce.Zjisti_PocetJednicekVyuc(vyuc, vyucujici_casy)
        seznam_predmety_pp_delky = pomocne_funkce.Najdi_PredmetyVyucujiciho(pppdv, vyuc, seznam_delkaPredmetu_predmet, seznam_vyuc)
        # [[predmet1, pocet_prednasek, delka_predenasky], [predmet2, pocet_prednasek, delka_predenasky], ...]
        pocet_hodin_k_oduceni = 0
        if seznam_predmety_pp_delky:
            for p in range(len(seznam_predmety_pp_delky)):
                pocet_hodin_k_oduceni += seznam_predmety_pp_delky[p][1]*seznam_predmety_pp_delky[p][2]
        if pocet_jednicek < pocet_hodin_k_oduceni:
            # print(seznam_vyuc[vyuc], pocet_jednicek, pocet_hodin_k_oduceni, seznam_predmety_pp_delky)
            chyby.append(f"[CHYBA] Vyucujici: {seznam_vyuc[vyuc]}, nemá dostatek volen k oduceni: {pocet_hodin_k_oduceni} hodin")
        """
        elif pocet_jednicek == pocet_hodin_k_oduceni:
            chyby.append(f"[UPOZORNENI] Vyucujici: {seznam_vyuc[vyuc]}, má stejný počet volen jako počet hodin k odučení.")
        """
        delky_prednasek_se_vejdou_do_volen = Kontrola_DelekPrednasek(vyuc, vyucujici_casy, seznam_predmety_pp_delky, seznam_vyuc)
        if not delky_prednasek_se_vejdou_do_volen:
            chyby.append(f"[CHYBA] Vyucujici: {seznam_vyuc[vyuc]}, nemá dostatečně velké úseky volen")


def Kontrola_DelekPrednasek(vyuc: int, vyucujici_casy: list[list[list[int]]], seznam_predmety_pp_delky: list[list[int]], seznam_vyuc: list[str]):
    """
    Kontroluje, zda jsou délky přednášek 2, 3 nebo 4.
    :param vyuc: index vyučujícího
    :param vyucujici_casy: data volných hodin vyučujících
    :param seznam_predmety_pp_delky: pomocný seznam obsahující délky přednášek a jejich počet
    :param seznam_vyuc: seznam vyučujících
    :return: bool
    """
    delky_prednasek_vyuc = [0, 0, 0]
    for predmet in range(len(seznam_predmety_pp_delky)):
        if seznam_predmety_pp_delky[predmet][2] == 2:
            delky_prednasek_vyuc[0] = 1
        elif seznam_predmety_pp_delky[predmet][2] == 3:
            delky_prednasek_vyuc[1] = 1
        elif seznam_predmety_pp_delky[predmet][2] == 4:
            delky_prednasek_vyuc[2] = 1
    pocet_jednicek_za_sebou = Zjisti_MaxPocetJednicekZaSebou(vyucujici_casy, vyuc, seznam_vyuc)
    for delka in range(3):
        if delky_prednasek_vyuc[delka] != 0 and (delka+2) > pocet_jednicek_za_sebou:
            return False
    return True


def Vypis_Chyby(chyby: list[str], upozorneni: list[str]) -> None:
    """
    Vypisuje chyby do souboru logs/chyby.txt
    :param chyby: seznam nalezených chyb
    :return: None
    """
    if chyby or upozorneni:
        cesta = os.path.join('logs', 'chyby.txt')
        with open(cesta, 'w', encoding='utf-8') as f:
            for chyba in chyby:
                f.write(chyba + '\n')
            for upozorneni_ in upozorneni:
                f.write(upozorneni_ + '\n')
        f.close()
        if upozorneni:
            print("Některá data chyběla v souborech s časy. Jsou vypsána upozornění o automatickém přidání do souboru logs/chyby.txt")
        if chyby:
            print("Našel jsem chyby ve vstupních souborech. Jsou vypsány v souboru logs/chyby.txt")
            sys.exit()


def Zjisti_MaxPocetJednicekZaSebou(vyucujici_casy: list[list[list[int]]], vyuc: int, seznam_vyuc: list[str]) -> int:
    """
    Hledá maximální počet jedniček za sebou v seznamu vyučující časy -> čím větší úsek tím délší předmět se může zapsat.
    :param vyucujici_casy: data volných hodin vyučujících
    :param vyuc: index vyučujícího v seznamu vyučujících
    :param seznam_vyuc: seznam vyučujících
    :return: maximální počet jedniček za sebou jdoucích
    """
    max = 1
    for den in range(5):
        pocet_jednicek_za_sebou = 0
        for cas in range(12):  # 0-11
            if vyucujici_casy[vyuc][den][cas] == 1:
                pocet_jednicek_za_sebou += 1
            else:
                pocet_jednicek_za_sebou = 0
            if max < pocet_jednicek_za_sebou:
                max = pocet_jednicek_za_sebou
    return max
