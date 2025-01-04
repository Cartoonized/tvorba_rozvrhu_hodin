import os
import time
from nacti_data import Nacti_CSV, Nacti_JSON
import kontroly
import tvorba_seznamu_z_nactenych_dat
import hodnoceni_predmetu
import tvorba_rozvrhu
import vypis_pomocnych_udaju
import pomocne_funkce
import gui
import hledej_a_zapis_pred_napevno


if __name__ == "__main__":
    start = time.time()
    dny = ["Po", "Ut", "St", "Ct", "Pa"]
    delka_Predmetu = [2, 3, 4]  # napevno!

    seznam_obor_predmet = Nacti_CSV(os.path.join('csv', 'obor_predmet.csv'))
    seznam_predmet_mistnost_poradi = Nacti_CSV(os.path.join('csv', 'predmet_mistnost_poradi.csv'))
    seznam_predmet_delkaPredmetu = Nacti_CSV(os.path.join('csv', 'predmet_delkaPredmetu.csv'))
    seznam_vyucujici_predmet_pocetPrednasek = Nacti_CSV(os.path.join('csv', 'vyucujici_predmet_pocetPrednasek.csv'))

    # kod predmetu, vyucujici, mistnost, den, casOd, delka prednasky
    data_o_jiz_zapsanych_p = Nacti_CSV(os.path.join('csv', 'predmety_napevno.csv'))

    seznam_vyucujici_casy = Nacti_JSON(os.path.join('json', 'vyucujici_casy.json'))
    seznam_mistnosti_casy = Nacti_JSON(os.path.join('json', 'mistnosti_casy.json'))

    pomocne_funkce.Odstran_OpakPrvkySeznamu(seznam_obor_predmet)
    pomocne_funkce.Odstran_OpakPrvkySeznamu(seznam_predmet_mistnost_poradi)
    pomocne_funkce.Odstran_OpakPrvkySeznamu(seznam_predmet_delkaPredmetu)
    pomocne_funkce.Odstran_OpakPrvkySeznamu(seznam_vyucujici_predmet_pocetPrednasek)
    pomocne_funkce.Odstran_OpakPrvkySeznamu(data_o_jiz_zapsanych_p)

    # ze souboru obor_predmet.csv
    seznam_oboru = tvorba_seznamu_z_nactenych_dat.Priprav_Seznam_Oboru(seznam_obor_predmet)

    # ze souboru obor_predmet.csv
    seznam_predmetu = tvorba_seznamu_z_nactenych_dat.Priprav_Seznam_Predmetu(seznam_obor_predmet)

    # ze souboru vyucujici_predmet_pocetPrednasek
    seznam_vyucujicich = tvorba_seznamu_z_nactenych_dat.Priprav_Seznam_Vyuc(seznam_vyucujici_predmet_pocetPrednasek)

    # ze souboru predmet_mistnost_poradi.csv
    seznam_mistnosti = tvorba_seznamu_z_nactenych_dat.Priprav_Seznam_Mistnosti(seznam_predmet_mistnost_poradi)  # ze souboru

    # pokud je ve sloupci více nenulových čísel -> pro všechny řádky(obory) je tento sloupec(předmět) společný
    pocet_potrebnych_prednasek_dle_oboru = tvorba_seznamu_z_nactenych_dat.Vytvor_PPPDO(seznam_obor_predmet, seznam_oboru, seznam_predmetu)

    # v řádcích jsou vyučující, ve sloupcích jsou předměty a hodnoty jsou počet přednášek vyučujícího k odučení
    pocet_potrebnych_prednasek_dle_vyucujiciho = tvorba_seznamu_z_nactenych_dat.Vytvor_PPPDV(seznam_vyucujici_predmet_pocetPrednasek,
                                                              seznam_vyucujicich,
                                                              seznam_predmetu)

    # v řádkcích jsou místnosti, ve sloupcích předměty, hodnoty = pořadí
    preference_mistnosti = tvorba_seznamu_z_nactenych_dat.Vytvor_PrefMist(seznam_predmet_mistnost_poradi, seznam_mistnosti, seznam_predmetu)

    # index je předmět, hodnota je délka přednášky
    # POCET PREDMETU ZDE JE 50 ZATIMCO len(seznam_predmetu) = 46
    seznam_delkaPredmetu_predmet = tvorba_seznamu_z_nactenych_dat.Vytvor_DP(seznam_predmet_delkaPredmetu, seznam_predmetu)

    upozorneni = []

    # v řádcích jsou vyučující, ve sloupcích dny s hodinami, 1 -> má volno, 0 -> nemá volno
    vyucujici_casy = tvorba_seznamu_z_nactenych_dat.Vytvor_Casy(seznam_vyucujici_casy, seznam_vyucujicich, upozorneni, 0)

    # v řádcích jsou mistnosti, ve sloupcích dny s hodinami, 1 -> je volno, 0 -> není volno
    mistnosti_casy = tvorba_seznamu_z_nactenych_dat.Vytvor_Casy(seznam_mistnosti_casy, seznam_mistnosti, upozorneni, 1)

    # v řádcích jsou obory, ve sloupcích dny s hodinami, 1 -> má volno, 0 -> nemá volno
    obory_casy = tvorba_seznamu_z_nactenych_dat.Vytvor_Tabulku_Obsazenosti(seznam_oboru)

    """
    LP2.LP(pocet_potrebnych_prednasek_dle_oboru,
           pocet_potrebnych_prednasek_dle_vyucujiciho,
           vyucujici_casy,
           obory_casy,
           mistnosti_casy,
           seznam_oboru,
           seznam_predmetu,
           seznam_vyucujicich)
    """
    # seznam chyb
    chyby = kontroly.Kontrola_Vst_Dat(seznam_predmetu,
                                      seznam_predmet_delkaPredmetu,
                                      seznam_predmet_mistnost_poradi,
                                      seznam_vyucujici_predmet_pocetPrednasek,
                                      data_o_jiz_zapsanych_p,
                                      delka_Predmetu,
                                      seznam_vyucujicich,
                                      seznam_mistnosti,
                                      vyucujici_casy,
                                      mistnosti_casy,
                                      pocet_potrebnych_prednasek_dle_vyucujiciho,
                                      seznam_delkaPredmetu_predmet)
    kontroly.Vypis_Chyby(chyby, upozorneni)

    seznam_poradi_predmetu, seznam_vlivu, seznam_hodnoceni = hodnoceni_predmetu.Vytvor_SeznamPoradiPredmetu(pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                                                         vyucujici_casy,
                                                                                         seznam_predmetu,
                                                                                         seznam_delkaPredmetu_predmet,
                                                                                         preference_mistnosti,
                                                                                         pocet_potrebnych_prednasek_dle_oboru)
    seznam_poradi_predmetu = pomocne_funkce.Odstran_OpakPrvkySeznamu(seznam_poradi_predmetu)
    hledej_a_zapis_pred_napevno.Proved_ZapisPredmetuNapevno(data_o_jiz_zapsanych_p,
                                                            vyucujici_casy,
                                                            pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                            seznam_delkaPredmetu_predmet,
                                                            seznam_vyucujicich,
                                                            pocet_potrebnych_prednasek_dle_oboru,
                                                            preference_mistnosti,
                                                            seznam_predmetu,
                                                            seznam_vyucujicich,
                                                            seznam_mistnosti,
                                                            mistnosti_casy)

    sablona_rozvrhu = tvorba_rozvrhu.Vytvor_SablonuRozvrhu(len(seznam_oboru),
                                            pocet_potrebnych_prednasek_dle_oboru,
                                            pocet_potrebnych_prednasek_dle_vyucujiciho,
                                            obory_casy,
                                            vyucujici_casy,
                                            mistnosti_casy,
                                            seznam_predmetu,
                                            seznam_vyucujicich,
                                            seznam_mistnosti,
                                            data_o_jiz_zapsanych_p,
                                            seznam_oboru)
    pocet_prepsani = [3, int((len(seznam_predmetu) - (len(seznam_predmetu) % 2))/2)]
    # pocet_prepsani = [0, 0]
    vytvorene_rozvrhy = []
    seznam_vlivy_vytv_roz = []
    seznam_vliv_predmety_hodnoceni_nezapPred = []
    posl = []
    vlivy_posl = []
    hodnoceni_posl = []
    print("Zkouším první algoritmus...")

    for i in range(2):
        vytvorene_rozvrhy, \
        seznam_vlivy_vytv_roz, \
        seznam_vliv_predmety_hodnoceni_nezapPred,\
        posl, vlivy_posl, hodnoceni_posl = tvorba_rozvrhu.TvorRozvrhyProRuzneVlivy(seznam_poradi_predmetu,
                                                                            seznam_vlivu,
                                                                            pocet_potrebnych_prednasek_dle_oboru,
                                                                            pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                                            vyucujici_casy,
                                                                            obory_casy,
                                                                            mistnosti_casy,
                                                                            seznam_delkaPredmetu_predmet,
                                                                            preference_mistnosti,
                                                                            seznam_predmetu,
                                                                            sablona_rozvrhu,
                                                                            seznam_hodnoceni,
                                                                            seznam_oboru,
                                                                            seznam_mistnosti,
                                                                            seznam_vyucujicich,
                                                                            data_o_jiz_zapsanych_p,
                                                                            pocet_prepsani[i])
        if vytvorene_rozvrhy:
            break

    if not vytvorene_rozvrhy:
        if posl:
            print("Zkouším druhý algoritmus...")
            vytvorene_rozvrhy = tvorba_rozvrhu.Tvor_RozvrhyUpravouPosloupnosti(posl,
                                                           vlivy_posl,
                                                           pocet_potrebnych_prednasek_dle_oboru,
                                                           pocet_potrebnych_prednasek_dle_vyucujiciho,
                                                           vyucujici_casy,
                                                           obory_casy,
                                                           mistnosti_casy,
                                                           seznam_delkaPredmetu_predmet,
                                                           preference_mistnosti,
                                                           seznam_predmetu,
                                                           sablona_rozvrhu,
                                                           hodnoceni_posl,
                                                           seznam_oboru,
                                                           seznam_mistnosti,
                                                           seznam_vyucujicich)
    if vytvorene_rozvrhy:
        print(f"Maximální povolený počet přepsání předmětů: {pocet_prepsani}")
        rozvrhy = pomocne_funkce.Odstran_OpakujiciSeRozvrhy(vytvorene_rozvrhy)
        pomocne_funkce.Vypis_Vlivy(seznam_vlivy_vytv_roz)
        print(f"Ruznych rozvrhu je: {len(rozvrhy)}")
        konec = time.time()
        cas = round(konec - start, 2)
        print(f"Kód běžel po dobu {cas} sekund.")
        gui.Vypis_Gui(rozvrhy, seznam_oboru, seznam_mistnosti, seznam_vyucujicich, seznam_predmetu, seznam_delkaPredmetu_predmet)
    else:
        konec = time.time()
        cas = round(konec - start, 2)
        print(f"Kód běžel po dobu {cas} sekund.")
        print("")
        print("Nejsou zadne vytvorene rozvrhy!")
    cesta_k_pom_excel = "xlsx/vlivy_predmety_hodnoty_nezapPred.xlsx"
    vypis_pomocnych_udaju.Vypis_PomUdajeDoExcelu(cesta_k_pom_excel, seznam_vliv_predmety_hodnoceni_nezapPred, seznam_predmetu)