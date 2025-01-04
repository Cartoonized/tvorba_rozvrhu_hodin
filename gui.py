import copy
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]


def Prevod_Rozvrhu(rozvrhy, index, seznam_delkaPredmetu_predmet):
    """
    převádí zapsané předměty do seznamu
    :param rozvrhy:
    :param index:
    :param seznam_delkaPredmetu_predmet:
    :return: seznam [den, predmet, cas, cas + delka_prednasky, vyucujici, mistnost, obor]
    """
    rozvrh = copy.deepcopy(rozvrhy[index])
    prevedeny_rozvrh = []
    for obor in range(len(rozvrh)):
        prevedeny_rozvrh.append([])
        for den in range(5):
            cas = 0
            while cas != 12:
                if rozvrh[obor][den][cas]:
                    vyucujici = rozvrh[obor][den][cas][0]
                    predmet = rozvrh[obor][den][cas][1]
                    mistnost = rozvrh[obor][den][cas][2]
                    delka_prednasky = seznam_delkaPredmetu_predmet[predmet]
                    prevedeny_rozvrh[obor].append([den, predmet, cas, cas + delka_prednasky, vyucujici, mistnost, obor])
                    cas += delka_prednasky
                else:
                    cas += 1
    return prevedeny_rozvrh


def Proved_PrevodUpravRozvrhuProOboryNaSlovnik(upraveny_rozvrh, seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich):
    """
    převádí seznamy rozvrhů, které obsahují potřebná data pro výpis rozvrhů pro obory, na slovník
    :param upraveny_rozvrh: rozvrh (seznam), kde každý předmět je převeden na seznam [den, predmet, cas, cas + delka_prednasky, vyucujici, mistnost, obor]
    :param seznam_oboru: seznam oborů
    :param seznam_predmetu: seznam předmětů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :return: rozvrh v podobě slovnku
    """
    # {"den": "Čtvrtek", "predmet": "DB1", "zacatek": 10, "konec": 13, "vyucujici": "Kovář", "mistnost": "P4"}
    dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
    rozvrh_slovnik = {seznam_oboru[obor]: upraveny_rozvrh[obor] for obor in range(len(upraveny_rozvrh))}
    for obor in range(len(seznam_oboru)):
        for predmet in range(len(upraveny_rozvrh[obor])):
            rozvrh_slovnik[seznam_oboru[obor]][predmet] = {
                "den": dny[upraveny_rozvrh[obor][predmet][0]],
                "predmet": seznam_predmetu[upraveny_rozvrh[obor][predmet][1]],
                "zacatek": upraveny_rozvrh[obor][predmet][2] + 8,
                "konec": upraveny_rozvrh[obor][predmet][3] + 8,
                "vyucujici": seznam_vyucujicich[upraveny_rozvrh[obor][predmet][4]],
                "mistnost": seznam_mistnosti[upraveny_rozvrh[obor][predmet][5]]}
    return rozvrh_slovnik


def Proved_PrevodUpravRozvrhuProMistnostiNaSlovnik(upraveny_rozvrh, seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich):
    """
    převádí seznamy rozvrhů, které obsahují potřebná data pro výpis rozvrhů pro místnosti, na slovník
    :param upraveny_rozvrh: rozvrh (seznam), kde každý předmět je převeden na seznam [den, predmet, cas, cas + delka_prednasky, vyucujici, mistnost, obor]
    :param seznam_oboru: seznam oborů
    :param seznam_predmetu: seznam předmětů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :return: rozvrh v podobě slovnku
    """
    dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
    rozvrh_slovnik = {seznam_mistnosti[mistnost]: [] for mistnost in range(len(seznam_mistnosti))}
    for obor in range(len(seznam_oboru)):
        for predmet in range(len(upraveny_rozvrh[obor])):
            mistnost_index = upraveny_rozvrh[obor][predmet][5]
            mistnost = seznam_mistnosti[mistnost_index]

            rozvrh_slovnik[mistnost].append({
                "den": dny[upraveny_rozvrh[obor][predmet][0]],
                "predmet": seznam_predmetu[upraveny_rozvrh[obor][predmet][1]],
                "zacatek": upraveny_rozvrh[obor][predmet][2] + 8,
                "konec": upraveny_rozvrh[obor][predmet][3] + 8,
                "vyucujici": seznam_vyucujicich[upraveny_rozvrh[obor][predmet][4]],
                "mistnost": seznam_mistnosti[upraveny_rozvrh[obor][predmet][5]]})
    return rozvrh_slovnik


