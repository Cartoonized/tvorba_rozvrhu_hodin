import csv
import json


def Nacti_JSON(cesta: str) -> list:
    """
    Načítá json soubory.
    :param cesta: cesta k souboru
    :return: seznam načtených dat jako str
    """
    seznam = []
    with open(cesta, 'r', encoding="utf-8") as json_file:
        hodnoty = json.load(json_file)

        for radek in hodnoty:
            name = radek['name']
            Po = radek['Po']
            Ut = radek['Ut']
            St = radek['St']
            Ct = radek['Ct']
            Pa = radek['Pa']
            seznam.append([name, [Po, Ut, St, Ct, Pa]])
        json_file.close()
    return seznam


def Nacti_CSV(cesta: str) -> list:
    """
    Načítá csv soubory.
    :param cesta: cesta k souboru
    :return: seznam načtených dat jako str
    """
    seznam = []
    with open(cesta, newline='', encoding="utf-8") as csv_file:
        hodnoty = csv.reader(csv_file)
        next(hodnoty)

        for radek in hodnoty:
            if radek:
                seznam.append(radek)
        csv_file.close()
    return seznam