def Proved_PrevodUpravRozvrhuProVyucujiciNaSlovnik(upraveny_rozvrh, seznam_oboru, seznam_predmetu, seznam_mistnosti, seznam_vyucujicich):
    """
    převádí seznamy rozvrhů, které obsahují potřebná data pro výpis rozvrhů pro vyučující, na slovník
    :param upraveny_rozvrh: rozvrh (seznam), kde každý předmět je převeden na seznam [den, predmet, cas, cas + delka_prednasky, vyucujici, mistnost, obor]
    :param seznam_oboru: seznam oborů
    :param seznam_predmetu: seznam předmětů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :return: rozvrh v podobě slovnku
    """
    dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
    rozvrh_slovnik = {seznam_vyucujicich[vyucujici]: [] for vyucujici in range(len(seznam_vyucujicich))}
    for obor in range(len(seznam_oboru)):
        for predmet in range(len(upraveny_rozvrh[obor])):
            vyucujici_index = upraveny_rozvrh[obor][predmet][4]
            vyucujici = seznam_vyucujicich[vyucujici_index]

            rozvrh_slovnik[vyucujici].append({
                "den": dny[upraveny_rozvrh[obor][predmet][0]],
                "predmet": seznam_predmetu[upraveny_rozvrh[obor][predmet][1]],
                "zacatek": upraveny_rozvrh[obor][predmet][2] + 8,
                "konec": upraveny_rozvrh[obor][predmet][3] + 8,
                "vyucujici": seznam_vyucujicich[upraveny_rozvrh[obor][predmet][4]],
                "mistnost": seznam_mistnosti[upraveny_rozvrh[obor][predmet][5]]})

    return rozvrh_slovnik


def Vypis_rozvrhu(rozvrh_oboru, canvas_frame, obor_name, index):
    """
    vypisuje rozvrh jednoho oboru
    :param rozvrh_oboru: rozvrh jednoho oboru
    :param canvas_frame: plátno
    :param obor_name: název oboru
    :param index: index data co chci vypsat (rozvrh pro Obory - 0 / Místnosti - 1 / Vyučující - 2)
    :return: None
    """
    dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
    dny.reverse()
    day_to_index = {day: i for i, day in enumerate(dny)}

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, day in enumerate(dny):
        ax.add_patch(Rectangle((8, i), 13, 1, facecolor="lightgray", edgecolor="black"))
        ax.text(6.8, i + 0.5, day, ha='left', va='center', color='black', fontsize=10, fontweight='bold')

    for predmet in rozvrh_oboru:
        day_idx = day_to_index[predmet["den"]]
        start_time = predmet["zacatek"]
        duration = predmet["konec"] - predmet["zacatek"]
        ax.broken_barh([(start_time, duration)], (day_idx + 0.3, 0.7), facecolors='gray', edgecolor='black')
        ax.broken_barh([(start_time, duration)], (day_idx, 0.3), facecolors='white', edgecolor='black')
        ax.text(start_time + duration / 2, day_idx + 0.62, predmet["predmet"], ha='center', va='center', color='black')

        ax.text(start_time + 0.2, day_idx + 0.1, predmet["vyucujici"], ha='left', va='bottom', fontsize=8, color='black')
        ax.text(start_time + duration - 0.2, day_idx + 0.1, predmet["mistnost"], ha='right', va='bottom', fontsize=8, color='black')


    ax.set_xlim(8, 20)
    ax.set_xticks(range(8, 21))
    ax.set_xticklabels([f"{hour}:00" for hour in range(8, 21)])
    ax.set_xlabel("")
    ax.xaxis.tick_top()
    ax.set_yticks([i + 0.5 for i in range(len(dny))])
    ax.set_yticklabels([])
    ax.set_ylim(0, len(dny))
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    if index == "Obory":
        ax.text(6.8, len(dny) + 0.5, f"Obor: {obor_name}", ha='left', va='center', fontsize=12, fontweight='bold')
    elif index == "Místnosti":
        ax.text(6.8, len(dny) + 0.5, f"Místnost: {obor_name}", ha='left', va='center', fontsize=12, fontweight='bold')
    else:
        ax.text(6.8, len(dny) + 0.5, f"Vyučující: {obor_name}", ha='left', va='center', fontsize=12, fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()


def Vykresli_Rozvrh(rozvrh_combobox, canvas_frame, canvas_container, rozvrhy, seznam_oboru, seznam_mistnosti, seznam_vyucujicich, seznam_predmetu, delky_predmetu, rozvrh_combobox2):
    """
    vykresluje rozvrh do gui
    :param rozvrh_combobox: combobox výběru indexu vytvořeného rozvrhu
    :param canvas_frame: plátno
    :param canvas_container: kontejnej pláten
    :param rozvrhy: rozvrhy všech oborů
    :param seznam_oboru: seznam oborů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :param seznam_predmetu: seznam předmětů
    :param delky_predmetu: seznam délek předmětů
    :param rozvrh_combobox2: combobox výběru indexu dat pro výpis (rozvrh pro Obory / Místnosti / Vyučující)
    :return: None
    """
    selected_rozvrh_index = int(rozvrh_combobox.get()) - 1
    selected_rozvrh_udaje = rozvrh_combobox2.get()
    prevedeny_rozvrh_pro_obory = Prevod_Rozvrhu(rozvrhy, selected_rozvrh_index, delky_predmetu)
    if selected_rozvrh_udaje == "Obory":
        rozvrh = Proved_PrevodUpravRozvrhuProOboryNaSlovnik(prevedeny_rozvrh_pro_obory,
                                                            seznam_oboru,
                                                            seznam_predmetu,
                                                            seznam_mistnosti,
                                                            seznam_vyucujicich)
    elif selected_rozvrh_udaje == "Místnosti":
        rozvrh = Proved_PrevodUpravRozvrhuProMistnostiNaSlovnik(prevedeny_rozvrh_pro_obory,
                                                                seznam_oboru,
                                                                seznam_predmetu,
                                                                seznam_mistnosti,
                                                                seznam_vyucujicich)
    else:
        rozvrh = Proved_PrevodUpravRozvrhuProVyucujiciNaSlovnik(prevedeny_rozvrh_pro_obory,
                                                                seznam_oboru,
                                                                seznam_predmetu,
                                                                seznam_mistnosti,
                                                                seznam_vyucujicich)
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    for nazev_oboru, rozvrh_oboru in rozvrh.items():
        Vypis_rozvrhu(rozvrh_oboru, canvas_frame, nazev_oboru, selected_rozvrh_udaje)
    canvas_container.yview_moveto(0)


def on_close(root):
    """
    zavírá okno při kliknutí na křížek
    :param root: root
    :return: None
    """
    if messagebox.askokcancel("Konec", "Checete program ukončit?"):
        root.quit()


def on_mouse_wheel(event, canvas_container):
    """
    umožňuje scrollování kolečkem myši
    :param event: událost scrollování
    :param canvas_container: kontejnej pláten
    :return:
    """
    canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")  # Scroll o 1 jednotku podle směru kolečka


def Vypis_Gui(rozvrhy, seznam_oboru, seznam_mistnosti, seznam_vyucujicich, seznam_predmetu, delky_predmetu):
    """
    hlavní funkce pro výpis a interakce s gui
    :param rozvrhy: vytvořené rozvrhy
    :param seznam_oboru: seznam oborů
    :param seznam_mistnosti: seznam místností
    :param seznam_vyucujicich: seznam vyučujících
    :param seznam_predmetu: seznam předmětů
    :param delky_predmetu:
    :return: None
    """
    root = tk.Tk()
    root.title("Výběr rozvrhu")
    root.state('zoomed')

    rozvrh_label = tk.Label(root, text="Vyberte číslo rozvrhu:")
    rozvrh_label.pack(padx=10, pady=5)

    rozvrh_combobox = ttk.Combobox(root, values=[str(i + 1) for i in range(len(rozvrhy))], state="readonly")
    rozvrh_combobox.pack(padx=10, pady=5)

    rozvrh_combobox2 = ttk.Combobox(root, values=["Obory", "Místnosti", "Vyučující"], state="readonly")
    rozvrh_combobox2.pack(padx=10, pady=5)

    show_button = tk.Button(root, text="Zobrazit rozvrhy", command=lambda: Vykresli_Rozvrh(rozvrh_combobox,
                                                                                           canvas_frame,
                                                                                           canvas_container,
                                                                                           rozvrhy,
                                                                                           seznam_oboru,
                                                                                           seznam_mistnosti,
                                                                                           seznam_vyucujicich,
                                                                                           seznam_predmetu,
                                                                                           delky_predmetu,
                                                                                           rozvrh_combobox2))
    show_button.pack(padx=10, pady=10)

    canvas_container = tk.Canvas(root)
    canvas_container.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas_container.yview)
    scrollbar.pack(side="right", fill="y")

    canvas_frame = tk.Frame(canvas_container)
    canvas_window = canvas_container.create_window((0, 0), window=canvas_frame, anchor="n")
    canvas_container.config(yscrollcommand=scrollbar.set)

    canvas_frame.bind("<Configure>", lambda e: canvas_container.config(scrollregion=canvas_container.bbox("all")))

    root.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas_container))
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()

